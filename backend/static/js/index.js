// FOLLOWING CODE SENDS LOGIN CREDENTIALS TO SERVER ON SUBMIT
let userid = document.getElementById('userid');
let password = document.getElementById('password');
let rememberMeStatus = document.getElementById('remember-me-status');
let submitBtn = document.getElementById('submit-btn');
var loader = document.getElementById('loader')

submitBtn.addEventListener('click',()=>{
    loader.style.display = 'block';
    userCredentials = {
        'user_id':userid.value,
        'password':password.value
    }
    fetch('/admin/login', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userCredentials)
    }).then((res) => res.json())
    .then((data) => {
        console.log(data);
        if (data['status']){
            // IT STOPS THE LOADER AS SOON AS THE STATUS IF FOUND AFTER SUBMITTING THE LOGIN BUTTON.
            loader.style.display = 'none';    
        }
    })
});
