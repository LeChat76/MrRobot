const joliTrait = document.getElementById("joliTrait");
const addressTable = document.getElementById("address-table");
const ipDispo = document.getElementById("ipDispo");
const modal = document.getElementById("addressModal");
const radios = document.querySelectorAll('input[type="radio"]');
const submitBtn = document.getElementById("submitBtn");
const tableBody = document.getElementById("freeIpAddressesTableBody");
const vlanTitle = document.getElementById("vlanTitle");
const vlansList = document.getElementById("vlansList");
const checkInputServerLabel = document.getElementsByClassName("form-check-label")[0];
const checkInputServer = document.getElementById("pingFromServer");


async function afficherIpDispos(vlan_id) {
    joliTrait.style.display = "block";
    addressTable.style.display = "block";
    ipDispo.style.display = "block";
    const url = `/network/getFreeIpAddresses/?vlan_id=${vlan_id}`;
    var tableBody = document.getElementById("freeIpAddressesTableBody");
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("DATA :", data)
            // Supprimer contenu de la table
            tableBody.innerHTML = "";
            // Ajout des adresses IP non affectées à la table
            data.forEach((address) => {
                var row = document.createElement("tr");
                row.innerHTML = `<td><input type="radio" name="freeIpRadio" value="${address.id}" data-ip="${address.ip}"></td>
                                 <td class="address-ip-value"  onclick="clickRadio(${address.id})">${address.ip}</td>`;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Erreur lors de la récupération des adresses IP:', error));
}

// fonction de modification d'adresse dans la table "address"
async function modifyAddress(addressId, hostname, description) {
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

function closeModal() {
    modal.style.display="none";
}

function clickRadio(buttonId) {
    var buttonRadio = document.querySelector('input[type="radio"][name="freeIpRadio"][value="' + buttonId + '"]');
    buttonRadio.click()
}

function noVlansAvailable() {
    vlanTitle.style.display = "none";
    vlansList.style.display = "none";
}

function activeCheckInputServerLabel() {
    checkInputServer.disabled = false;
    console.log("TOP");
}

// gestionnaire d'événement des qu'on selectionne un vlan
document.getElementById("vlansList").addEventListener("change", function() {
    var selectedVlanId = this.value;
    document.getElementById('selectedVlan').value = selectedVlanId
    if (selectedVlanId) {
        afficherIpDispos(selectedVlanId);
    }
});

// gestionnaire d'evenement sur le tableau qui regroupe les boutons radios
// (il n'est pas possible de créer un gestionnaire d'evenement pour les boutons
// car ils n'existent pas au moment de l'ouverture de la page, ils sont créés
// avec le code JS de la fonction "afficherIpDispos")
addressTable.addEventListener("change", function(event) {
    let selectedIpAddress = '';
    // Récupération de l'élément sur lequel l'événement a été déclenché
    const targetElement = event.target;

    // Vérification si l'élément cliqué est bien un bouton radio
    if (targetElement.tagName === 'INPUT' && targetElement.type === 'radio') {
        selectedIpAddress = targetElement.dataset.ip;
        document.getElementById('addressId').value = targetElement.value;
        document.getElementById('selectedIpAddress').innerText = selectedIpAddress;
        modal.style.display="block";
    }
});
// gestionnaire d'evenement pour fermer le modal si on click sur la page
document.addEventListener('click', function(event) {
    if (event.target === modal) {
      closeModal();
    }
});

// gestionnaire d'evenement permettant de recharger la liste des adresses IP dispos
// après avoir selectionné et renseigné une adresses IP
window.addEventListener('load', function() {
    var selectedVlanId = document.getElementById('vlansList').value;
    document.getElementById('selectedVlan').value = selectedVlanId;
    if (selectedVlanId) {
        afficherIpDispos(selectedVlanId);
    }
});

// gestionnaire d'ouverture de page
document.addEventListener("DOMContentLoaded", function() {
    var vlanAvailability = document.getElementById('vlanAvailability');
    if (vlanAvailability) {
        noVlansAvailable();
    }
});
