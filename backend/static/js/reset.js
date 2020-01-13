let currentPassword = document.getElementById('currentPassword');
let newPassword = document.getElementById('newPassword');
let confirmPassword = document.getElementById('confirmPassword');
let submitBtn = document.getElementById('submitBtn');

// EVENT LISTENERS --START
submitBtn.addEventListener('click', ()=>{
    if (newPassword.value == confirmPassword.value){
        userCredentials = {
            'current_password': currentPassword.value,
            'new_password': newPassword.value
        }

        fetch('/admin/reset_password',{
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: JSON.stringify( userCredentials )
        }).then( response => response.json() )
        .then((data)=>{
            console.log(data);
        });
    } else {
        console.log("Sorry,new Password and confirm Passwords didn't match.");
    }
});
//EVENT LISTENERS --END