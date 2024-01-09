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
            data.forEach((address, index) => {
                var row = document.createElement("tr");
                row.innerHTML = `<td class="address-ip-value" style="pointer-events: none; user-select: none;">${address.ip}</td>`
                if (index !== 0 && index !== data.length - 1) {
                    row.innerHTML += `<td contenteditable="true">${address.hostname}</td>
                                        <td contenteditable="true">${address.description}</td>   
                                        <td><form action="{% url 'network:modify_address' ${address.ip} %}" method="post">
                                        <button class="modify-btn" type="submit">Modifier</button>
                                        </form></td>`;
                } else {
                    row.innerHTML += `<td style="pointer-events: none; user-select: none;">${address.hostname}</td>
                                        <td style="pointer-events: none; user-select: none;">${address.description}</td>` 
                };
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

