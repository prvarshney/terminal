let programme = document.getElementById('programme');
let branch = document.getElementById('branch');
let section = document.getElementById('section');
let yearOfPass = document.getElementById('year_of_pass');
let showBtn = document.getElementById('queryBtn');
let loader = document.getElementById('loader');

showBtn.addEventListener('click', ()=>{
    window.location.href = `/admin/dashboard/showAll/${programme.value}/${branch.value}/${section.value}/${yearOfPass.value}`;
    // loader.style.display = "none";
    // console.log(queryValues);
    // fetch('/admin/show_all'+programme.value+branch.value+section.value+yearOfPass.value , {
    //     method : 'POST',
    //     redirect:"follow",
    //     headers : { 'Content-Type':'application/json', 'Accept':'application/json'},
    //     credentials : "include",
    //     body: JSON.stringify(queryValues)
    // }).then( response => response.json() )
    // .then(response => {
    //     console.log(response);
    //     if( response.status == 212 ){
    //         window.location.href = "/admin/show_all";
    //     }
    //     else{
    //         console.log(response);
    //     }
    // })

});

