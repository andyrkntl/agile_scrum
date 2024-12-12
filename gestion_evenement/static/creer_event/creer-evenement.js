
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('event-form');
    const imageInput = document.getElementById('event-image');
    const imageContainer = document.getElementById('image-container');
    const addDateBtn = document.getElementById('add-date-btn');

    imageInput.addEventListener('change', function (e) {
        for (let file of e.target.files) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.classList.add('img-thumbnail', 'mr-2', 'mb-2');
                img.style.width = '100px';
                img.style.height = '100px';
                img.style.objectFit = 'cover';
                imageContainer.appendChild(img);
            }
            reader.readAsDataURL(file);
        }
    });

    addDateBtn.addEventListener('click', function () {
        const dateInput = document.createElement('input');
        dateInput.type = 'date';
        dateInput.classList.add('form-control', 'mt-2');
        dateInput.required = true;
        imageContainer.appendChild(dateInput);
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        // Validation de base
        const title = document.getElementById('event-title').value;
        const startDate = document.getElementById('event-start-date').value;
        const startTime = document.getElementById('event-start-time').value;
        const endDate = document.getElementById('event-end-date').value;
        const endTime = document.getElementById('event-end-time').value;
        const location = document.getElementById('event-location').value;
        const description = document.getElementById('event-description').value;

        if (!title || !startDate || !startTime || !endDate || !endTime || !location || !description) {
            alert('Veuillez remplir tous les champs obligatoires.');
            return;
        }

        // Simuler l'envoi des données à un serveur
        console.log('Événement créé :', {
            title,
            startDate,
            startTime,
            endDate,
            endTime,
            location,
            description,
        });

        // Réinitialiser le formulaire
        form.reset();
        imageContainer.innerHTML = '';

        // Afficher un message de confirmation
        alert('Votre événement a été créé avec succès !');
    });
});

