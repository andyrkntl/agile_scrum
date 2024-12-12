document.addEventListener('DOMContentLoaded', function () {
    // Initialize the carousel
    var myCarousel = document.querySelector('#eventCarousel')
    var carousel = new bootstrap.Carousel(myCarousel, {
        interval: 3000, // Change slide every 3 seconds
        wrap: true // Continuously loop
    })

    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

