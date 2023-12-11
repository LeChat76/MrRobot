document.addEventListener('DOMContentLoaded', function () {
    const pawPrintsContainer = document.querySelector('.paw-prints-container');
    const maxPawPrints = 10;
    const pawPrints = [];

    function createPawPrint() {
        if (pawPrints.length >= maxPawPrints) {
            // Supprimer la première empreinte si le nombre maximum est atteint
            const removedPawPrint = pawPrints.shift();
            pawPrintsContainer.removeChild(removedPawPrint);
        }

        const pawPrint = document.createElement('div');
        pawPrint.className = 'paw-print';
        pawPrint.style.width = '0.5cm'; // Ajustez la taille des empreintes
        pawPrint.style.height = '0.5cm';
        pawPrint.style.background = `url('../static/images/fond_chat.png') repeat`;
        pawPrint.style.backgroundSize = '100%';
        pawPrint.style.position = 'absolute';

        // Positionnement aléatoire sur toute la page
        const randomTop = Math.random() * (window.innerHeight - 15) + window.scrollY;
        const randomLeft = Math.random() * window.innerWidth;
        const randomAngle = Math.random() * 360; // Angle de rotation aléatoire

        pawPrint.style.top = `${randomTop}px`; // Utilisation de pixels pour la position verticale
        pawPrint.style.left = `${randomLeft}px`;
        pawPrint.style.transform = `rotate(${randomAngle}deg)`; // Appliquer la rotation
        pawPrint.style.zIndex = '9999'; // Mettre en premier plan

        pawPrints.push(pawPrint);
        pawPrintsContainer.appendChild(pawPrint);

        // Appeler récursivement la fonction pour générer la prochaine empreinte avec un délai aléatoire
        setTimeout(createPawPrint, Math.random() * (7000 - 3000) + 3000); // Délai aléatoire entre 3 et 7 secondes
    }

    // Lancer la première empreinte
    createPawPrint();
});
