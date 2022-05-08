const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
document.getElementById('form').onsubmit = function(e) {

    e.preventDefault();
    const username = usernameInput.value;
    const password = passwordInput.value;
    fetch('/login/enter', {
        method: 'POST',
        body: JSON.stringify({
            'username': username,
            'password': password
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(
        response => response.json()
    ).then(function(jsonResponse){
        if (jsonResponse['error']){
            // when is an error
            window.location.href = '/errors/500'
        }
        else if (jsonResponse['invalid_login']){
            // when login is NOT successful
            document.getElementById('error').className = '';
        }
        else {
            // when login is successful
            window.location.href = '/simulator'
        }
    }).catch(function() {
        console.log('error_login')
    });
}

document.getElementById('form').onchange = function(e){
    document.getElementById('error').className = 'hidden';
}