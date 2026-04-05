// Custom Admin JavaScript for Test Drive Bookings

document.addEventListener('DOMContentLoaded', function() {
    // Function to change text color to yellow
    function makeTextYellow() {
        // Change all links containing "Test Drive Booking" or "Test Drive Bookings"
        const links = document.querySelectorAll('a');
        links.forEach(function(link) {
            if (link.textContent.includes('Test Drive Booking') ||
                link.textContent.includes('Test Drive Bookings')) {
                link.style.color = '#FFD700';
                link.style.fontWeight = 'bold';
            }
        });

        // Change headings containing "Test Drive"
        const headings = document.querySelectorAll('h1, h2, h3');
        headings.forEach(function(heading) {
            if (heading.textContent.includes('Test Drive')) {
                heading.style.color = '#FFD700';
            }
        });

        // Change breadcrumb items
        const breadcrumbs = document.querySelectorAll('.breadcrumb a');
        breadcrumbs.forEach(function(crumb) {
            if (crumb.textContent.includes('Test Drive')) {
                crumb.style.color = '#FFD700';
            }
        });

        // Change module title in admin home
        const moduleTitles = document.querySelectorAll('#app-contacts h2');
        moduleTitles.forEach(function(title) {
            title.style.color = '#FFD700';
        });

        // Change model links in admin home
        const modelLinks = document.querySelectorAll('.model-contact a');
        modelLinks.forEach(function(link) {
            link.style.color = '#FFD700';
            link.style.fontWeight = 'bold';
        });

        // Change content title
        const contentTitle = document.querySelector('.content-title');
        if (contentTitle && contentTitle.textContent.includes('Test Drive')) {
            contentTitle.style.color = '#FFD700';
        }
    }

    // Run on page load
    makeTextYellow();

    // Run again after a short delay to catch dynamically loaded content
    setTimeout(makeTextYellow, 500);
});