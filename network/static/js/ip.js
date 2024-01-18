const joliTrait = document.getElementById("joliTrait");
const addressTable = document.getElementById("address-table");
const ipDispo = document.getElementById("ipDispo");
const modal = document.getElementById("addressModal");
const radios = document.querySelectorAll('input[type="radio"]');
const submitBtn = document.getElementById("submitBtn");
const tableBody = document.getElementById("freeIpAddressesTableBody");

async function afficherProchaineIpDispo(vlan_id) {
    joliTrait.style.display = "block";
    addressTable.style.display = "block";
    ipDispo.style.display = "block";
    const url = `getFreeIpAddresses/?vlan_id=${vlan_id}`;
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
                row.innerHTML = `<td><input type="radio" name="freeIpRadio" value="${address.id}"></td>
                                 <td class="address-ip-value" style="user-select: none;">${address.ip}</td>`
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Erreur lors de la récupération des adresses IP:', error));
}

// gestionnaire d'événement des qu'on selectionne un vlan
document.getElementById("vlansList").addEventListener("change", function() {
    var selectedVlanId = this.value;
    if (selectedVlanId) {
        afficherProchaineIpDispo(selectedVlanId);
    }
});
// gestionnaire d'evenement sur le tableau qui regroupe les boutons radios
// (il n'est pas possible de créer un gestionnaire d'evenement pour les boutons
// car ils n'existent pas au moment de l'ouverture de la page, ils sont créés
// avec le code JS de la fonction "afficherProchaineIpDispo")
addressTable.addEventListener("change", function(event) {
    // Récupération de l'élément sur lequel l'événement a été déclenché
    const targetElement = event.target;

    // Vérification si l'élément cliqué est bien un bouton radio
    if (targetElement.tagName === 'INPUT' && targetElement.type === 'radio') {
        // console.log("Bouton radio sélectionné :", targetElement.value);
        modal.style.display="block";
    }
});
