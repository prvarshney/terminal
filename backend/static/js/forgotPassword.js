let userid = document.getElementById('userid');
let submitOtpBtn = document.getElementById('submitOtpBtn');
let newPasswordBtn = document.getElementById('newPasswordBtn');
let confirmPasswordBtn = document.getElementById('confirmPasswordBtn');
let secondDiv = document.getElementById('secondDiv');
let submitPasswordBtn = document.getElementById('submitPasswordBtn');
let enterOtpBtn = document.getElementById('enterOtpBtn');
let loader = document.getElementById('loader');
let eyeTogglerNew = document.getElementById('eyeTogglerNew');
let eyeTogglerConfirm = document.getElementById('eyeTogglerConfirm');
let eyeTogglerStatus = false;

userid.value = "";
enterOtpBtn.value = "";

// EVENT LISTENERS --START
submitOtpBtn.addEventListener('click',()=>{
    // LOADING LOADER.GIF
    loader.style.display = "block";
    userid_val = userid.value;
    fetch('/admin/forgot_password/'+userid_val,{
        method: 'GET',        
    }).then((res) => res.json())
    .then((data) => {
        // HIDING LOADER.GIF
        loader.style.display = 'none';        
        if (data['status']==200){
            // DISPLAY THE FIELDS TO SET PASSWORD
            secondDiv.style.display = 'block';
        }
    });
});

//SETTING EYE TOGGLER-
eyeTogglerNew.addEventListener('click', ()=>{
    if(!eyeTogglerStatus){
        eyeTogglerStatus = true;
        eyeTogglerNew.classList.remove('fa-eye-slash');
        eyeTogglerNew.classList.add('fa-eye');
        newPasswordBtn.type = 'text';
    }
    else{
        eyeTogglerStatus = false;
        eyeTogglerNew.classList.remove('fa-eye');
        eyeTogglerNew.classList.add('fa-eye-slash');
        newPasswordBtn.type = 'password';
    }
});

eyeTogglerConfirm.addEventListener('click', ()=>{
    if(!eyeTogglerStatus){
        eyeTogglerStatus = true;
        eyeTogglerConfirm.classList.remove('fa-eye-slash');
        eyeTogglerConfirm.classList.add('fa-eye');
        confirmPasswordBtn.type = "text";
    }
    else{
        eyeTogglerStatus = false;
        eyeTogglerConfirm.classList.remove('fa-eye');
        eyeTogglerConfirm.classList.add('fa-eye-slash');
        confirmPasswordBtn.type = "password";
    }
})


submitPasswordBtn.addEventListener('click',()=>{
    // LOADING LOADER.GIF
    loader.style.display = "block";  
    if (newPasswordBtn.value == confirmPasswordBtn.value){              
        userCredentials = {        
            'user_id': userid.value,
            'otp': Number(enterOtpBtn.value),
            'new_password': newPasswordBtn.value
        }  
        fetch('/admin/recover_password',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'},
            body: JSON.stringify(userCredentials)
        }).then((res) => res.json())  
        .then( res => {
            // HIDING LOADER.GIF
            loader.style.display = 'none';            
        });  
    } else {
        console.log('Passwords did not match.')
        // HIDING LOADER.GIF
        loader.style.display = 'none';   
    }
});
//EVENT LISTENERS --END