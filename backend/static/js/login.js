// FOLLOWING CODE SENDS LOGIN CREDENTIALS TO SERVER ON SUBMIT
let userid = document.getElementById('userid');
let password = document.getElementById('password');
let rememberMeStatus = document.getElementById('remember-me-status');
let submitBtn = document.getElementById('submit-btn');
let eyeToggler = document.getElementById('eye-toggler');
let errorDisplayField = document.getElementById('error-display-field');
let loader = document.getElementById('loader');
let eyeTogglerStatus = false;

userid.value = "";
password.value = "";

// EVENT LISTENERS --START
eyeToggler.addEventListener('click', ()=>{
    if ( !eyeTogglerStatus ){
        eyeTogglerStatus = true;
        eyeToggler.classList.remove('fa-eye-slash');
        eyeToggler.classList.add('fa-eye');
        password.type = 'text';
    }
    else{
        eyeTogglerStatus = false;
        eyeToggler.classList.remove('fa-eye');
        eyeToggler.classList.add('fa-eye-slash');
        password.type = 'password';
    }
});


submitBtn.addEventListener('click', ()=>{
    // LOADING LOADER.GIF
    loader.style.display = "block";
    userCredentials = {
        'user_id': userid.value,
        'password': password.value
    }

    fetch('/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify( userCredentials )
    }).then( response => response.json() )
    .then( response => {
        // HIDING LOADER.GIF
        loader.style.display = 'none';
        if( response.status == 200 ){    // EXECUTES WHEN LOGIN GETS SUCCESSFUL
            // REDIRECTING TO DASHBOARD
            window.location.href = "/admin/queryTable";
        }
        else{       // EXECUTES WHEN LOGIN WAS UNSUCCESSFUL
            errorDisplayField.classList.remove('invisible');
        }
    })
});

//EVENT LISTENERS --END