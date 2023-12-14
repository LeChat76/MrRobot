// Fonction pour déverrouiller la liste déroulante
function deverrouillerListe() {
    var troisPremiersOctets = document.getElementById("first_tree_bytes").value;

    // Deverrouille la liste des masque si la valeur entrée est conforme (ex: 192.168.10)
    var pattern = /^(25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9]?)\.(25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9]?)\.(25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9][0-9]?[0-9]?)$/;

    if (pattern.test(troisPremiersOctets)) {
        // si la valeur est conforme, dévérrouillage de la liste
        document.getElementById("networks_masks").removeAttribute("disabled");
    } else {
        // Sinon verrouillage
        document.getElementById("networks_masks").setAttribute("disabled", "disabled");
    }
}

// gestionnaire d'événements à chaque changement de valeur des 3 premiers octets
document.getElementById("first_tree_bytes").addEventListener("input", deverrouillerListe);


// Fonction pour afficher le nombre d'hôtes dispo en foncton du mask selectionné
function afficherNbHotes() {
    var networksMasksSelect = document.getElementById("networks_masks");
    var nbHostsDisplay = document.getElementById("nb_hosts_display");

    // Récupération la valeur associée au mask selectionné
    var nbHostsValue = networksMasksSelect.options[networksMasksSelect.selectedIndex].getAttribute("data-nb-hosts");

    // Mise à jour de la valeur dans la page
    nbHostsDisplay.textContent = "Nombre d'hôtes disponibles : " + nbHostsValue + " .";
}

// gestionnaire d'événements des la selection du mask
document.getElementById("networks_masks").addEventListener("change", afficherNbHotes);