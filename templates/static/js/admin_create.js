// function for motherboard form
document.getElementById('form_motherboard').onsubmit = function(e) {
    e.preventDefault();
    const motherboard_name = document.getElementById('motherboard_name').value;
    const motherboard_description = document.getElementById('motherboard_description').value;
    const motherboard_price = document.getElementById('motherboard_price').value;
    fetch('/admin/create/motherboard', {
        method: 'POST',
        body: JSON.stringify({
            'motherboard_name': motherboard_name,
            'motherboard_description': motherboard_description,
            'motherboard_price': motherboard_price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(
        response => response.json()
    ).then(function(jsonResponse){
        console.log(jsonResponse);
        
        if (jsonResponse['error']){
            // when is an error
            window.location.href = '/errors/500';
        }
        else if (! jsonResponse['invalid_register']){
            // when register is successful
            alert("MOTHERBOARD ADDED SUCCESSFULLY");
            document.getElementById('form_motherboard').reset();
        }
        else {
            // when register is NOT successful
            document.getElementById('error_text').textContent = String(jsonResponse['invalid_register']);
            document.getElementById('error').className = '';
        }
        
    }).catch(function() {
        console.log('error_register')
    });
}
// function for on change error
document.getElementById('form_motherboard').onchange = function(e){
    document.getElementById('error').className = 'hidden';
}

// function for form_component form
document.getElementById('form_component').onsubmit = function(e) {
    e.preventDefault();
    const component_name = document.getElementById('component_name').value;
    const component_description = document.getElementById('component_description').value;
    const component_type = document.getElementById('component_type').value;
    const component_price = document.getElementById('component_price').value;
    fetch('/admin/create/component', {
        method: 'POST',
        body: JSON.stringify({
            'component_name': component_name,
            'component_description': component_description,
            'component_type': component_type,
            'component_price': component_price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(
        response => response.json()
    ).then(function(jsonResponse){
        console.log(jsonResponse);
        
        if (jsonResponse['error']){
            // when is an error
            window.location.href = '/errors/500';
        }
        else if (! jsonResponse['invalid_register']){
            // when register is successful
            alert("COMPONENT ADDED SUCCESSFULLY");
            document.getElementById('form_component').reset();
        }
        else {
            // when register is NOT successful
            document.getElementById('error_text').textContent = String(jsonResponse['invalid_register']);
            document.getElementById('error').className = '';
        }
        
    }).catch(function() {
        console.log('error_register')
    });
}
// function for on change error
document.getElementById('form_component').onchange = function(e){
    document.getElementById('error').className = 'hidden';
}

// function for form_component form
document.getElementById('form_compatible').onsubmit = function(e) {
    e.preventDefault();
    const id_motherboard = document.getElementById('id_motherboard').value;
    const id_component = document.getElementById('id_component').value;
    fetch('/admin/create/compatible', {
        method: 'POST',
        body: JSON.stringify({
            'id_motherboard': id_motherboard,
            'id_component': id_component
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(
        response => response.json()
    ).then(function(jsonResponse){
        console.log(jsonResponse);
        
        if (jsonResponse['error']){
            // when is an error
            window.location.href = '/errors/500';
        }
        else if (! jsonResponse['invalid_register']){
            // when register is successful
            alert("COMPATIBLE ADDED SUCCESSFULLY");
            document.getElementById('form_compatible').reset();
        }
        else {
            // when register is NOT successful
            document.getElementById('error_text').textContent = String(jsonResponse['invalid_register']);
            document.getElementById('error').className = '';
        }
        
    }).catch(function() {
        console.log('error_register')
    });
}
// function for on change error
document.getElementById('form_compatible').onchange = function(e){
    document.getElementById('error').className = 'hidden';
}