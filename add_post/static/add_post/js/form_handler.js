function addBedroomField() {
    const container = document.getElementById('bedroomContainer');
    const bedroomNumber = container.querySelectorAll('input').length + 1;

    const newLabel = document.createElement('label')
    newLabel.htmlFor = 'bedroom' + bedroomNumber;
    newLabel.textContent = 'Bedroom ' + bedroomNumber + ':';
    container.appendChild(newLabel)
    
    const newBedroom = document.createElement('input');
    newBedroom.type = 'text';
    newBedroom.id = 'bedroom' + bedroomNumber;
    newBedroom.name = 'bedroom' + bedroomNumber;
    newBedroom.className = 'bedroom-input';
    container.appendChild(newBedroom);
}

document.getElementById('companyNameDropDown').addEventListener('change', function() {
    const selectElement = document.getElementById('id_company_name');
    const selectedIndex = selectElement.selectedIndex;
    const companyName = selectElement.options[selectedIndex].value;

    console.log(companyName)
    const buildingDropdown = document.getElementById('buildingNameDropDown');
    const newCompanyNameFields = document.getElementById('newCompanyName');
    const newBuildingNameFields = document.getElementById('newBuildingName');

    if (companyName === 'Other') {
        // Hide building dropdown and show new building fields
        buildingDropdown.style.display = 'none';
        newCompanyNameFields.style.display = 'block';
        newBuildingNameFields.style.display = 'block';

    } else {
        // Show building dropdown and hide new building fields
        buildingDropdown.style.display = 'block';
        newCompanyNameFields.style.display = 'none';
        newBuildingNameFields.style.display = 'none';


        // Make AJAX request to fetch buildings for the selected company
        fetch('get_buildings/?company_name=' + encodeURIComponent(companyName))
            .then(response => response.json())
            .then(data => {

                let selectHTML = '<select name="building_name" id="id_building_name"> <option value="">Select Building</option> <option value="Other">Other</option>';
                data.forEach(building => {
                    selectHTML += `<option value="${building}">${building}</option>`;
                });
                selectHTML += '</select>'; 
                
                // Set the innerHTML of buildingDropdown to the constructed HTML
                buildingDropdown.innerHTML = selectHTML;
                console.log(data);
            })
            .catch(error => console.error('Error:', error));
    }
});
document.getElementById('buildingNameDropDown').addEventListener('change', function() {
    const selectElement = document.getElementById('id_building_name');
    const selectedIndex = selectElement.selectedIndex;
    const buildingName = selectElement.options[selectedIndex].value;

    console.log("Building name " + buildingName);
    if(buildingName == 'Other'){

        
        
        const newBuildingNameFields = document.getElementById('newBuildingName');

        newBuildingNameFields.style.display = 'block';

    }
});

