document.addEventListener('DOMContentLoaded', function () {
    const nochesInput = document.getElementById('noches');
    const tarifaInput = document.getElementById('tarifa_noche');
    const totalPagarInput = document.getElementById('total_pagar');
    const form = document.getElementById('reserva-form');

    function calcularTotal() {
        const noches = parseInt(nochesInput.value, 10);
        const tarifa = parseFloat(tarifaInput.value);

        if (!isNaN(noches) && !isNaN(tarifa) && noches > 0 && tarifa > 0) {
            const total = noches * tarifa;
            totalPagarInput.value = '$' + total.toFixed(2);
        } else {
            totalPagarInput.value = '';
        }
    }

    nochesInput.addEventListener('input', calcularTotal);
    tarifaInput.addEventListener('input', calcularTotal);

    form.addEventListener('submit', function (event) {
        const nombre = document.getElementById('nombre_huesped').value.trim();
        const noches = nochesInput.value.trim();
        const tarifa = tarifaInput.value.trim();

        if (!nombre || !noches || !tarifa) {
            alert('Todos los campos son obligatorios.');
            event.preventDefault();
            return;
        }

        if (/\d/.test(nombre)) {
            alert('El nombre del huésped no debe contener números.');
            event.preventDefault();
            return;
        }

        const nochesVal = parseInt(noches, 10);
        const tarifaVal = parseFloat(tarifa);

        if (isNaN(nochesVal) || nochesVal <= 0) {
            alert('El número de noches debe ser un número positivo.');
            event.preventDefault();
            return;
        }

        if (isNaN(tarifaVal) || tarifaVal <= 0) {
            alert('La tarifa por noche debe ser un número positivo.');
            event.preventDefault();
            return;
        }
    });

    // Calcular total al cargar la página si hay valores (para el modo de edición)
    calcularTotal();
});
