function addBedroomField() {
    const container = document.getElementById('bedroomContainer');
    const newBedroom = document.createElement('input');
    newBedroom.type = 'text';
    newBedroom.name = 'bedroom' + (container.children.length / 2 + 1);
    newBedroom.className = 'bedroom-input';
    container.appendChild(newBedroom);
}

document.getElementById('companyNameDropDown').addEventListener('change', function() {
    const selectElement = document.getElementById('id_company_name');
    const selectedIndex = selectElement.selectedIndex;
    const companyName = selectElement.options[selectedIndex].value;

    console.log(companyName)
    const buildingDropdown = document.getElementById('buildingNameDropDown');
    const newBuildingFields = document.getElementById('newBuildingFields');

    if (companyName === 'Other') {
        // Hide building dropdown and show new building fields
        buildingDropdown.style.display = 'none';
        newBuildingFields.style.display = 'block';
    } else {
        // Show building dropdown and hide new building fields
        buildingDropdown.style.display = 'block';
        newBuildingFields.style.display = 'none';

        // Make AJAX request to fetch buildings for the selected company
        fetch('get_buildings/?company_name=' + encodeURIComponent(companyName))
            .then(response => response.json())
            .then(data => {

                buildingDropdown.innerHTML = '<select name="building_name" id="id_building_name">'
                buildingDropdown.innerHTML = '<option value="">Select Building</option>';
                data.forEach(building => {
                    buildingDropdown.innerHTML += `<option value="${building}">${building}</option>`;
                });
                buildingDropdown.innerHTML = '</select>' 
                console.log(data);
            })
            .catch(error => console.error('Error:', error));
    }
});

