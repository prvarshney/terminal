let userid = document.getElementById('userid');
let submitOtpBtn = document.getElementById('submitOtpBtn');
let newPasswordBtn = document.getElementById('newPasswordBtn');
let confirmPasswordBtn = document.getElementById('confirmPasswordBtn');
let secondDiv = document.getElementById('secondDiv');
let submitPasswordBtn = document.getElementById('submitPasswordBtn');
let enterOtpBtn = document.getElementById('enterOtpBtn');
userid.value = "";
enterOtpBtn.value = "";

// EVENT LISTENERS --START
submitOtpBtn.addEventListener('click',()=>{
    userid_val = userid.value;
    fetch('/admin/forgot_password/'+userid_val,{
        method: 'GET',        
    }).then((res) => res.json())
    .then((data) => {
        if (data['status']==200){
            secondDiv.style.display = 'block';
        }
    });
});

submitPasswordBtn.addEventListener('click',()=>{
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
    } else {
        console.log('Passwords did not match.')
    }
});
//EVENT LISTENERS --END