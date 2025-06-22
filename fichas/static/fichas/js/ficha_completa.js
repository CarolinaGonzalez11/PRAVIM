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
    const radios = document.getElementsByName('ficha-ingreso_efectivo');
    const fechaIngreso = document.getElementById('id_ficha-fecha_ingreso');
    function checkEstado() {
        let valor = null;
        radios.forEach = Array.prototype.forEach; // Para forEach en NodeList en IE
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
document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.getElementById('id_denuncia-tiene_denuncia');
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
    const lugarDenuncia = document.querySelector('select[name$="lugar_denuncia"]');
    const otroLugarCampo = document.getElementById('otro-lugar-campo');
    if (lugarDenuncia && otroLugarCampo) {
        function toggleOtroLugar() {
            otroLugarCampo.style.display = (lugarDenuncia.value === 'OTRO') ? 'block' : 'none';
        }
        lugarDenuncia.addEventListener('change', toggleOtroLugar);
        toggleOtroLugar();
    }

    // Mostrar "otra dificultad"
    const dificultades = document.querySelectorAll('input[name$="dificultades"]');
    const dificultadesOtraCampo = document.getElementById('dificultades-otra-campo');

    if (dificultades.length > 0 && dificultadesOtraCampo) {
        function toggleDificultadOtra() {
            let checked = false;
            dificultades.forEach(input => {
                if (input.value === 'otra' && input.checked) checked = true;
            });
            dificultadesOtraCampo.style.display = checked ? 'block' : 'none';
        }
        dificultades.forEach(input => input.addEventListener('change', toggleDificultadOtra));
        toggleDificultadOtra();
    }


    // Mostrar detalle de medida cautelar solo si es sí
    const medidaCautelar = document.getElementById('id_denuncia-medida_cautelar');
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


document.addEventListener('DOMContentLoaded', function () {
    // Diagnóstico: mostrar "otro" si corresponde
    const diagnostico = document.getElementById('id_psico-diagnostico');
    const diagnosticoOtroRow = document.getElementById('diagnostico-otro-row');
    if (diagnostico && diagnosticoOtroRow) {
        function toggleDiagnosticoOtro() {
            diagnosticoOtroRow.style.display = (diagnostico.value === 'otro') ? '' : 'none';
        }
        diagnostico.addEventListener('change', toggleDiagnosticoOtro);
        toggleDiagnosticoOtro();
    }

    // Atención salud mental: mostrar año y lugar si check
    const atencion = document.getElementById('id_psico-atencion_salud_mental');
    const atencionAnio = document.getElementById('atencion-anio-row');
    const atencionLugar = document.getElementById('atencion-lugar-row');
    if (atencion && atencionAnio && atencionLugar) {
        function toggleAtencionCampos() {
            const checked = atencion.checked;
            atencionAnio.style.display = checked ? '' : 'none';
            atencionLugar.style.display = checked ? '' : 'none';
        }
        atencion.addEventListener('change', toggleAtencionCampos);
        toggleAtencionCampos();
    }

    // Internación: mostrar año y lugar si check
    const internacion = document.getElementById('id_psico-internacion');
    const internacionAnio = document.getElementById('internacion-anio-row');
    const internacionLugar = document.getElementById('internacion-lugar-row');
    if (internacion && internacionAnio && internacionLugar) {
        function toggleInternacionCampos() {
            const checked = internacion.checked;
            internacionAnio.style.display = checked ? '' : 'none';
            internacionLugar.style.display = checked ? '' : 'none';
        }
        internacion.addEventListener('change', toggleInternacionCampos);
        toggleInternacionCampos();
    }
});







document.addEventListener('DOMContentLoaded', function() {
    var patrullajeActivo = document.getElementById('id_plan-patrullaje_activo');
    var patrullajeCampos = document.querySelectorAll('.patrullaje-campos');
    function togglePatrullajeCampos() {
        patrullajeCampos.forEach(function(row) {
            row.style.display = (patrullajeActivo && patrullajeActivo.checked) ? '' : 'none';
        });
    }
    if (patrullajeActivo) {
        patrullajeActivo.addEventListener('change', togglePatrullajeCampos);
        togglePatrullajeCampos();
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const fechaNacimiento = document.getElementById('id_persona-fecha_nacimiento');
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

document.addEventListener('DOMContentLoaded', function() {
    var selectSalud = document.getElementById('id_deriv_salud-dispositivo_salud');
    var rowSaludOtro = document.getElementById('row_salud_otro');
    var inputSaludOtro = document.getElementById('id_deriv_salud-dispositivo_salud_otro');

    function mostrarCampoOtroSalud() {
        if (selectSalud.value === 'OTRO') {
            rowSaludOtro.style.display = '';
            inputSaludOtro.required = true;
        } else {
            rowSaludOtro.style.display = 'none';
            inputSaludOtro.value = '';
            inputSaludOtro.required = false;
        }
    }

    if (selectSalud && rowSaludOtro && inputSaludOtro) {
        selectSalud.addEventListener('change', mostrarCampoOtroSalud);
        // Llama al cargar por si viene con valor
        mostrarCampoOtroSalud();
    }
});


//mapa

let geoBarrios = null, geoCuadrantes = null, geoVillas = null;

// Función para cargar todos los geojson y luego inicializar el mapa y lógica
function cargarGeoJsonsYInit(callback) {
    let cargados = 0;
    fetch('/static/geo/barrios.geojson')
        .then(r => r.json()).then(gj => {
            geoBarrios = gj; cargados++; ready();
        });
    fetch('/static/geo/cuadrantes.geojson')
        .then(r => r.json()).then(gj => {
            geoCuadrantes = gj; cargados++; ready();
        });
    fetch('/static/geo/villas.geojson')
        .then(r => r.json()).then(gj => {
            geoVillas = gj; cargados++; ready();
        });
    function ready() {
        if (cargados === 3 && typeof callback === 'function') callback();
    }
}

// Y luego, en vez de ejecutar directamente la inicialización del mapa, pon:
cargarGeoJsonsYInit(function(){
    // Aquí va toda tu lógica de mapa, setMarkerAndSave, actualizarCamposTerritoriales, etc.
    // Por ejemplo:
    // initMapYFormulario(); // Si tienes una función que inicializa todo
});


const inputDireccion = document.getElementById("direccion-autocompleta");
const inputLat = document.getElementById("id_latitud");
const inputLon = document.getElementById("id_longitud");
const mapaDiv = document.getElementById("mapa-direccion");

const initialLat = -33.5167;  // Maipú
const initialLon = -70.7617;
const initialZoom = 13;

const apiKey = "pk.6ab9d34608e281ef51b917bdf4e46a5f";

// Inicializa mapa centrado en Maipú sin pin
const map = L.map(mapaDiv).setView([initialLat, initialLon], initialZoom);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

let marker = null;

// Función para agregar/mover el pin y guardar lat/lon
function setMarkerAndSave(lat, lon) {
  if (marker) {
    marker.setLatLng([lat, lon]);
  } else {
    marker = L.marker([lat, lon], { draggable: true }).addTo(map);
    marker.on("dragend", function (e) {
      const pos = marker.getLatLng();
      setLatLonInputs(pos.lat, pos.lng);
      // Reverse geocode y actualiza campo dirección
      fetch(`https://us1.locationiq.com/v1/reverse?key=${apiKey}&lat=${pos.lat}&lon=${pos.lng}&format=json&addressdetails=1&normalizeaddress=1&accept-language=es`)
        .then(res => res.json())
        .then(data => {
          if (data.display_name) inputDireccion.value = data.display_name;
        });
    });
  }
  setLatLonInputs(lat, lon);
  map.setView([lat, lon], 17);
}

// Guarda lat/lon en los inputs ocultos
function setLatLonInputs(lat, lon) {
  inputLat.value = lat;
  inputLon.value = lon;
}

// Limpia el pin y los campos lat/lon
function clearMarkerAndLatLon() {
  if (marker) {
    map.removeLayer(marker);
    marker = null;
  }
  inputLat.value = "";
  inputLon.value = "";
}

// AUTOCOMPLETADO: al tipear en dirección, muestra sugerencias y permite seleccionar
let timeoutID;
inputDireccion.addEventListener("input", function () {
  const query = inputDireccion.value.trim();
  // Si está vacío, limpiar pin y lat/lon
  if (!query) {
    clearMarkerAndLatLon();
    return;
  }
  // Delay para no saturar la API
  clearTimeout(timeoutID);
  timeoutID = setTimeout(() => {
    fetch(`https://us1.locationiq.com/v1/search?key=${apiKey}&q=${encodeURIComponent(query)}&format=json&addressdetails=1&limit=5&accept-language=es`)
      .then(res => res.json())
      .then(data => {
        // Quitar sugerencias previas si existen
        let suggestionBox = document.getElementById("autocomplete-suggestions");
        if (suggestionBox) suggestionBox.remove();
        // Si hay resultados, mostrar lista
        if (Array.isArray(data) && data.length > 0) {
          suggestionBox = document.createElement("div");
          suggestionBox.id = "autocomplete-suggestions";
          suggestionBox.style.position = "absolute";
          suggestionBox.style.zIndex = 1000;
          suggestionBox.style.background = "#fff";
          suggestionBox.style.border = "1px solid #ccc";
          suggestionBox.style.width = "100%";
          suggestionBox.style.left = 0;
          suggestionBox.style.top = (inputDireccion.offsetHeight + 2) + "px";
          suggestionBox.style.maxHeight = "160px";
          suggestionBox.style.overflowY = "auto";
          data.forEach((item) => {
            const option = document.createElement("div");
            option.textContent = item.display_name;
            option.style.padding = "6px";
            option.style.cursor = "pointer";
            option.addEventListener("mousedown", function () {
              inputDireccion.value = item.display_name;
              setMarkerAndSave(item.lat, item.lon);
              suggestionBox.remove();
            });
            suggestionBox.appendChild(option);
          });
          inputDireccion.parentElement.appendChild(suggestionBox);
        }
      });
  }, 400); // 400ms debounce
});

// Si pierde foco, borra sugerencias después de un pequeño delay
inputDireccion.addEventListener("blur", function () {
  setTimeout(() => {
    let suggestionBox = document.getElementById("autocomplete-suggestions");
    if (suggestionBox) suggestionBox.remove();
  }, 150);
});

// Si el campo ya tiene coordenadas al editar, carga el pin
if (inputLat.value && inputLon.value) {
  setMarkerAndSave(inputLat.value, inputLon.value);
}

// Si quieres: al limpiar dirección, se borra el pin
inputDireccion.addEventListener("input", function () {
  if (!inputDireccion.value.trim()) clearMarkerAndLatLon();
});

function buscarNombrePoligono(geojson, lat, lon, nombreCampo) {
    if (!geojson) return "";
    const pt = turf.point([parseFloat(lon), parseFloat(lat)]);
    for (let feature of geojson.features) {
        if (turf.booleanPointInPolygon(pt, feature)) {
            return feature.properties[nombreCampo];
        }
    }
    return "";
}

function autoCompletarCamposGeo(lat, lon) {
    // Espera si aún no han cargado
    if (!geoBarrios || !geoCuadrantes || !geoVillas) {
        setTimeout(() => autoCompletarCamposGeo(lat, lon), 350);
        return;
    }
    const barrio = buscarNombrePoligono(geoBarrios, lat, lon, "BARRIO");
    const cuadrante = buscarNombrePoligono(geoCuadrantes, lat, lon, "NUM_CUAD");
    const villa = buscarNombrePoligono(geoVillas, lat, lon, "NOMBRE_LOT");

    // ¡¡Corrige aquí los IDs!!
    if (document.getElementById("id_persona-barrio")) document.getElementById("id_persona-barrio").value = barrio || "";
    if (document.getElementById("id_persona-cuadrante")) document.getElementById("id_persona-cuadrante").value = cuadrante || "";
    if (document.getElementById("id_persona-villa")) document.getElementById("id_persona-villa").value = villa || "";
}

function setMarkerAndSave(lat, lon) {
  if (marker) {
    marker.setLatLng([lat, lon]);
  } else {
    marker = L.marker([lat, lon], { draggable: true }).addTo(map);
    marker.on("dragend", function (e) {
      const pos = marker.getLatLng();
      setLatLonInputs(pos.lat, pos.lng);
      // Reverse geocode y actualiza campo dirección
      fetch(`https://us1.locationiq.com/v1/reverse?key=${apiKey}&lat=${pos.lat}&lon=${pos.lng}&format=json&addressdetails=1&normalizeaddress=1&accept-language=es`)
        .then(res => res.json())
        .then(data => {
          if (data.display_name) inputDireccion.value = data.display_name;
        });
      autoCompletarCamposGeo(pos.lat, pos.lng);   // <--- AGREGA ESTA LÍNEA
    });
  }
  setLatLonInputs(lat, lon);
  map.setView([lat, lon], 17);
  autoCompletarCamposGeo(lat, lon);   // <--- AGREGA ESTA LÍNEA
}

