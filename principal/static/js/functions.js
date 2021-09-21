
$(document).ready(function() {
    // Parametros del calendario
    $.datepicker.regional['es'] = {
        closeText: 'Cerrar',
        prevText: '< Ant',
        nextText: 'Sig >',
        currentText: 'Hoy',
        monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        monthNamesShort: ['Ene','Feb','Mar','Abr', 'May','Jun','Jul','Ago','Sep', 'Oct','Nov','Dic'],
        dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
        dayNamesShort: ['Dom','Lun','Mar','Mié','Juv','Vie','Sáb'],
        dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','Sá'],
        weekHeader: 'Sm',
        dateFormat: 'dd/mm/yy',
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: ''
    };
    $.datepicker.setDefaults($.datepicker.regional['es']);
    // Funcion del calendario
    $( function() {
        $( "#id_fecha_compra" ).datepicker({dateFormat: 'dd/mm/yy'}); 
        $( "#id_fecha_venta" ).datepicker({dateFormat: 'dd/mm/yy'}); 
    });
    
    verificacionVenta();
    $("#id_vendido").click( function() {
        verificacionVenta();
    });
    function verificacionVenta() {
        if ($('#id_vendido').is(':checked')) {
            $('.form2 input').prop('disabled', false); // Doble verificaion, se desactivael inpu
            $('.form2').removeAttr('disabled'); // Se desactiva el div con el conteneido css
            $('.form2 :input').removeAttr('disabled');
        } else {
            $('.form2 :input').prop('disabled', true);
            $('.form2').attr('disabled', true);
        }   
    }

    $("#id_llego_cargador").click( function() {
        verificacionCargador1();
    });
    function verificacionCargador1() {
        if ($('#id_llego_cargador').is(':checked')) {
            $('#id_llego_cargador_rapido').prop('checked', false); // Doble verificaion, se desactivael inputt
        } 
    }

    $("#id_llego_cargador_rapido").click( function() {
        verificacionCargador();
    });
    function verificacionCargador() {
        if ($('#id_llego_cargador_rapido').is(':checked')) {
            $('#id_llego_cargador').prop('checked', false); // Doble verificaion, se desactivael inputt
        } 
    }

    $("#id_sefue_cargador").click( function() {
        verificacionCargadorSefue();
    });
    function verificacionCargadorSefue() {
        if ($('#id_sefue_cargador').is(':checked')) {
            $('#id_sefue_cargador_rapido').prop('checked', false); // Doble verificaion, se desactivael inputt
        } 
    }
    $("#id_sefue_cargador_rapido").click( function() {
        verificacionCargadorSefue2();
    });
    function verificacionCargadorSefue2() {
        if ($('#id_sefue_cargador_rapido').is(':checked')) {
            $('#id_sefue_cargador').prop('checked', false); // Doble verificaion, se desactivael inputt
        } 
    }

    $('.eliminar').click(function() { // Si hace click en cualquier "eliminar"
        $('.obscurecer').fadeIn(120); // Se activa la capa principal
        $('#fondo-eliminar' + $(this).attr('target')).fadeIn(150); // Se activa solo el id de esa capa
    });
    $('.obscurecer, #cancelar').click(function() { // Si hace click en cualquier parte de lo obscuro
        $('.obscurecer').fadeOut(150); // Se oculta esa capa
        $('.cuadro-eliminar').fadeOut(150); // Se oculta todas las clases del cuadro
    });

    $('.ver').click(function() {
        $('.obscurecer').fadeIn(120);
        $('#fondo-ver' + $(this).attr('target')).fadeIn(150); 
    });
    $('.obscurecer, #cancelar').click(function() { 
        $('.cuadro-ver').fadeOut(150); 
    });

    $("#id_fecha_compra").attr("autocomplete", "off");
    $("#id_fecha_venta").attr("autocomplete", "off");
});