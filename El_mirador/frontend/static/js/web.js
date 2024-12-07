const API_BASE = 'http://localhost:5000';

// Función para cargar departamentos en un select específico
async function cargarDepartamentos(selectElement) {
    try {
        const response = await fetch('http://localhost:5000/departamento/listar');
        const data = await response.json();

        // Validar si el elemento select existe
        if (!selectElement) {
            console.error("El elemento select no existe.");
            return;
        }

        // Limpiar opciones existentes
        selectElement.innerHTML = '<option value="">Selecciona un departamento</option>';

        if (Array.isArray(data)) {
            data.forEach(departamento => {
                const option = document.createElement("option");
                option.value = departamento.cod;
                option.textContent = `Departamento ${departamento.cod}`;
                selectElement.appendChild(option);
            });
        } else {
            alert("Error al cargar los departamentos.");
        }
    } catch (error) {
        console.error("Error al cargar los departamentos:", error);
        alert("Error al cargar los departamentos.");
    }
}

// Función para agregar una nueva fila de departamento en "Generar Gastos"
function addRow() {
    const container = document.getElementById("departamentos-container");

    const row = document.createElement("div");
    row.classList.add("row");

    const select = document.createElement("select");
    select.classList.add("select-departamento");
    select.required = true;

    // Cargar departamentos en el nuevo select
    cargarDepartamentos(select);

    const input = document.createElement("input");
    input.type = "number";
    input.classList.add("monto-departamento");
    input.placeholder = "Monto del gasto";
    input.required = true;

    const button = document.createElement("button");
    button.type = "button";
    button.classList.add("remove-row");
    button.textContent = "X";
    button.onclick = () => removeRow(button);

    row.appendChild(select);
    row.appendChild(input);
    row.appendChild(button);

    container.appendChild(row);
}


// Función para eliminar una fila
function removeRow(button) {
    const row = button.parentElement;
    row.remove();
}


// Ejecutar la carga inicial de departamentos al cargar la página
document.addEventListener("DOMContentLoaded", function () {
    // Cargar departamentos en los selects iniciales
    const generarSelect = document.getElementById("departamentos-generar");
    const pagarSelect = document.getElementById("departamentos-pagar");

    if (generarSelect) cargarDepartamentos(generarSelect);
    if (pagarSelect) cargarDepartamentos(pagarSelect);
});


// Lógica para enviar el formulario de generación de gastos comunes
document.getElementById("form-generar-gastos").addEventListener("submit", function (event) {
    event.preventDefault();

    const anio = document.getElementById("anio").value;
    const mes = document.getElementById("mes").value;

    const monto_departamento = {};

    document.querySelectorAll(".row").forEach(row => {
        const select = row.querySelector(".select-departamento");
        const input = row.querySelector(".monto-departamento");

        if (select.value && input.value) {
            monto_departamento[select.value] = parseFloat(input.value);
        }
    });

    const data = {
        mes: mes ? parseInt(mes) : null,
        anio: parseInt(anio),
        monto_departamento: monto_departamento
    };

    // Enviar datos al backend
    fetch("http://localhost:5000/gastos/generar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
            }
            if (data.registros) {
                const output = document.getElementById("output");
                output.textContent = JSON.stringify(data.registros, null, 2);
            }
        })
        .catch(error => console.error("Error:", error));
});

// Lógica para enviar el formulario de marcar como pagado
document.getElementById("form-marcar-pago").addEventListener("submit", async function (event) {
    event.preventDefault();

    const departamento = document.getElementById("departamentos-pagar").value;
    const mes = document.getElementById("mesapagar").value;
    const anio = document.getElementById("anioapagar").value;
    const fecha_pago = document.getElementById("fecha_pago").value;

    const data = {
        departamento: departamento,
        mes: mes,  // Mes seleccionado
        anio: anio,  // Año seleccionado
        fecha_pago: fecha_pago  // Fecha de pago
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/gastos/pagar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        // Mostrar el resultado en la sección de salida
        const output = document.getElementById("output");
        output.textContent = JSON.stringify(result, null, 2);

        // Mostrar un mensaje en caso de error
        if (!response.ok) {
            output.classList.add("error");
        } else {
            output.classList.remove("error");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Ocurrió un error al procesar el pago.");
    }
});

document.getElementById("form-consultar-gastos").addEventListener("submit", async function(event) {
    event.preventDefault();

    const hasta_mes = document.getElementById("hasta_mes").value;
    const hasta_año = document.getElementById("hasta_año").value;

    // Validar que se seleccionaron los campos
    if (!hasta_mes || !hasta_año) {
        alert("Por favor, completa todos los campos.");
        return;
    }

    const data = {
        hasta_mes: hasta_mes,
        hasta_año: hasta_año
    };

    try {
        const response = await fetch("http://localhost:5000/gastos/pendientes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        const output = document.getElementById("output");
        if (response.ok) {
            output.textContent = JSON.stringify(result, null, 2);
        } else {
            output.textContent = JSON.stringify(result.error, null, 2);
        }
    } catch (error) {
        console.error("Error al consultar los gastos pendientes:", error);
        alert("Ocurrió un error al consultar los gastos.");
    }
});

