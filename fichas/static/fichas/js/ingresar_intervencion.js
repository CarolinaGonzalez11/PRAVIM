// === Opciones (puedes reemplazar estas constantes por variables globales si prefieres pasarlas desde el backend) ===

const PROFESIONALES_UAV = [
    "Nathaly Reyes", 
    "Paloma Quinteros", 
    "Gloria Rivera"
];

const OBJETIVOS_INTERVENCION = [
    "Despejar situación actual por medio de entrevista, elevando ficha de acogida.",
    "Vinculación a la red.",
    "Aumentar la sensación de seguridad.",
    "Dar acompañamiento al proceso/Conocer situación actual.",
    "Seguimiento telefónico, según acuerdo.",
    "Psicoeducación.",
    "Cierre del proceso."
];



// =========== Render dinámico de los checkboxes y selects en la fila "nueva intervención" ============

window.addEventListener('DOMContentLoaded', function() {
    // Renderiza los checkboxes de responsables y objetivos
    renderCheckboxes("nueva-intervencion", "responsables", PROFESIONALES_UAV);
    renderCheckboxes("nueva-intervencion", "objetivos", OBJETIVOS_INTERVENCION);
});

// Renderiza checkboxes en la celda correspondiente
function renderCheckboxes(rowId, name, opciones) {
    let fila = document.getElementById(rowId);
    if (!fila) return;
    let celda = fila.querySelector(`td[data-field="${name}"]`);
    if (!celda) return;
    celda.innerHTML = opciones.map(opt => `
        <label style="display:block; margin-bottom:2px;">
            <input type="checkbox" name="${name}" value="${opt}"> ${opt}
        </label>
    `).join('');
}


// ======================== Funciones para obtener datos de la fila =========================

function obtenerDatosDeFila(tr) {
    let datos = {};
    // Recoge todos los valores
    tr.querySelectorAll('input, select').forEach(el => {
        if (el.type === "checkbox") {
            if (!datos[el.name]) datos[el.name] = [];
            if (el.checked) datos[el.name].push(el.value);
        } else {
            datos[el.name] = el.value;
        }
    });

    return datos;
}

// ======================== Agregar nueva intervención =========================

function agregarIntervencion(event) {
    event.preventDefault();
    let fila = document.getElementById('nueva-intervencion');
    let datos = obtenerDatosDeFila(fila);

    // Validación simple
    if (!datos.fecha || !datos.etapa || !datos.tipo_intervencion) {
        alert("Debe ingresar al menos Fecha, Etapa y Tipo de Atención");
        return;
    }

    fetch(AGREGAR_INTERVENCION_URL, { // AGREGAR_INTERVENCION_URL debe estar definida en el template como variable global JS
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN  // CSRF_TOKEN debe estar definido como variable global
        },
        body: JSON.stringify(datos)
    }).then(resp => resp.json())
    .then(data => {
        if (data.success) {
            agregarFilaTabla(data, fila);
            // Limpia todos los campos
            fila.querySelectorAll('input[type="text"], input[type="date"], select').forEach(el => el.value = "");
            fila.querySelectorAll('input[type="checkbox"]').forEach(el => el.checked = false);
        } else {
            alert("Error al guardar intervención: " + (data.error || ""));
        }
    });
}

function agregarFilaTabla(data, fila) {
    let nueva = document.createElement('tr');
    nueva.setAttribute('data-id', data.id);
    nueva.innerHTML = `
        <td>${data.fecha}</td>
        <td>${data.etapa}</td>
        <td>${data.tipo_intervencion}</td>
        <td>${data.responsables || ""}</td>
        <td>${data.participantes || ""}</td>
        <td>${data.lugar_via || ""}</td>
        <td>${data.objetivos || ""}</td>
        <td>${data.descripcion || ""}</td>
        <td>${data.resultados || ""}</td>
        <td><button type="button" class="btn-edit" onclick="editarFila(this)">Editar</button></td>
    `;
    document.getElementById('body-intervenciones').insertBefore(nueva, fila);
}

// ======================== Edición de fila existente =========================

