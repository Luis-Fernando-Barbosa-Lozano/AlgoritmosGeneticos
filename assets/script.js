// Contador para el número de individuos
let contador = 1;

// Obtener los elementos necesarios
const inputPoblacionMaxima = document.getElementById('cantPoblacional');
const inputIndividuo = document.getElementById('cantGeneraciones');
const botonAgregar = document.querySelector('button[onclick="agregarIndividuo()"]');
const botonAceptar = document.querySelector('button[onclick="limiteIndividuo()"]');


// Función para agregar individuos a la tabla
function agregarIndividuo() {
    const valorIndividuo = inputIndividuo.value;
    const poblacionMaxima = parseInt(inputPoblacionMaxima.value);

    if (valorIndividuo && !isNaN(poblacionMaxima) && contador <= poblacionMaxima) {
        // Obtén la tabla y el cuerpo de la tabla
        const tabla = document.getElementById('tablaResultados').getElementsByTagName('tbody')[0];

        // Crea una nueva fila
        const nuevaFila = tabla.insertRow();

        // Crea celdas para el índice y el valor del individuo
        const celdaIndice = nuevaFila.insertCell(0);
        const celdaIndividuo = nuevaFila.insertCell(1);

        // Asigna los valores a las celdas
        celdaIndice.textContent = contador++;
        celdaIndividuo.textContent = valorIndividuo;

        // Resetea el campo de entrada para un nuevo valor
        inputIndividuo.value = '';

        // Desactivar el botón si se alcanza el límite
        if (contador > poblacionMaxima) {
            botonAgregar.disabled = true;
            botonAgregar.style.display = 'none'; // Oculta el botón de agregar
            botonAceptar.style.display = 'none'; // 
        }
    }
}

// Agregar event listeners para actualizar los botones
inputPoblacionMaxima.addEventListener('input', actualizarBotones);
inputIndividuo.addEventListener('input', actualizarBotones);
