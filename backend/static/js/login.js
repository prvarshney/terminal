// FOLLOWING CODE SENDS LOGIN CREDENTIALS TO SERVER ON SUBMIT
let userid = document.getElementById('userid');
let password = document.getElementById('password');
let rememberMeStatus = document.getElementById('remember-me-status');
let submitBtn = document.getElementById('submit-btn');
let loader = document.getElementById('loader');

// document.cookie = "username=John Smith;path=/";
// var decodedCookie = decodeURIComponent(document.cookie);
// console.log(decodedCookie);

// CHECKING THE PRESENCE OF ACCESS_TOKEN_COOKIE AND REFRESH_TOKEN_COOKIE
let decodedCookie = decodeURIComponent( document.cookie ).split(';');
for( let itr = 0; itr < decodedCookie.length; itr++ ){
    let cookie = decodedCookie[itr].split('=');
    let key = cookie[0] // KEY IS AT Oth INDEX
    let value = cookie[1]   // VALUE IS AT 1th INDEX
    if( key == 'access_token_cookie' ){
        // REDIRECTING TO DASHBOARD
        window.location.href = "/dashboard";
    }
}

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
            let date = new Date();
            let cookieCreationTime = date.getTime();    // CONVERTED CURRENT TIME INTO MICROSECONDS FORMAT
            let accessTokenCookieExpirationTime = new Date( cookieCreationTime + 15*60000 );
            let cookieExpirationTime = accessTokenCookieExpirationTime.toUTCString();
            document.cookie = `access_token_cookie = ${response['access-token']};expires = ${cookieExpirationTime}; path=/; SameSite=Strict`;
            let refreshTokenCookieExpirationTime = new Date( cookieCreationTime + 30*24*60*60000 );
            cookieExpirationTime = refreshTokenCookieExpirationTime.toUTCString();
            document.cookie = `refresh_token_cookie = ${response['refresh-token']};expires = ${cookieExpirationTime}; path=/; SameSite=Strict`;
            // REDIRECTING TO DASHBOARD
            window.location.href = "/dashboard";
        }
    })
});
//EVENT LISTENERS --END