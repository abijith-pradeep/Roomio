function addBedroomField() {
    const container = document.getElementById('bedroomContainer');
    const newBedroom = document.createElement('input');
    newBedroom.type = 'text';
    newBedroom.name = 'bedroom' + (container.children.length / 2 + 1);
    newBedroom.className = 'bedroom-input';
    container.appendChild(newBedroom);
}

document.getElementById('companyNameDropDown').addEventListener('change', function() {
    const companyName = this.value;
    console.log("something changed")
    console.log(companyName)
    const newBuildingFields = document.getElementById('newBuildingFields');
    if (companyName === 'Other') {
        newBuildingFields.style.display = 'block';
    } else {
        newBuildingFields.style.display = 'none';
        // Optionally, fetch and update building names here
    }
});