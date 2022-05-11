// PARA PERIFERICOS
const peripherals = document.getElementsByName('peripherals');
for (i = 0; i < peripherals.length; i++){
    const peripheral = peripherals[i];
    peripheral.onchange = function(e){
        const change = e.target.checked;
        const name = e.target.dataset['name'];
        const price = e.target.dataset['price'];
        if (change === true){
            // append child
            let li = document.createElement('li');
            li.setAttribute('name', name);
            li.innerHTML = String(name) + " " + String(price);
            document.getElementById('shopping_items').appendChild(li);
            // anadir de precio
            total_price =  document.getElementById('total_price').innerHTML;
            total_price = (parseFloat(total_price) + parseFloat(price)).toFixed(2);
            document.getElementById('total_price').innerHTML = total_price;
        }
        else if (change === false){
            // remove child
            const elem = document.getElementsByName(name);
            document.getElementById('shopping_items').removeChild(elem[0]);
            // quitar de precio
            total_price =  document.getElementById('total_price').innerHTML;
            total_price = (parseFloat(total_price) - parseFloat(price)).toFixed(2);
            document.getElementById('total_price').innerHTML = total_price;
        }
    }
}

// PARA RADIO INPUT
const psu_list = document.getElementsByName('psu');
const cpu_list = document.getElementsByName('cpu');
const hdd_list = document.getElementsByName('hdd');
const ram_list = document.getElementsByName('ram');
const ssd_list = document.getElementsByName('ssd');
const gpu_list = document.getElementsByName('gpu');
const pc_cooling_list = document.getElementsByName('pc_cooling');

var elements = 
    Array.from(psu_list)
    .concat(Array.from(cpu_list))
    .concat(Array.from(hdd_list))
    .concat(Array.from(ram_list))
    .concat(Array.from(ssd_list))
    .concat(Array.from(gpu_list))
    .concat(Array.from(pc_cooling_list));

for (i = 0; i < elements.length; i++){
const item = elements[i];

    item.onchange = function(e){

        const change = e.target.checked;
        const name = e.target.dataset['name'];
        const price = e.target.dataset['price'];
        if (change === true){
            // append child
            let li = document.createElement('li');
            li.setAttribute('name', name);
            li.innerHTML = String(name) + " " + String(price);
            document.getElementById('shopping_items').appendChild(li);
            // anadir de precio
            total_price =  document.getElementById('total_price').innerHTML;
            total_price = (parseFloat(total_price) + parseFloat(price)).toFixed(2);
            document.getElementById('total_price').innerHTML = total_price;
        }

        // after this iterate again and chase the one has changed
        for (i = 0; i<elements.length; i++){
            const item2 = elements[i];
            const list = document.getElementsByName(item2.dataset.name);
            if (list.length > 0 && item2.checked === false){
                const price = item2.dataset.price;
                // remove child
                document.getElementById('shopping_items').removeChild(list[0]);
                // quitar de precio
                total_price =  document.getElementById('total_price').innerHTML;
                total_price = (parseFloat(total_price) - parseFloat(price)).toFixed(2);
                document.getElementById('total_price').innerHTML = total_price;
            }
        }
    }
}
