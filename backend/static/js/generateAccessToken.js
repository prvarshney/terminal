// SENDING GET REQUEST TO /generate_access_token to REGENERATE ACCESS TOKEN COOKIE FROM REFRESH_TOKEN_COOKIE

fetch('/generate_access_token', {
    method: 'GET',
    headers: { 'Accept':'application/json' }
}).then(response => response.json())
.then(response => {
    location.reload();
})