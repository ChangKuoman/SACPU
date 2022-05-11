// function for form_motherboard form
document.getElementById('form_motherboard').onsubmit = function(e) {
    e.preventDefault();
    const motherboard_id = document.getElementById('motherboard_id').value;

    const motherboard_name = document.getElementById('motherboard_name').value;
    const motherboard_price = document.getElementById('motherboard_price').value;
    const motherboard_description = document.getElementById('motherboard_description').value;

    fetch('/admin/update/motherboard', {
        method: 'POST',
        body: JSON.stringify({
            'motherboard_id': motherboard_id,
            'motherboard_name': motherboard_name,
            'motherboard_price': motherboard_price,
            'motherboard_description': motherboard_description
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(
        response => response.json()
    ).then(function(jsonResponse){
        
        if (jsonResponse['error']){
            // when is an error
            window.location.href = '/errors/500';
        }
        else if (! jsonResponse['invalid_register']){
            // when deleted is successful
            alert("MOTHERBOARD UPDATED SUCCESSFULLY");
            document.getElementById('form_motherboard').reset();

            // update name from motherboard form IF changed
            if (jsonResponse['child_name'] !== undefined){
                document.getElementById(jsonResponse['child_id']).innerHTML = String(jsonResponse['child_name']);
            }
        
        }
        else {
            // when deleted is NOT successful
            document.getElementById('error_text').textContent = String(jsonResponse['invalid_register']);
            document.getElementById('error').className = '';
        }
        
    }).catch(function() {
        console.log('error admin update motherboard');
    });
}
// function for on change error
document.getElementById('form_motherboard').onchange = function(e){
//    document.getElementById('error').className = 'hidden';
}

// function for form_component form
document.getElementById('form_component').onsubmit = function(e) {
    e.preventDefault();
    const component_id = document.getElementById('component_id').value;

    const component_name = document.getElementById('component_name').value;
    const component_price = document.getElementById('component_price').value;
    const component_description = document.getElementById('component_description').value;
    const component_type = document.getElementById('component_type').value;

    fetch('/admin/update/component', {
        method: 'POST',
        body: JSON.stringify({
            'component_id': component_id,
            'component_name': component_name,
            'component_price': component_price,
            'component_description': component_description,
            'component_type': component_type
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(
        response => response.json()
    ).then(function(jsonResponse){
        
        if (jsonResponse['error']){
            // when is an error
            window.location.href = '/errors/500';
        }
        else if (! jsonResponse['invalid_register']){
            // when deleted is successful
            alert("COMPONENT UPDATED SUCCESSFULLY");
            document.getElementById('form_component').reset();

            // update name from component form IF changed
            if (jsonResponse['child_name'] !== undefined){
                document.getElementById(jsonResponse['child_id']).innerHTML = String(jsonResponse['child_name']);
            }
        
        }
        else {
            // when deleted is NOT successful
            document.getElementById('error_text').textContent = String(jsonResponse['invalid_register']);
            document.getElementById('error').className = '';
        }
        
    }).catch(function() {
        console.log('error admin update component');
    });
}
// function for on change error
document.getElementById('form_component').onchange = function(e){
//    document.getElementById('error').className = 'hidden';
}