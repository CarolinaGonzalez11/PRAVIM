// Maneja el aviso de cambios sin guardar
let isFormDirty = false;
document.getElementById("formFicha").addEventListener("input", function () {
    isFormDirty = true;
});
window.addEventListener("beforeunload", function (e) {
    if (isFormDirty) {
        e.preventDefault();
        e.returnValue = '';
    }
});
document.getElementById("formFicha").addEventListener("submit", function () {
    isFormDirty = false;
});

// Expande los textarea automáticamente
document.addEventListener('DOMContentLoaded', () => {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const baseHeight = textarea.scrollHeight;
        textarea.style.height = baseHeight + 'px';
        textarea.addEventListener('input', () => {
            if (textarea.scrollHeight > textarea.offsetHeight) {
                textarea.style.height = 'auto';
                textarea.style.height = textarea.scrollHeight + 'px';
            }
        });
    });
});

// Habilita/deshabilita fecha de ingreso según el radio de "ingreso efectivo"
document.addEventListener('DOMContentLoaded', function () {
    const radios = document.getElementsByName('ingreso_efectivo');
    const fechaIngreso = document.getElementById('id_fecha_ingreso');
    function checkEstado() {
        let valor = null;
        radios.forEach(radio => { if (radio.checked) valor = radio.value; });
        if (valor === "True") {
            fechaIngreso.removeAttribute('disabled');
        } else {
            fechaIngreso.setAttribute('disabled', 'disabled');
            fechaIngreso.value = '';
        }
    }
    if (radios && fechaIngreso) {
        radios.forEach(radio => radio.addEventListener('change', checkEstado));
        checkEstado();
    }
});

// Calcula el total de integrantes en el hogar
document.addEventListener('DOMContentLoaded', function() {
    function updateTotalIntegrantes() {
        let adultos = parseInt(document.getElementById('id_n_adultos')?.value) || 0;
        let nna = parseInt(document.getElementById('id_n_nna')?.value) || 0;
        document.getElementById('total-integrantes').textContent = adultos + nna;
    }
    document.getElementById('id_n_adultos')?.addEventListener('input', updateTotalIntegrantes);
    document.getElementById('id_n_nna')?.addEventListener('input', updateTotalIntegrantes);
    updateTotalIntegrantes();
});

// Mostrar/ocultar campos de denuncia según el boolean "¿Tiene denuncia?"
document.addEventListener('DOMContentLoaded', () => {
    const checkbox = document.getElementById('id_tiene_denuncia');
    const detalleCampos = document.getElementById('denuncia-detalle-campos');
    function toggleDetalleCampos() {
        if (checkbox && detalleCampos) {
            detalleCampos.style.display = checkbox.checked ? 'table-row-group' : 'none';
        }
    }
    if (checkbox && detalleCampos) {
        checkbox.addEventListener('change', toggleDetalleCampos);
        toggleDetalleCampos(); // Estado inicial
    }
});



