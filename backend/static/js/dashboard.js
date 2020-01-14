let show_all = document.getElementById('show-all');
let removeOne = document.getElementById('removeOne');
let loader = document.getElementById('loader');

show_all.addEventListener('click', ()=>{
    window.location.href = "/admin/dashboard/queryTable";
});

removeOne.addEventListener('click', ()=>{
    // loader.style.display = "block";
    window.location.href = "/admin/dashboard/deleteOne";
    // loader.style.display = 'none';
})