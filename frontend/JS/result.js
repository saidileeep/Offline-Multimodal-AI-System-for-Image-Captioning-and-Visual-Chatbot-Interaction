let caption=localStorage.getItem("caption")
let counts=JSON.parse(localStorage.getItem("counts"))
let image=localStorage.getItem("image")

document.getElementById("caption").innerText=caption

document.getElementById("resultImage").src=image

let text=""

for(let key in counts){

text+=key+" : "+counts[key]+"\n"

}

document.getElementById("objects").innerText=text

function openChat(){

window.location.href="chatbot.html"

}