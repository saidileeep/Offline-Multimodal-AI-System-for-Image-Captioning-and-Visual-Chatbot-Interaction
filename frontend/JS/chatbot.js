let image = localStorage.getItem("uploadedImage")

document.getElementById("chatImage").src = image

function ask(){

let question=document.getElementById("question").value
let chatBox=document.getElementById("chat-box")

chatBox.innerHTML+="<p class='user'>You: "+question+"</p>"

let loader=document.getElementById("chat-loader")
let bar=document.getElementById("chat-progress-bar")
let text=document.getElementById("chat-progress-text")

loader.style.display="block"

let progress=0

let interval=setInterval(function(){

progress+=10

if(progress>95){progress=95}

bar.style.width=progress+"%"
text.innerText=progress+"%"

},200)

fetch("http://127.0.0.1:8000/chat/",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
question:question
})

})
.then(res=>res.json())
.then(data=>{

clearInterval(interval)

bar.style.width="100%"
text.innerText="100%"

setTimeout(function(){

loader.style.display="none"

chatBox.innerHTML+="<p class='bot'>Bot: "+data.answer+"</p>"

},400)

})

}