document.addEventListener('DOMContentLoaded', function () {
    // Mostrar campo "otro" si corresponde
    const lugarDenuncia = document.getElementById('id_lugar_denuncia');
    const otroLugarCampo = document.getElementById('otro-lugar-campo');
    if (lugarDenuncia && otroLugarCampo) {
        function toggleOtroLugar() {
            otroLugarCampo.style.display = (lugarDenuncia.value === 'OTRO') ? 'block' : 'none';
        }
        lugarDenuncia.addEventListener('change', toggleOtroLugar);
        toggleOtroLugar();
    }

    // Mostrar "otra dificultad"
    const dificultades = document.getElementsByName('dificultades');
    const dificultadesOtraCampo = document.getElementById('dificultades-otra-campo');
    if (dificultades && dificultadesOtraCampo) {
        function toggleDificultadOtra() {
            let checked = false;
            dificultades.forEach = Array.prototype.forEach;
            dificultades.forEach(input => {
                if (input.value === 'otra' && input.checked) checked = true;
            });
            dificultadesOtraCampo.style.display = checked ? 'block' : 'none';
        }
        dificultades.forEach(input => input.addEventListener('change', toggleDificultadOtra));
        toggleDificultadOtra();
    }

    // Mostrar detalle de medida cautelar solo si es sí
    const medidaCautelar = document.getElementById('id_medida_cautelar');
    const medidaCautelarDetalle = document.getElementById('medida-cautelar-detalle-campo');
    if (medidaCautelar && medidaCautelarDetalle) {
        function toggleMedidaDetalle() {
            medidaCautelarDetalle.style.display = medidaCautelar.checked ? 'block' : 'none';
        }
        medidaCautelar.addEventListener('change', toggleMedidaDetalle);
        toggleMedidaDetalle();
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const motivoSelect = document.getElementById('id_motivo_ingreso');
    const motivoOtroRow = document.getElementById('motivo-otro-row');
    function toggleMotivoOtro() {
        console.log("VALOR SELECT:", motivoSelect ? motivoSelect.value : "no hay motivoSelect");
        motivoOtroRow.style.display = (motivoSelect && motivoSelect.value && motivoSelect.value.toUpperCase() === 'OTROS') ? 'table-row' : 'none';
    }
    if (motivoSelect && motivoOtroRow) {
        motivoSelect.addEventListener('change', toggleMotivoOtro);
        toggleMotivoOtro();
    }
});


document.addEventListener('DOMContentLoaded', function() {
    // Diagnóstico: Mostrar campo "otro"
    const diagSelect = document.getElementById('id_diagnostico');
    const diagOtroRow = document.getElementById('diagnostico-otro-row');
    function toggleDiagOtro() {
        diagOtroRow.style.display = (diagSelect && diagSelect.value === 'otro') ? 'table-row' : 'none';
    }
    if (diagSelect && diagOtroRow) {
        diagSelect.addEventListener('change', toggleDiagOtro);
        toggleDiagOtro();
    }

    // Atención salud mental: año y lugar solo si SÍ
    const atencionCheck = document.getElementById('id_atencion_salud_mental');
    const atencionAnioRow = document.getElementById('atencion-anio-row');
    const atencionLugarRow = document.getElementById('atencion-lugar-row');
    function toggleAtencion() {
        const checked = atencionCheck && (atencionCheck.checked || atencionCheck.value === "True" || atencionCheck.value === "true" || atencionCheck.value === "1");
        atencionAnioRow.style.display = checked ? 'table-row' : 'none';
        atencionLugarRow.style.display = checked ? 'table-row' : 'none';
    }
    if (atencionCheck && atencionAnioRow && atencionLugarRow) {
        atencionCheck.addEventListener('change', toggleAtencion);
        toggleAtencion();
    }

    // Internación: año y lugar solo si SÍ
    const internacionCheck = document.getElementById('id_internacion');
    const internacionAnioRow = document.getElementById('internacion-anio-row');
    const internacionLugarRow = document.getElementById('internacion-lugar-row');
    function toggleInternacion() {
        const checked = internacionCheck && (internacionCheck.checked || internacionCheck.value === "True" || internacionCheck.value === "true" || internacionCheck.value === "1");
        internacionAnioRow.style.display = checked ? 'table-row' : 'none';
        internacionLugarRow.style.display = checked ? 'table-row' : 'none';
    }
    if (internacionCheck && internacionAnioRow && internacionLugarRow) {
        internacionCheck.addEventListener('change', toggleInternacion);
        toggleInternacion();
    }
});




document.addEventListener('DOMContentLoaded', function() {
    var patrullajeActivo = document.getElementById('id_patrullaje_activo');
    var patrullajeCampos = document.querySelectorAll('.patrullaje-campos');
    function togglePatrullajeCampos() {
        patrullajeCampos.forEach(function(row) {
            row.style.display = patrullajeActivo && patrullajeActivo.checked ? '' : 'none';
        });
    }
    if (patrullajeActivo) {
        patrullajeActivo.addEventListener('change', togglePatrullajeCampos);
        togglePatrullajeCampos();
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const fechaNacimiento = document.getElementById('id_fecha_nacimiento');
    const rangoEtareoSelectWrapper = document.getElementById('rango-etareo-select-wrapper');
    const rangoEtareoSelect = document.querySelector('.select-rango-etareo');
    const rangoEtareoReadonlyWrapper = document.getElementById('rango-etareo-readonly-wrapper');
    const rangoEtareoReadonly = document.getElementById('rango-etareo-readonly');

    function obtenerTextoSeleccionado(selectElement) {
        if (!selectElement) return '';
        const selectedOption = selectElement.options[selectElement.selectedIndex];
        return selectedOption ? selectedOption.text : '';
    }

    function toggleRangoEtareo() {
        if (fechaNacimiento && fechaNacimiento.value) {
            // Oculta el select y muestra el readonly
            if (rangoEtareoSelectWrapper) rangoEtareoSelectWrapper.style.display = 'none';
            if (rangoEtareoReadonlyWrapper) rangoEtareoReadonlyWrapper.style.display = '';
            if (rangoEtareoSelect) rangoEtareoSelect.setAttribute('disabled', 'disabled');
            if (rangoEtareoReadonly) {
                // Mostrar el texto del rango etáreo actualmente seleccionado
                rangoEtareoReadonly.value = obtenerTextoSeleccionado(rangoEtareoSelect);
            }
        } else {
            // Muestra el select editable y oculta el campo readonly
            if (rangoEtareoSelectWrapper) rangoEtareoSelectWrapper.style.display = '';
            if (rangoEtareoReadonlyWrapper) rangoEtareoReadonlyWrapper.style.display = 'none';
            if (rangoEtareoSelect) rangoEtareoSelect.removeAttribute('disabled');
        }
    }

    if (fechaNacimiento) {
        fechaNacimiento.addEventListener('change', toggleRangoEtareo);
        // Ejecutar también al cargar
        toggleRangoEtareo();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const generoSelect = document.querySelector('.select-genero');
    const generoOtroCampo = document.getElementById('genero-otro-campo');
    if (generoSelect && generoOtroCampo) {
        function toggleGeneroOtro() {
            // Usa el valor "OTRO" porque así está en tu modelo
            generoOtroCampo.style.display = (generoSelect.value === 'OTRO') ? 'block' : 'none';
        }
        generoSelect.addEventListener('change', toggleGeneroOtro);
        toggleGeneroOtro();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Inicializa select2 si no está inicializado
    $('.select2').select2({
        width: '100%',
        placeholder: 'Seleccione o busque nacionalidad',
        allowClear: true
    });

    function toggleNacionalidadOtro() {
        // El valor puede ser null, "" o "Otro"
        var val = $('#id_nacionalidad').val();
        if (val && val.toLowerCase() === 'otro') {
            $('#nacionalidad-otro-campo').show();
        } else {
            $('#nacionalidad-otro-campo').hide();
            $('#id_nacionalidad_otro').val('');
        }
    }

    // Usar ambos eventos para asegurar compatibilidad con select2 y selects normales
    $('#id_nacionalidad').on('change.select2 change', toggleNacionalidadOtro);
    toggleNacionalidadOtro(); // Ejecutar al cargar
});

document.addEventListener('DOMContentLoaded', function() {
    const cesfamSelect = document.getElementById('id_cesfam');
    const cesfamOtroCampo = document.getElementById('cesfam-otro-campo');
    function toggleCesfamOtro() {
        if (cesfamSelect && cesfamOtroCampo) {
            cesfamOtroCampo.style.display = (cesfamSelect.value === 'OTRO') ? 'block' : 'none';
            // Limpia el campo si se cambia a otra opción
            if (cesfamSelect.value !== 'OTRO') {
                const input = cesfamOtroCampo.querySelector('input, textarea');
                if (input) input.value = '';
            }
        }
    }
    if (cesfamSelect && cesfamOtroCampo) {
        cesfamSelect.addEventListener('change', toggleCesfamOtro);
        toggleCesfamOtro(); // Estado inicial
    }
});
