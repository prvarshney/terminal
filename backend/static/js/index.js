// FOLLOWING CODE SENDS LOGIN CREDENTIALS TO SERVER ON SUBMIT
let userid = document.getElementById('userid');
let password = document.getElementById('password');
let rememberMeStatus = document.getElementById('remember-me-status');
let submitBtn = document.getElementById('submit-btn');
var loader = document.getElementById('loader');
let submitOtp = document.getElementById('submitOtp');
var setPassword = document.getElementById('setPassword');
var setPassword2 = document.getElementById('setPassword2');
var newPassword = document.getElementById('newPassword');
var confirmPassword = document.getElementById('confirmPassword');
var enterOTP = document.getElementById('enterOTP');

// submitBtn.addEventListener('click',()=>{
//     loader.style.display = 'block';
//     userCredentials = {
//         'user_id':userid.value,
//         'password':password.value
//     }
//     fetch('/admin/login', {
//         method: 'POST',
//         headers: {
//             'Accept': 'application/json',
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(userCredentials)
//     }).then((res) => res.json())
//     .then((data) => {
//         console.log(data);
//         if (data['status']){
//             // IT STOPS THE LOADER AS SOON AS THE STATUS IF FOUND AFTER SUBMITTING THE LOGIN BUTTON.
//             loader.style.display = 'none';               
//         }
//         if (data['status']==200){
//             console.log('Logged In');
//             window.location.href = "http://localhost:5000"
//         } 
//     })
// });

submitOtp.addEventListener('click',()=>{
    userid_val = userid.value;
    fetch('/admin/forgot_password/'+userid_val,{
        method: 'GET',        
    }).then((res) => res.json())
    .then((data) => {
        console.log(data);
        if (data['status']==200){
            setPassword.style.display = 'block';
        }
    });
});

setPassword2.addEventListener('click',()=>{
    userCredentials = {
        'user_id': userid.value,
        'otp': enterOTP.value,
        'new_password': newPassword.value
        // 'confirm_Password': confirmPassword.value,
    };   
    fetch('/admin/recover_password',{
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userCredentials)
    }).then((res) => res.json())
    .then((data) => {
        console.log(userCredentials)
        console.log(data);
    })
});

