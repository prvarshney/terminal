let currentPassword = document.getElementById('currentPassword');
let newPassword = document.getElementById('newPassword');
let confirmPassword = document.getElementById('confirmPassword');
let submitBtn = document.getElementById('submitBtn');
let loader = document.getElementById('loader');
let eyeTogglerCurrent = document.getElementById('eyeTogglerCurrent');
let eyeTogglerNew = document.getElementById('eyeTogglerNew');
let eyeTogglerConfirm = document.getElementById('eyeTogglerConfirm');
let eyeTogglerStatus = false;

// EVENT LISTENERS --START
eyeTogglerCurrent.addEventListener('click', ()=>{
    if(!eyeTogglerStatus){
        eyeTogglerStatus = true;
        eyeTogglerCurrent.classList.remove('fa-eye-slash');
        eyeTogglerCurrent.classList.add('fa-eye');
        currentPassword.type = 'text';
    }
    else{
        eyeTogglerStatus = false;
        eyeTogglerCurrent.classList.remove('fa-eye');
        eyeTogglerCurrent.classList.add('fa-eye-slash');
        currentPassword.type = 'password';
    }
});

eyeTogglerNew.addEventListener('click', ()=>{
    if(!eyeTogglerStatus){
        eyeTogglerStatus = true;
        eyeTogglerNew.classList.remove('fa-eye-slash');
        eyeTogglerNew.classList.add('fa-eye');
        newPassword.type = 'text';
    }
    else{
        eyeTogglerStatus = false;
        eyeTogglerNew.classList.remove('fa-eye');
        eyeTogglerNew.classList.add('fa-eye-slash');
        newPassword.type = 'password';
    }
});

eyeTogglerConfirm.addEventListener('click', ()=>{
    if(!eyeTogglerStatus){
        eyeTogglerStatus = true;
        eyeTogglerConfirm.classList.remove('fa-eye-slash');
        eyeTogglerConfirm.classList.add('fa-eye');
        confirmPassword.type = "text";
    }
    else{
        eyeTogglerStatus = false;
        eyeTogglerConfirm.classList.remove('fa-eye');
        eyeTogglerConfirm.classList.add('fa-eye-slash');
        confirmPassword.type = "password";
    }
})

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