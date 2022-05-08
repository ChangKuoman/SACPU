document.getElementById('form').onsubmit = function(e) {
    e.preventDefault();
    var ele = document.getElementsByName('motherboard');
    console.log(ele);
    for(i = 0; i < ele.length; i++) {
        if(ele[i].checked){
            fetch('/simulator/motherboard', {
                method: 'POST',
                body: JSON.stringify({
                    'motherboard': ele[i].value
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
                else {
                    // when motherboard is successful
                    window.location.href = '/simulator/' + String(jsonResponse['motherboard'])
                }

            }).catch(function() {
                console.log('error_choose_motherboard')
            });
            break;
        }
    }
}