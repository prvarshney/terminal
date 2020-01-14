let userid = document.getElementById('userid');
let submitOtp = document.getElementById('submitOtp');
let newPassword = document.getElementById('newPassword');
let confirmPassword = document.getElementById('confirmPassword');
let setPassword = document.getElementById('setPassword');
let submitPassword = document.getElementById('submitPassword');
let enterOTP = document.getElementById('enterOTP');
userid.value = "";
enterOTP.value = "";

// EVENT LISTENERS --START
submitOtp.addEventListener('click',()=>{
    userid_val = userid.value;
    fetch('/admin/forgot_password/'+userid_val,{
        method: 'GET',        
    }).then((res) => res.json())
    .then((data) => {
        if (data['status']==200){
            setPassword.style.display = 'block';
        }
    });
});

submitPassword.addEventListener('click',()=>{
    if (newPassword.value == confirmPassword.value){
        userCredentials = {        
            'user_id': userid.value,
            'otp': Number(enterOTP.value),
            'new_password': newPassword.value
        }  
        fetch('/admin/recover_password',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'},
            body: JSON.stringify(userCredentials)
        }).then((res) => res.json())        
    } else {
        console.log('Passwords did not match.')
    }
});
//EVENT LISTENERS --END