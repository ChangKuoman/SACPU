// function for form_motherboard form
document.getElementById('form_motherboard').onsubmit = function(e) {
    e.preventDefault();
    const id_motherboard = document.getElementById('id_motherboard').value;
    fetch('/admin/delete/motherboard', {
        method: 'POST',
        body: JSON.stringify({
            'id_motherboard': id_motherboard
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
            alert("MOTHERBOARD DELETED SUCCESSFULLY");
            document.getElementById('form_motherboard').reset();

            // eliminate from motherboard form
            document.getElementById('id_motherboard').removeChild(document.getElementById(jsonResponse['child_id']));

            // eliminate from compatible form
            const elements = document.getElementsByClassName(jsonResponse['child_id']);
            while(elements.length > 0){
                elements[0].parentNode.removeChild(elements[0]);
            }
        
        }
        else {
            // when deleted is NOT successful
            document.getElementById('error_text').textContent = String(jsonResponse['invalid_register']);
            document.getElementById('error').className = '';
        }
        
    }).catch(function() {
        console.log('error admin delete motherboard');
    });
}
// function for on change error
document.getElementById('form_motherboard').onchange = function(e){
    document.getElementById('error').className = 'hidden';
}

// function for form_component form
document.getElementById('form_component').onsubmit = function(e) {
    e.preventDefault();
    const id_component = document.getElementById('id_component').value;
    fetch('/admin/delete/component', {
        method: 'POST',
        body: JSON.stringify({
            'id_component': id_component
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
            alert("COMPONENT DELETED SUCCESSFULLY");
            document.getElementById('form_component').reset();

            // eliminate from component form
            document.getElementById('id_component').removeChild(document.getElementById(jsonResponse['child_id']));

            // eliminate from compatible form
            const elements = document.getElementsByClassName(jsonResponse['child_id']);
            while(elements.length > 0){
                elements[0].parentNode.removeChild(elements[0]);
            }
        
        }
        else {
            // when deleted is NOT successful
            document.getElementById('error_text').textContent = String(jsonResponse['invalid_register']);
            document.getElementById('error').className = '';
        }
        
    }).catch(function() {
        console.log('error admin delete component');
    });
}
// function for on change error
document.getElementById('form_component').onchange = function(e){
    document.getElementById('error').className = 'hidden';
}

// function for form_compatible form
document.getElementById('form_compatible').onsubmit = function(e) {
    e.preventDefault();
    const id_compatible = document.getElementById('id_compatible').value;
    fetch('/admin/delete/compatible', {
        method: 'POST',
        body: JSON.stringify({
            'id_compatible': id_compatible
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
            alert("COMPONENT DELETED SUCCESSFULLY");
            document.getElementById('form_compatible').reset();

            // eliminate from compatible form
            document.getElementById('id_compatible').removeChild(document.getElementById(jsonResponse['child_id']));

        }
        else {
            // when deleted is NOT successful
            document.getElementById('error_text').textContent = String(jsonResponse['invalid_register']);
            document.getElementById('error').className = '';
        }
        
    }).catch(function() {
        console.log('error admin delete compatible')
    });
}
// function for on change error
document.getElementById('form_compatible').onchange = function(e){
    document.getElementById('error').className = 'hidden';
}