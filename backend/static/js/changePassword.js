let currentPassword = document.getElementById('currentPassword');
let newPassword = document.getElementById('newPassword');
let confirmPassword = document.getElementById('confirmPassword');
let submitBtn = document.getElementById('submitBtn');
let loader = document.getElementById('loader');

// EVENT LISTENERS --START
submitBtn.addEventListener('click', ()=>{
    // LOADING LOADER.GIF
    loader.style.display = "block";
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
            // HIDING LOADER.GIF
            loader.style.display = 'none';
            console.log(data);
        });
    } else {
        // HIDING LOADER.GIF
        loader.style.display = 'none';
        console.log("Sorry,new Password and confirm Passwords didn't match.");
    }
});

//EVENT LISTENERS --END