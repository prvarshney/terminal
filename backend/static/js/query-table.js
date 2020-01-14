let programme = document.getElementById('programme');
let branch = document.getElementById('branch');
let section = document.getElementById('section');
let yearOfPass = document.getElementById('year_of_pass');
let showBtn = document.getElementById('queryBtn');

showBtn.addEventListener('click', ()=>{
    queryValues = {
        'programme' : programme.value,
        'branch' : branch.value,
        'section' : section.value,
        'year_of_pass' : yearOfPass.value 
    };
    console.log(queryValues);
    fetch('/admin/show_all', {
        method : 'POST',
        headers : { 'Content-Type':'application/json', 'Accept':'application/json'},
        credentials : "include",
        body: JSON.stringify(queryValues)
    }).then( response => response.json() )
    .then(response => {
        console.log(response);
        if( response.status == 212 ){
            window.location.href = "/admin/show_all";
        }
        else{
            console.log(response);
        }
    })

});

