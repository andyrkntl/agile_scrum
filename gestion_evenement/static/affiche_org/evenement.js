document.addEventListener('DOMContentLoaded', function () {
    const eventsContainer = document.getElementById('events-container');
    const editForm = document.getElementById('edit-event-form');
    const saveEditBtn = document.getElementById('save-edit-btn');
    const editModal = new bootstrap.Modal(document.getElementById('editEventModal'));

    // Simulons une liste d'événements (à remplacer par une vraie API)
    let events = [
        { id: 1, title: "Concert de jazz", date: "2023-07-15", description: "Un concert de jazz exceptionnel avec des artistes de renommée internationale." },
        { id: 2, title: "Exposition d'art moderne", date: "2023-08-01", description: "Découvrez les œuvres fascinantes d'artistes contemporains." },
        { id: 3, title: "Marathon de la ville", date: "2023-09-10", description: "Participez au marathon annuel de la ville et dépassez vos limites." }
    ];

    function displayEvents() {
        eventsContainer.innerHTML = '';
        events.forEach(event => {
            const eventElement = createEventElement(event);
            eventsContainer.appendChild(eventElement);
        });
    }

    function createEventElement(event) {
        const eventDiv = document.createElement('div');
        eventDiv.className = 'col';
        eventDiv.innerHTML = `
            <div class="card h-100 event-card" data-event-id="${event.id}">
                <div class="card-body">
                    <h5 class="card-title">${event.title}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">${formatDate(event.date)}</h6>
                    <p class="card-text">${event.description}</p>
                </div>
                <div class="card-footer">
                    <button class="btn btn-sm btn-outline-primary edit-btn">
                        <i class="bi bi-pencil"></i> Modifier
                    </button>
                    <button class="btn btn-sm btn-outline-danger delete-btn">
                        <i class="bi bi-trash"></i> Supprimer
                    </button>
                </div>
            </div>
        `;

        eventDiv.querySelector('.edit-btn').addEventListener('click', () => openEditModal(event));
        eventDiv.querySelector('.delete-btn').addEventListener('click', () => deleteEvent(event.id));

        return eventDiv;
    }

    function formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString('fr-FR', options);
    }

    function openEditModal(event) {
        document.getElementById('edit-event-id').value = event.id;
        document.getElementById('edit-event-title').value = event.title;
        document.getElementById('edit-event-date').value = event.date;
        document.getElementById('edit-event-description').value = event.description;
        editModal.show();
    }

    function deleteEvent(eventId) {
        if (confirm('Êtes-vous sûr de vouloir supprimer cet événement ?')) {
            events = events.filter(event => event.id !== eventId);
            displayEvents();
        }
    }

    saveEditBtn.addEventListener('click', function () {
        const eventId = parseInt(document.getElementById('edit-event-id').value);
        const eventIndex = events.findIndex(e => e.id === eventId);

        if (eventIndex !== -1) {
            events[eventIndex] = {
                id: eventId,
                title: document.getElementById('edit-event-title').value,
                date: document.getElementById('edit-event-date').value,
                description: document.getElementById('edit-event-description').value
            };
            displayEvents();
            editModal.hide();
        }
    });

    // Afficher les événements au chargement de la page
    displayEvents();
});