function editarFila(btn) {
    let tr = btn.closest('tr');
    let tds = tr.querySelectorAll('td');
    //solo toma los 10 elementos 
    let valores = Array.from(tds).map(td => td.textContent.trim()).slice(0, 10);

    // Renderiza la fila editable
    tr.innerHTML = `
        <td><input name="fecha" type="date" value="${valores[0]}"></td>
        <td>
            <select name="etapa">
                <option value="Diagnóstico" ${valores[1] === "Diagnóstico" ? "selected" : ""}>Diagnóstico</option>
                <option value="Intervención" ${valores[1] === "Intervención" ? "selected" : ""}>Intervención</option>
                <option value="Preparación Egreso/Egreso" ${valores[1].includes("Egreso") ? "selected" : ""}>Preparación Egreso/Egreso</option>
            </select>
        </td>
        <td>
            <select name="tipo_intervencion">
                <option value="Psicológica" ${valores[2] === "Psicológica" ? "selected" : ""}>Psicológica</option>
                <option value="Social" ${valores[2] === "Social" ? "selected" : ""}>Social</option>
                <option value="Psicosocial" ${valores[2] === "Psicosocial" ? "selected" : ""}>Psicosocial</option>
                <option value="Vinculación con red" ${valores[2] === "Vinculación con red" ? "selected" : ""}>Vinculación con red</option>
                <option value="Otra" ${valores[2] === "Otra" ? "selected" : ""}>Otra</option>
            </select>
        </td>
        <td>${renderCheckboxesHTML('responsables', PROFESIONALES_UAV, valores[3])}</td>
        <td><input name="participantes" type="text" value="${valores[4]}"></td>
        <td>
            <select name="lugar_via">
                <option value="Domicilio" ${valores[5] === "Domicilio" ? "selected" : ""}>Domicilio</option>
                <option value="Otro sitio en terreno" ${valores[5] === "Otro sitio en terreno" ? "selected" : ""}>Otro sitio en terreno</option>
                <option value="Contacto telefónico" ${valores[5] === "Contacto telefónico" ? "selected" : ""}>Contacto telefónico</option>
                <option value="Video llamada" ${valores[5] === "Video llamada" ? "selected" : ""}>Video llamada</option>
                <option value="Dependencias UAV" ${valores[5] === "Dependencias UAV" ? "selected" : ""}>Dependencias UAV</option>
                <option value="Correo, e-mail" ${valores[5] === "Correo, e-mail" ? "selected" : ""}>Correo, e-mail</option>
                <option value="Otro" ${valores[5] === "Otro" ? "selected" : ""}>Otro</option>
            </select>
        </td>
        <td>${renderCheckboxesHTML('objetivos', OBJETIVOS_INTERVENCION, valores[6])}</td>
        <td><input name="descripcion" type="text" value="${valores[7]}"></td>
        <td><input name="resultados" type="text" value="${valores[8]}"></td>
        <td>
            <button class="btn-save" onclick="guardarEdicion(event, this)">Guardar</button>
            <button class="btn-cancel" onclick="cancelarEdicion(event, this, valores)">Descartar</button>
        </td>
    `;
}

// Helpers para checkboxes y select en edición
function renderCheckboxesHTML(name, opciones, seleccionados) {
    let seleccionadosArr = (seleccionados || "").split(',').map(s => s.trim());
    return opciones.map(opt => `
        <label style="display:block; margin-bottom:2px;">
            <input type="checkbox" name="${name}" value="${opt}" ${seleccionadosArr.includes(opt) ? "checked" : ""}> ${opt}
        </label>
    `).join('');
}

// ======================== Guardar edición =========================

function guardarEdicion(event, btn) {
    event.preventDefault();
    let tr = btn.closest('tr');
    let id = tr.getAttribute('data-id');
    let datos = obtenerDatosDeFila(tr);

    fetch(`/fichas/api/intervencion/editar/${id}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        },
        body: JSON.stringify(datos)
    }).then(resp => resp.json())
    .then(data => {
        if (data.success) {
            // Reemplaza la fila por los nuevos valores
            tr.innerHTML = `
                <td>${data.fecha}</td>
                <td>${data.etapa}</td>
                <td>${data.tipo_intervencion}</td>
                <td>${data.responsables || ""}</td>
                <td>${data.participantes || ""}</td>
                <td>${data.lugar_via || ""}</td>
                <td>${data.objetivos || ""}</td>
                <td>${data.descripcion || ""}</td>
                <td>${data.resultados || ""}</td>
                <td><button type="button" class="btn-edit" onclick="editarFila(this)">Editar</button></td>
            `;
        } else {
            alert("Error al actualizar intervención: " + (data.error || ""));
        }
    });
}

// ======================== Cancelar edición =========================

function cancelarEdicion(event, btn, valores) {
    event.preventDefault();
    let tr = btn.closest('tr');
    tr.innerHTML = `
        <td>${valores[0]}</td>
        <td>${valores[1]}</td>
        <td>${valores[2]}</td>
        <td>${valores[3]}</td>
        <td>${valores[4]}</td>
        <td>${valores[5]}</td>
        <td>${valores[6]}</td>
        <td>${valores[7]}</td>
        <td>${valores[8]}</td>
        <td><button type="button" class="btn-edit" onclick="editarFila(this)">Editar</button></td>
    `;
}

function eliminarIntervencion(btn) {
    if (!confirm('¿Seguro que quieres eliminar esta intervención? Esta acción no se puede deshacer.')) return;
    let tr = btn.closest('tr');
    let id = tr.getAttribute('data-id');
    fetch(`/fichas/api/intervencion/eliminar/${id}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        }
    }).then(resp => resp.json())
    .then(data => {
        if (data.success) {
            tr.remove();
        } else {
            alert("No se pudo eliminar: " + (data.error || "Error desconocido"));
        }
    });
}
