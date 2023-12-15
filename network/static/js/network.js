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

// Fonction pour afficher le nombre d'hôtes dispo en foncton du mask selectionné
// plus liste des réseaux disponibles
function afficherNbHotes() {
    var firstTreeBytes = document.getElementById("first_tree_bytes").value;
    var networksMasksSelect = document.getElementById("networks_masks");
    var nbHostsDisplay = document.getElementById("nb_hosts_display");
    var jolisTraits = document.getElementsByClassName("joliTrait")
    var networkTitle = document.getElementById("networkTitle");
    var networkList = [];
    var radioButtonContainer = document.getElementById("radioButtonContainer");
    // Récupération la valeur associée au mask selectionné
    var nbHostsValue = networksMasksSelect.options[networksMasksSelect.selectedIndex].getAttribute("data-nb-hosts");
   
    // Mise à jour de la valeur dans la page
    nbHostsDisplay.textContent = "Nombre d'hôtes disponibles pour le masque selectionné : " + nbHostsValue + ".";

    // Calcul de la liste des réseau
    current4thByte = parseInt(nbHostsValue) + 2
    networkRange = firstTreeBytes + ".1 => " + firstTreeBytes + "." + String(nbHostsValue);
    networkList.push(networkRange)
    while (current4thByte <= 254) {
        networkRange = firstTreeBytes + "." + String(current4thByte + 1) + " => " + firstTreeBytes + "." + String(current4thByte + parseInt(nbHostsValue))
        current4thByte = current4thByte + parseInt(nbHostsValue) + 2
        networkList.push(networkRange)
    }

    for (var i = 0; i < jolisTraits.length; i++) {
        jolisTraits[i].style.display = "block";
    }
    networkTitle.style.display = "block";
    radioButtonContainer.style.display = "block";

    // Vérifiez si le conteneur existe avant de tenter de le vider
    if (radioButtonContainer) {
        radioButtonContainer.innerHTML = ""; // Cela supprime tous les éléments enfants du conteneur
    }

    networkList.forEach(function(network) {
        var label = document.createElement("label");
        var input = document.createElement("input");
        input.type = "radio";
        input.name = "network";
        input.id = "networkRadBtn"
        input.value = network;

        label.appendChild(input);
        label.appendChild(document.createTextNode(" " + network));
        label.appendChild(document.createElement("br"));
        radioButtonContainer.appendChild(label);
    });
}

function afficherAddBtn() {
    var addBtn = document.getElementById("addBtn");
    addBtn.style.display = "block";
}

function afficherVlans() {
    var vlanTitle = document.getElementById("vlanTitle");
    var vlansList = document.getElementById("vlansList")

    vlanTitle.style.display = "block";
    vlansList.style.display = "block";
}

// gestionnaire d'événement à chaque changement de valeur des 3 premiers octets
document.getElementById("first_tree_bytes").addEventListener("input", deverrouillerListe);

// gestionnaire d'événement des la selection du mask
document.getElementById("networks_masks").addEventListener("change", afficherNbHotes);

//gestionnaire d'évènement des la selection d'un reseau
document.getElementById("radioButtonContainer").addEventListener("change", afficherVlans);

// gestionnaire d'évènement des la selection du vlan
document.getElementById("vlansList").addEventListener("change", afficherAddBtn);
