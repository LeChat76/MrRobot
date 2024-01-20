const joliTrait = document.getElementsByClassName("joliTrait")[0];
const addressTable = document.getElementById("address-table");
const vlanTitle = document.getElementById("vlanTitle");
const vlansList = document.getElementById("vlansList");


async function afficherAdresses(vlan_id) {
    joliTrait.style.display = "block";
    addressTable.style.display = "block";
    const url = `getNetworkAddresses/?vlan_id=${vlan_id}`;
    var tableBody = document.getElementById("networkAddressesTableBody");

    fetch(url)
        .then(response => response.json())
        .then(data => {
            // console.log("DATA :", data)
            // Supprimer contenu de la table
            tableBody.innerHTML = "";

            // Ajout des adresses IP à la table
            data.forEach((address, index) => {
                var row = document.createElement("tr");
                row.innerHTML = `<td class="address-ip-value" style="pointer-events: none; user-select: none;">${address.ip}</td>`
                if (index !== 0 && index !== data.length - 1) {
                    row.innerHTML += `<td id="hostname_${address.id}" contenteditable="true">${address.hostname}</td>
                                        <td id="description_${address.id}" contenteditable="true">${address.description}</td>   
                                        <button id="modify-btn_${address.id}" type="button">Modifier</button>`;
                } else {
                    row.innerHTML += `<td style="pointer-events: none; user-select: none;">${address.hostname}</td>
                                        <td style="pointer-events: none; user-select: none;">${address.description}</td>` 
                };
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Erreur lors de la récupération des adresses IP:', error));
}

// fonction de modification d'adresse dans la table "address"
function modifyAddress(addressId, hostname, description) {
    const url = `/network/modifyAddress/`;
    const formData = new FormData();
    formData.append("addressId", addressId);
    formData.append("hostname", hostname);
    formData.append("description", description);
    formData.append("csrfmiddlewaretoken", document.getElementsByName('csrfmiddlewaretoken')[0].value);

    return fetch(url, {
        method: "POST",
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erreur de réseau');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        modifyEffect(addressId);
        return true;
    })
    .catch(error => {
        console.error('Erreur:', error);
        return false;
    });
}

function modifyEffect(buttonId) {
    const button = document.getElementById("modify-btn_" + buttonId);

    // Changement de la couleur et du texte du bouton
    button.style.backgroundColor = "#30E230"; // vert
    button.textContent = "Modif. OK!";

    // Retour à la couleur et au texte d'origine après 2,5 sec
    setTimeout(function() {
        button.style.backgroundColor = "#FF5733"; //rouge
        button.textContent = "Modifier";
    }, 2500);
}

function noVlansAvailable() {
    vlanTitle.style.display = "none";
    vlansList.style.display = "none";
}

// gestionnaire d'évènement des la selection du vlan
document.getElementById("vlansList").addEventListener("change", function () {
    var selectedVlanId = this.value;
    if (selectedVlanId) {
        afficherAdresses(selectedVlanId);
    }
});

// gestionnaire d'évenlent quand on click sur un élément de la table d'adresse
document.getElementById("address-table").addEventListener("click", function(event) {
    // vérification si c'est le bouton "modifier" qui est cliqué parmi tous les éléments du tableau
    if (event.target.id && event.target.id.startsWith("modify-btn_")) {
        // récupération de l'ID (dans l'ID du bouton), du hostname et de la description
        var addressId = event.target.id.split("_")[1];
        var hostname = document.getElementById("hostname_" + addressId).textContent;
        var description = document.getElementById("description_" + addressId).textContent;
        modifyAddress(addressId, hostname, description);
    }
});

// gestionnaire d'ouverture de page
document.addEventListener("DOMContentLoaded", function() {
    var vlanAvailability = document.getElementById('vlanAvailability');
    if (vlanAvailability) {
        noVlansAvailable();
    }
});