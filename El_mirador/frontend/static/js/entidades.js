const API_BASE = 'http://localhost:5000';

// Lógica para crear un propietario
document.getElementById("form-propietario").addEventListener("submit", function(event) {
    event.preventDefault();
    let rut = document.getElementById("rut").value;
    let nombre = document.getElementById("nombre-propietario").value;
    let ape_pat = document.getElementById("ape_pat").value;
    let ape_mat = document.getElementById("ape_mat").value;
    let email = document.getElementById("email").value;
    let fono1 = document.getElementById("fono1").value;
    let fono2 = document.getElementById("fono2").value;
    let estado = document.getElementById("estado-propietario").value;

    const data = {
        rut: rut,
        nombre: nombre,
        ape_pat: ape_pat,
        ape_mat: ape_mat,
        email: email,
        fono1: fono1,
        fono2: fono2,
        estado: estado
    };

    fetch(`${API_BASE}/propietario/crear`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ocurrió un error en la solicitud');
    });
});


// Lógica para crear un edificio
document.getElementById("form-edificio").addEventListener("submit", function(event) {
    event.preventDefault();

    let nombre = document.getElementById("nombre-edificio").value;
    let direccion = document.getElementById("direccion").value;
    let inmobiliaria = document.getElementById("inmobiliaria").value;
    let estado = document.getElementById("estado-edificio").value;
    let npisos = parseInt(document.getElementById("npisos").value);
    let valor_gasto_comun = parseFloat(document.getElementById("valor_gasto_comun").value);

    const data = {
        nombre: nombre,
        direccion: direccion,
        inmobiliaria: inmobiliaria,
        estado: estado,
        npisos: npisos,
        valor_gasto_comun: valor_gasto_comun
    };

    fetch(`${API_BASE}/edificio/crear`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ocurrió un error en la solicitud');
    });
});

// Función para obtener los edificios y llenar el select
async function cargarEdificios() {
    try {
        const response = await fetch('http://localhost:5000/edificio/listar');
        const data = await response.json();
        console.log(data);
        if (Array.isArray(data)) {
            const select = document.getElementById("cod_edificio");
            data.forEach(edificio => {
                const option = document.createElement("option");
                option.value = edificio.cod;
                option.textContent = edificio.Nombre;
                select.appendChild(option);
            });
        } else {
            alert("Error al cargar los edificios.");
        }
    } catch (error) {
        console.error("Error al cargar los edificios:", error);
        alert("Error al cargar los edificios.");
    }
}

// Ejecutar al cargar la página
document.addEventListener("DOMContentLoaded", cargarEdificios);

// Lógica para crear un departamento
async function enviarFormulario() {
    const formData = new FormData(document.getElementById("formDepartamento"));
    const data = {
        codDepto: (formData.get("piso")+formData.get("numero")),
        cod_edificio: formData.get("cod_edificio"),
        piso: formData.get("piso"),
        numero: formData.get("numero"),
        num_hab: formData.get("num_hab"),
        num_baños: formData.get("num_baños"),
        rut_prop: formData.get("rut_prop"),
        rutarre: formData.get("rutarre")
    };
    
    try {
        console.log("Datos del formulario enviados:", data);
        const response = await fetch("http://localhost:5000/departamento/crear", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        const result = await response.json();
        alert(result.message || result.error);
    } catch (error) {
        console.error("Error al crear el departamento:", error);
        alert("Error al crear el departamento.");
    }
}