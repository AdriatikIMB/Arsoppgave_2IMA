document.addEventListener('DOMContentLoaded', () => {
    // Fyller inn tilgjengelige tider for reservasjoner
    populateTimeSlots();

    const nextButton = document.getElementById('nextButton');

    if (nextButton) {
        nextButton.addEventListener('click', function() {
            if (validateForm()) {
                window.location.href = "/contact"; // Naviger til kontaktinformasjonssiden
            }
        });
    }
});

// Fyller inn tilgjengelige tider for reservasjoner
function populateTimeSlots() {
    const timeSelect = document.getElementById('time');
    const dateInput = document.getElementById('date');
    if (!timeSelect || !dateInput) return;

    // Sett minimums- og maksimumsdato
    const today = new Date();
    const todayString = today.toISOString().split("T")[0];
    dateInput.setAttribute('min', todayString);

    const maxDate = new Date();
    maxDate.setMonth(today.getMonth() + 1);
    dateInput.setAttribute('max', maxDate.toISOString().split("T")[0]);

    // Generer tidspunkter fra 15:30 til 22:00 med 15 minutters intervaller
    let currentTime = new Date();
    currentTime.setHours(15, 30, 0, 0);
    const maxStartTime = new Date();
    maxStartTime.setHours(22, 0, 0);

    while (currentTime <= maxStartTime) {
        const timeOption = document.createElement('option');
        timeOption.value = timeOption.textContent = currentTime.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        });
        timeSelect.appendChild(timeOption);
        currentTime.setMinutes(currentTime.getMinutes() + 15);
    }
}

// Funksjon for å validere skjemaet
function validateForm() {
    const people = document.getElementById('people').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;

    if (people && date && time) {
        return true;
    } else {
        alert("Vennligst fyll ut alle feltene før du går videre.");
        return false;
    }
}


 // Handle form submission and send JSON data to Flask server
 document.getElementById('takeawayForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from reloading the page

    const name = document.getElementById('takeawayName').value;
    const dish = document.getElementById('dish').value;

    const orderData = {
        name: name,
        dish: dish
    };

    // Send the order as a JSON object to the backend
    fetch('/takeaway_orders', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        const responseMessage = document.getElementById('responseMessage');
        if (data.success) {
            responseMessage.innerHTML = 'Bestillingen ble sendt!';
        } else {
            responseMessage.innerHTML = 'Noe gikk galt. Prøv igjen.';
        }
    })
    .catch(error => {
        document.getElementById('responseMessage').innerHTML = 'Feil ved sending av bestilling. Vennligst prøv igjen.';
        console.error('Error:', error);
    });
});