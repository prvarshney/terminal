// FOLLOWING CODE SENDS LOGIN CREDENTIALS TO SERVER ON SUBMIT
let userid = document.getElementById('userid');
let password = document.getElementById('password');
let rememberMeStatus = document.getElementById('remember-me-status');
let submitBtn = document.getElementById('submit-btn');
let loader = document.getElementById('loader');

// EVENT LISTENERS --START
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
            window.location.href = "/dashboard";
        }
        else{       // EXECUTES WHEN LOGIN WAS UNSUCCESSFUL
            console.log(response);
        }
    })
});
//EVENT LISTENERS --END