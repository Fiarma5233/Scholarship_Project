

// // Vérifie si l'utilisateur a déjà répondu au popup
// if (!localStorage.getItem('popupShown')) {
//     Swal.fire({
//         title: "Souhaitez-vous recevoir des informations ?",
//         text: "Souhaitez-vous recevoir prochainement des informations sur les nouvelles opportunités disponibles ?",
//         icon: "warning",
//         showCancelButton: true,
//         confirmButtonText: "Oui",
//         cancelButtonText: "Non"
//     }).then((result) => {
//         if (result.isConfirmed) {
//             window.location.href = "/login";
//         } else {
//             localStorage.setItem('popupShown', 'true');
//         }
//     });
// }

// // Vérifier les messages de succès ou d'erreur
// {% if message %}
//     let iconType = "{{ 'success' if not is_error else 'error' }}";
//     let titleColor = "{{ 'green' if not is_error else 'red' }}";  // Couleur selon le type
//     let backgroundColor = "{{ 'lightgreen' if not is_error else 'lightcoral' }}";  // Couleur de fond

//     Swal.fire({
//         title: "{{ message }}",
//         icon: iconType,
//         timer: 2000,
//         timerProgressBar: true,
//         didOpen: () => {
//             Swal.showLoading();
//         },
//         willClose: () => {
//             window.location.href = "/";
//         },
//         customClass: {
//             title: titleColor, // Appliquer la couleur du titre
//             popup: backgroundColor // Appliquer la couleur de fond
//         }
//     });
// {% endif %}



document.addEventListener('DOMContentLoaded', function() {
    // Vérifie si l'utilisateur a déjà répondu au popup
    if (!localStorage.getItem('popupShown')) {
        Swal.fire({
            title: "Souhaitez-vous recevoir des informations ?",
            text: "Souhaitez-vous recevoir prochainement des informations sur les nouvelles opportunités disponibles ?",
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Oui",
            cancelButtonText: "Non"
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = "/login";
            } else {
                localStorage.setItem('popupShown', 'true');
            }
        });
    }

    // Vérifier les messages de succès ou d'erreur
    {% if message %}
        let iconType = "{{ 'success' if not is_error else 'error' }}";
        let titleColor = "{{ 'green' if not is_error else 'red' }}";  // Couleur selon le type
        let backgroundColor = "{{ 'lightgreen' if not is_error else 'lightcoral' }}";  // Couleur de fond

        Swal.fire({
            title: "{{ message }}",
            icon: iconType,
            timer: 2000,
            timerProgressBar: true,
            didOpen: () => {
                Swal.showLoading();
            },
            willClose: () => {
                window.location.href = "/";
            },
            customClass: {
                title: titleColor, // Appliquer la couleur du titre
                popup: backgroundColor // Appliquer la couleur de fond
            }
        });
    {% endif %}
});


// document.addEventListener('DOMContentLoaded', function() {
//     // Vérifie si l'utilisateur a déjà répondu au popup
//     if (!localStorage.getItem('popupShown')) {
//         Swal.fire({
//             title: "Souhaitez-vous recevoir des informations ?",
//             text: "Souhaitez-vous recevoir prochainement des informations sur les nouvelles opportunités disponibles ?",
//             icon: "warning",
//             showCancelButton: true,
//             confirmButtonText: "Oui",
//             cancelButtonText: "Non"
//         }).then((result) => {
//             if (result.isConfirmed) {
//                 window.location.href = "/login";
//             } else {
//                 localStorage.setItem('popupShown', 'true');
//             }
//         });
//     }
// });
