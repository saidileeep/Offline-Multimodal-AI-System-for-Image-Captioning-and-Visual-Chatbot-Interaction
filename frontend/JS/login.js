function login(){

let user=document.getElementById("username").value
let pass=document.getElementById("password").value

if(user==="mohan" && pass==="1234"){

window.location.href="upload.html"

}
else{

alert("Invalid Login")

}

}