# Generales
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.db.models import Count
# Modelos
from principal.models import *
# Formularios
from principal.forms import *
# Login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Login y salida
def ingreso(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        print(form.errors)
        if form.is_valid():
            username = form.data.get("username")
            raw_password = form.data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.info(request, "Saludos  %s" % user)
                return redirect(index)
        else:
            messages.info(request, "Credenciales incorrectas")
    else:
        form = AuthenticationForm()
    informacion_template = {'form': form}
    return render(request, 'logearse.html', informacion_template)

def salida(request):
    logout(request)
    messages.info(request, "Sesión finalizada")
    return redirect(index)

@login_required(login_url='/login/')  
def index(request):
    telefonos = Telefono.objects.all()
    dispositivos = Dispositivo.objects.all()
    accesorios = Accesorio.objects.all()
    monederos = Monedero.objects.all()
    
    cantidad_modelo = ModeloTelefono.objects.annotate(Count('modelos'))
    n =0
    modelos_telefonos= []
    
    for x in cantidad_modelo:
        consulta =Telefono.objects.filter(modelo=cantidad_modelo[n].id).filter(vendido=True).count()
        consulta2 =Telefono.objects.filter(modelo=cantidad_modelo[n].id).filter(vendido=False).count()
        modelos_telefonos.append(
            {'modelo': cantidad_modelo[n].nombre , 'cantidad':cantidad_modelo[n].modelos__count, 'vendidos': consulta, 'novendidos':consulta2 })
        n+=1
        
    monederos = Monedero.objects.all()
    informacion = {'telefonos': telefonos, 'dispositivos':dispositivos, 'accesorios':accesorios,'monederos':monederos, 'modelos_telefonos':modelos_telefonos, 'monederos':monederos}
    return render(request, 'index.html', informacion)

@login_required(login_url='/login/')  
def telefonos(request):
    telefonos = Telefono.objects.all()
    monederos = Monedero.objects.all()
    informacion = {'telefonos': telefonos, 'monederos':monederos}
    return render(request, 'telefonos.html', informacion)

@login_required(login_url='/login/')  
def crear_telefono(request):
    if request.method=='POST':
        form = FormTelefono(request.POST)
        if form.is_valid():
                form.save() 
                messages.info(request, "Creado exitosamente")
                return redirect(index)
    else:
        form = FormTelefono()
    titulo = "Añadir telefono"
    monederos = Monedero.objects.all()
    informacion = {'form':form, 'titulo':titulo, 'monederos':monederos}
    return render(request, 'forms/form-telefonos.html',  informacion)

@login_required(login_url='/login/')  
def editar_telefono(request, id):
    telefono = Telefono.objects.get(pk=id)
    if request.method=='POST':
        form = FormTelefono(request.POST, instance=telefono)
        if form.is_valid():
                form.save()
                messages.info(request, "Teléfono modificado")
                return redirect(index)
    else:
        form = FormTelefono(instance=telefono)
    titulo = "Editar información del telefono"
    monederos = Monedero.objects.all()
    informacion = {'form':form, 'titulo':titulo, 'monederos':monederos}
    return render(request, 'forms/form-telefonos.html',  informacion)

@login_required(login_url='/login/')  
def eliminar_telefono(request, id):
    Telefono.objects.get(pk=id).delete()
    messages.info(request, "Teléfono eliminado")
    return redirect(index)
    
@login_required(login_url='/login/')  
def monedero(request, id):
    monedero = Monedero.objects.get(pk=id)
    monederos = Monedero.objects.all()
    informacion = {'monedero':monedero, 'monederos':monederos}
    return render(request, 'monedero.html', informacion)

@login_required(login_url='/login/')  
def monedero_telefono(request, id):
    telefono = Telefono.objects.get(pk=id)
    if request.method=='POST':
        form = FormMonederoTelefono(telefono, request.POST)
        if form.is_valid():
            form.save()
            return redirect(index)
    else:
        form = FormMonederoTelefono(telefono)
    titulo = "Repartir dinero de "
    monederos = Monedero.objects.all()
    diccionario = {'form': form, 'telefono': telefono, 'titulo':titulo, 'valor':True, 'valor3': True,  'monederos':monederos}
    return render(request, 'forms/form-transacciones.html', diccionario)

@login_required(login_url='/login/')  
def monedero_transaccion(request, id):
    monedero = Monedero.objects.get(pk=id)
    if request.method=='POST':
        form = FormMonedero(monedero, request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Transacción registrada")
            return redirect('monedero', id=id)
    else:
        form = FormMonedero(monedero)
    titulo = "Nueva transacción"
    monederos = Monedero.objects.all()
    diccionario = {'form': form, 'monedero': monedero, 'titulo':titulo, 'valor':True, 'valor2': True, 'monederos':monederos}
    return render(request, 'forms/form-transaccion-nueva.html', diccionario)

@login_required(login_url='/login/')  
def eliminar_transaccion(request, id, mn):
    Transaccion.objects.get(pk=id).delete()
    messages.info(request, "Transación eliminada")
    return redirect('monedero', id=mn)
    
@login_required(login_url='/login/')  
def dispositivos(request):
    dispositivos = Dispositivo.objects.all()
    monederos = Monedero.objects.all()
    informacion = {'dispositivos': dispositivos, 'monederos':monederos}
    return render(request, 'dispositivos.html', informacion)

@login_required(login_url='/login/')  
def crear_dispositivo(request):
    if request.method=='POST':
        form = FormDispositivo(request.POST)
        if form.is_valid():
            form.save() 
            messages.info(request, "Creado exitosamente")
            return redirect(dispositivos)
    else:
        form = FormDispositivo()
    titulo = "Añadir dispositivo"
    monederos = Monedero.objects.all()
    informacion = {'form':form, 'titulo':titulo, 'monederos':monederos}
    return render(request, 'forms/form-dispositivos.html',  informacion)

@login_required(login_url='/login/')  
def editar_dispositivo(request, id):
    dispositivo = Dispositivo.objects.get(pk=id)
    if request.method=='POST':
        form = FormDispositivo(request.POST, instance=dispositivo)
        if form.is_valid():
            form.save()
            messages.info(request, "Modificación exitosa")
            return redirect(dispositivos)
    else:
        form = FormDispositivo(instance=dispositivo)
    titulo = "Editar información del dispositivo"
    monederos = Monedero.objects.all()
    informacion = {'form':form, 'titulo':titulo, 'monederos':monederos}
    return render(request, 'forms/form-dispositivos.html',  informacion)

@login_required(login_url='/login/')  
def eliminar_dispositivo(request, id):
        Dispositivo.objects.get(pk=id).delete()
        messages.info(request, "Dispositivo eliminado")
        return redirect(dispositivos)
    
@login_required(login_url='/login/')  
def monedero_dispositivo(request, id):
    dispositivo = Dispositivo.objects.get(pk=id)
    if request.method=='POST':
        form = FormMonederoDispositivo(dispositivo, request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Transacción exitosa")
            return redirect(index)
    else:
        form = FormMonederoDispositivo(dispositivo)
    titulo = "Repartir dinero de "
    monederos = Monedero.objects.all()
    diccionario = {'form': form, 'dispositivo': dispositivo, 'titulo':titulo, 'valor':True, 'valor3': True, 'monederos':monederos}
    return render(request, 'forms/form-transacciones2.html', diccionario)

@login_required(login_url='/login/')  
def crear_accesorio(request):
    if request.method=='POST':
        form = FormAccesorio(request.POST)
        if form.is_valid():
            form.save() 
            messages.info(request, "Creado exitosamente")
            return redirect(index)
    else:
        form = FormAccesorio()
    titulo = "Añadir accesorio"
    monederos = Monedero.objects.all()
    informacion = {'form':form, 'titulo':titulo, 'monederos':monederos}
    return render(request, 'forms/form-accesorios.html',  informacion)

@login_required(login_url='/login/')  
def monedero_accesorio(request, id):
    accesorio = Accesorio.objects.get(pk=id)
    if request.method=='POST':
        form = FormMonederoAccesorio(accesorio, request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Transacción exitosa")
            return redirect(index)
    else:
        form = FormMonederoAccesorio(accesorio)
    titulo = "Repartir dinero de "
    monederos = Monedero.objects.all()
    diccionario = {'form': form, 'accesorio': accesorio, 'titulo':titulo, 'valor':True, 'valor3': True, 'monederos':monederos}
    return render(request, 'forms/form-transacciones3.html', diccionario)

@login_required(login_url='/login/')  
def editar_accesorio(request, id):
    accesorio = Accesorio.objects.get(pk=id)
    if request.method=='POST':
        form = FormAccesorio(request.POST, instance=accesorio)
        if form.is_valid():
            form.save() 
            messages.info(request, "Accesorio modificado")
            return redirect(index)
    else:
        form = FormAccesorio(instance=accesorio)
    titulo = "Editar información del accesorio"
    monederos = Monedero.objects.all()
    informacion = {'form':form, 'titulo':titulo, 'monederos':monederos}
    return render(request, 'forms/form-accesorios.html',  informacion)

@login_required(login_url='/login/')  
def eliminar_accesorio(request, id):
    Accesorio.objects.get(pk=id).delete()
    messages.info(request, "Accesorio eliminado")
    return redirect(index)