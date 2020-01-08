console.log("Hello World");
// document.getElementById("submit_btn").addEventListener("click", function(){
//     // let user_id = document.getElementById('user_id');
//     console.log("Hello World");
// });
let submit = document.getElementById("submit_btn");
let user_id = document.getElementById("user_id");
submit.addEventListener("click", function (){
    console.log(user_id.value);
})
console.log(user_id.value);