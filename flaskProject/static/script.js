document.getElementById('geneticForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = {
        longitud_binaria: document.getElementById('longitud_binaria').value,
        min_max: document.getElementById('min_max').value,
        porcentaje_cruce: document.getElementById('porcentaje_cruce').value,
        tipo_cruce: document.getElementById('tipo_cruce').value,
        porcentaje_mutacion: document.getElementById('porcentaje_mutacion').value,
        funcion_adaptacion: document.getElementById('funcion_adaptacion').value,
    };

    try {
        const response = await fetch('/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData),
        });

        const result = await response.json();
        if (response.ok) {
            document.getElementById('resultMessage').textContent = result.message;
            showModal();
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

function showModal() {
    const modal = document.getElementById('resultModal');
    const closeBtn = document.querySelector('.modal .close');

    modal.style.display = 'block';

    closeBtn.onclick = function () {
        modal.style.display = 'none';
    };

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };
}
