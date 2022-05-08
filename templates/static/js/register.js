const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const password_checkInput = document.getElementById('password_check');
document.getElementById('form').onsubmit = function(e) {
    e.preventDefault();
    const username = usernameInput.value;
    const password = passwordInput.value;
    const password_check = password_checkInput.value;
    fetch('/register/create', {
        method: 'POST',
        body: JSON.stringify({
            'username': username,
            'password': password,
            'password_check': password_check
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(
        response => response.json()
    ).then(function(jsonResponse){
        console.log(jsonResponse);
        
        if (jsonResponse['error']){
            console.log('1');
            // when is an error
            window.location.href = '/errors/500'
        }
        else if (! jsonResponse['invalid_register']){
            console.log('2');
            // when register is successful
            window.location.href = '/login';
        }
        else {
            console.log('3');
            // when register is NOT successful
            document.getElementById('error_text').textContent = String(jsonResponse['invalid_register']);
            document.getElementById('error').className = '';
        }
        
    }).catch(function() {
        console.log('error_register')
    });
}

document.getElementById('form').onchange = function(e){
    document.getElementById('error').className = 'hidden';
}