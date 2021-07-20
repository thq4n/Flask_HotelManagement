function checkdate(){
    var datein = new Date(document.getElementById("pick_up_date_in").value);
    var dateout = new Date(document.getElementById("pick_up_date_out").value);
    if (dateout-datein >= 0) {
        document.getElementById("bookingForm").submit()
    }
    else {
        alert("Invalid input!");
    }
}

function checkSamePass(passA, passB, text, button){
    var pass1 = document.getElementById(passA).value
    var pass2 = document.getElementById(passB).value
    console.info(pass1)
    if (pass1.localeCompare(pass2)!=0){
        document.getElementById(text).innerHTML = "Password is not the same!";
        document.getElementById(text).innerHTML.bold()
        document.getElementById(button).style.display = "none";
    }
    else
    {
        document.getElementById(text).innerHTML = "";
        document.getElementById(button).style.display = "block";
    }
}

function checkUsername (username, textbox, button){
    fetch('api/user/checkusername', {
        'method': 'post',
        'body': JSON.stringify({
            'username': username
        }),
        'headers':{
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data['message'])
        if (data['message'] == 1){
            text = document.getElementById(textbox)
            text.innerText = "Username is exist"
            but = document.getElementById(button)
            but.style.display = "none"
        }
        else {
            text = document.getElementById(textbox)
            text.innerText = ""
            but = document.getElementById(button)
            but.style.display = "block"
        }
    })
}

function checkIdCard (idcard, textbox, button){
    fetch('api/user/checkidcard', {
        'method': 'post',
        'body': JSON.stringify({
            'ic': idcard
        }),
        'headers':{
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data['message'])
        if (data['message'] == 1){
            text = document.getElementById(textbox)
            text.innerText = "ID is exist"
            but = document.getElementById(button)
            but.style.display = "none"
        }
        else {
            text = document.getElementById(textbox)
            text.innerText = ""
            but = document.getElementById(button)
            but.style.display = "block"
        }
    })
}

function checkEmail (email, textbox, button){
    fetch('api/user/checkemail', {
        'method': 'post',
        'body': JSON.stringify({
            'email': email
        }),
        'headers':{
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data['message'])
        if (data['message'] == 1){
            text = document.getElementById(textbox)
            text.innerText = "Email is exist"
            but = document.getElementById(button)
            but.style.display = "none"
        }
        else {
            text = document.getElementById(textbox)
            text.innerText = ""
            but = document.getElementById(button)
            but.style.display = "block"
        }
    })
}

function bookRoom (room_id, user_id, datein, dateout){
    if (confirm(`Book this room (${room_id})???`) == true){
        fetch(`api/bookroom/${room_id}`, {
            'method': 'post',
            'body': JSON.stringify({
                'user_id': user_id,
                'datein': datein,
                'dateout': dateout
            }),
            'headers':{
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data['message']){
                alert(data['message'])
                location.reload()
            }
        })
    }
}

function cancleBooking(booking_id){
    if (confirm(`Are you sure?`) == true){
        fetch(`api/booking/cancle`, {
            'method': 'post',
            'body': JSON.stringify({
                'booking_id': booking_id
            }),
            'headers':{
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data['message']){
                alert(data['message'])
                location.reload()
            }
        })
    }
}

//FOOD:
function addToCart (id, name, price){
    fetch('api/addtocart', {
        'method': 'post',
        'body': JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        'headers':{
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        var stats = document.getElementById("cart-stats")
        stats.innerText = `${data.total_quantity} - ${data.total_amount}$`
    })
}

function pay() {
    fetch('api/pay', {
        'method': 'post',
        'headers':{
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.message)
        location.reload()
    }).catch(err => console.log(err));
}

function del(item_id){
    if (confirm("Ban co muon xoa san pham") == true){
        fetch(`/api/cart/${item_id}`, {
            'method': 'delete',
            'headers': {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if(data.code == 1){
                var x = document.getElementById(`item${ item_id }`)
                location.reload()
            } else {
                alert('Xoa that bai!');
            }
        }).catch(err => alert('Xoa that bai'))
    }

}

function update(obj, item_id){
    fetch(`/api/cart/${item_id}`, {
        'method': 'post',
        'body': JSON.stringify({
            'quantity': obj.value
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if(data.code != 1){
            alert('Cap nhat that bai!');
        } else {
            console.log('success')
        }
    }).catch(err => console.log('That bai'))

}

function showDetailBill(bill_id){
    if (document.getElementById(`detail-tablel-${bill_id}`).style.display == 'none'){
        document.getElementById(`detail-tablel-${bill_id}`).style.display = 'block'
    }
    else {
        document.getElementById(`detail-tablel-${bill_id}`).style.display = 'none'
    }
}
