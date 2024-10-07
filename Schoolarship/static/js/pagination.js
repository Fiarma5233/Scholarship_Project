document.addEventListener("DOMContentLoaded", function() {
    const pages = document.querySelectorAll('.bourses-page');
    let currentPage = 0;

    function showPage(pageIndex) {
        pages.forEach((page, index) => {
            page.style.display = (index === pageIndex) ? 'block' : 'none';
        });
    }

    // Afficher la première page au chargement
    showPage(currentPage);

    // Gestion des boutons de pagination
    document.querySelector('.prev').addEventListener('click', function() {
        if (currentPage > 0) {
            currentPage--;
            showPage(currentPage);
        }
    });

    document.querySelector('.next').addEventListener('click', function() {
        if (currentPage < pages.length - 1) {
            currentPage++;
            showPage(currentPage);
        }
    });
});
