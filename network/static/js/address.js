const joliTrait = document.getElementsByClassName("joliTrait")[0];
const addressTable = document.getElementsByClassName("address-table")[0];

async function afficherAdresses(vlan_id) {
    joliTrait.style.display = "block";
    addressTable.style.display = "block";
    const url = `getNetworkAddresses/?vlan_id=${vlan_id}`;
    var tableBody = document.getElementById("networkAddressesTableBody");

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("DATA :", data)
            // Supprimer contenu de la table
            tableBody.innerHTML = "";

            // Ajout des adresses IP à la table
            data.forEach(address => {
                var row = document.createElement("tr");
                row.innerHTML = `<td class="address-ip-value">${address.ip}</td>
                                    <td>${address.hostname || ''}</td>
                                    <td>${address.description || ''}</td>`;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Erreur lors de la récupération des adresses IP:', error));
}

// gestionnaire d'évènement des la selection du vlan
document.getElementById("vlansList").addEventListener("change", function () {
    var selectedVlanId = this.value;
    if (selectedVlanId) {
        afficherAdresses(selectedVlanId);
    }
});

