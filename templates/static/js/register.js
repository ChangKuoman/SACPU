const descriptionUsername = document.getElementById("username");
const descriptionPassword = document.getElementById("password");

document.getElementById("form").onsubmit = function(e) {
    e.preventDefault();
    const username = descriptionUsername.value;
    const password = descriptionPassword.value;
    fetch('/register/create', {
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
        console.log('jsonResponse: ', jsonResponse);
    }).catch(function() {
       // document.getElementById('error').className = '';
    });
}

document.getElementById('form').onchange = function(e){
  //  document.getElementById('error').className = 'hidden';
}