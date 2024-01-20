const networksMasksSelect = document.getElementById("networks_masks");
const jolisTraits = document.getElementsByClassName("joliTrait");
const nbHostsDisplay = document.getElementById("nb_hosts_display");
const networkTitle = document.getElementById("networkTitle");
const radioButtonContainer = document.getElementById("radioButtonContainer");
const vlanTitle = document.getElementById("vlanTitle");
const vlansList = document.getElementById("vlansList");
const addBtn = document.getElementById("addBtn");
const nbHostsValueInput = document.getElementById("nb_hosts_value");
const firstThreeBytesLabel = document.getElementById("first_three_bytes_label");
const firstThreeBytesInput = document.getElementById("first_three_bytes");
const vlanAvailabilityDiv = document.getElementById("vlanAvailability")

const noNetworkMessageDiv = document.getElementById("noNetworkMessage");

// Fonction pour déverrouiller la liste déroulante
function deverrouillerListe() {
    let firstThreeBytes = document.getElementById("first_three_bytes").value;

    networksMasksSelect.selectedIndex = 0;
    nbHostsDisplay.textContent = "";
    for (var i = 0; i < jolisTraits.length; i++) {
        jolisTraits[i].style.display = "none";
    }
    networkTitle.style.display = "none";
    noNetworkMessageDiv.style.display = "none";
    radioButtonContainer.style.display = "none";
    vlanTitle.style.display = "none";
    vlansList.style.display = "none";
    vlansList.selectedIndex = "0";
    addBtn.style.display = "none";

    // Deverrouille la liste des masque si la valeur entrée est conforme (ex: 192.168.10)
    let pattern = /^(25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9]?)\.(25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9]?)\.(25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9][0-9]?[0-9]?)$/;
    console.log("TOP")
    if (pattern.test(firstThreeBytes)) {
        // si la valeur est conforme, dévérrouillage de la liste
        document.getElementById("networks_masks").removeAttribute("disabled");
    } else {
        // Sinon verrouillage
        document.getElementById("networks_masks").setAttribute("disabled", "disabled");
    }
}

// Fonction pour afficher le nombre d'hôtes dispo en foncton du mask selectionné
// plus liste des réseaux disponibles
async function selectRange() {
    const firstThreeBytes = document.getElementById("first_three_bytes").value;
    let current4thByte = 0;
    let networkList = [];
    let networkFirstByteList = [];
    let networkLastByteList = [];
    let networkFirstByte = 0;
    let nbHostsValue = parseInt(networksMasksSelect.options[networksMasksSelect.selectedIndex].getAttribute("data-nb-hosts")) + 2;
    let networkLastByte = parseInt(nbHostsValue) - 1

    // Mise à jour de la valeur dans la page
    nbHostsDisplay.textContent = "Nombre d'hôtes disponibles pour le masque selectionné : " + String(parseInt(nbHostsValue) - 2) + ".";
    nbHostsValueInput.value = nbHostsValue

    while (current4thByte <= 254) {
        let networkRangeAvailable = await checkIpInDb(firstThreeBytes, networkFirstByte, networkLastByte)
        console.log("networkRangeAvailable :", networkRangeAvailable);
        if (!networkRangeAvailable) {
            let networkRange = firstThreeBytes + "." + String(current4thByte) + " => " + firstThreeBytes + "." + String(current4thByte + nbHostsValue- 1);
            networkList.push(networkRange);
            networkFirstByteList.push(current4thByte);
            networkLastByteList.push(current4thByte + nbHostsValue - 1)          
        }
        current4thByte = current4thByte + nbHostsValue
        networkFirstByte = current4thByte
        networkLastByte = current4thByte + nbHostsValue - 1
    }

    if (networkList.length >0)  {
        for (var i = 0; i < jolisTraits.length; i++) {
            jolisTraits[i].style.display = "block";
        }
        networkTitle.style.display = "block";
        radioButtonContainer.style.display = "block";
        noNetworkMessageDiv.style.display = "none";
    
        // Vérifie si le conteneur existe avant de tenter de le vider
        if (radioButtonContainer) {
            radioButtonContainer.innerHTML = ""; // Cela supprime tous les éléments enfants du conteneur
        }
    
        networkList.forEach(function(network, index) {
            let label = document.createElement("label");
            let input = document.createElement("input");
            input.type = "radio";
            input.name = "networkRange"
            input.value = networkFirstByteList[index];
    
            label.appendChild(input);
            label.appendChild(document.createTextNode(" " + network));
            label.appendChild(document.createElement("br"));
            radioButtonContainer.appendChild(label);
        });
    } else {
        // Cache la balise <div id="noNetworkMessage">
        noNetworkMessageDiv.style.display = "block";
        networkTitle.style.display = "none";
        radioButtonContainer.style.display = "none";
        for (var i = 0; i < jolisTraits.length; i++) {
            jolisTraits[i].style.display = "none";
        }
    }
}

// fonction qui vérifie si les range d'IP contiennent des IP déjà allouée
async function checkIpInDb(firstThreeBytes, networkFirstByte, networkLastByte) {
    const url = `/network/checkIpInDb/?firstThreeBytes=${firstThreeBytes}&networkFirstByte=${networkFirstByte}&networkLastByte=${networkLastByte}`;

    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur de réseau');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            return data && data.ip_exists ? true : false;
        })
        .catch(error => {
            console.error('Erreur:', error);
            return false;
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

function noVlansAvailable() {
    firstThreeBytesInput.style.display = "none";
    firstThreeBytesLabel.style.display = "none";
    networksMasksSelect.style.display = "none";
}

// gestionnaire d'événement à chaque changement de valeur des 3 premiers octets
document.getElementById("first_three_bytes").addEventListener("input", deverrouillerListe);

// gestionnaire d'événement des la selection du mask
document.getElementById("networks_masks").addEventListener("change", selectRange);

//gestionnaire d'évènement des la selection d'un reseau
document.getElementById("radioButtonContainer").addEventListener("change", afficherVlans);

// gestionnaire d'évènement des la selection du vlan
document.getElementById("vlansList").addEventListener("change", afficherAddBtn);

// gestionnaire d'ouverture de page
document.addEventListener("DOMContentLoaded", function() {
    var vlanAvailability = document.getElementById('vlanAvailability');
    if (vlanAvailability) {
        noVlansAvailable();
    }
});
