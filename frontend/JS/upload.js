function uploadImage(){

let file=document.getElementById("upload").files[0]

if(!file){

alert("Choose image")
return

}

let reader=new FileReader()

reader.onload=function(e){

localStorage.setItem("image",e.target.result)

document.getElementById("preview").src=e.target.result

}

reader.readAsDataURL(file)

let loader=document.getElementById("ai-loader")
let bar=document.getElementById("progress-bar")
let text=document.getElementById("progress-text")

loader.style.display="block"

let progress=0

let interval=setInterval(function(){

progress+=10

bar.style.width=progress+"%"
text.innerText=progress+"%"

if(progress>=100){

clearInterval(interval)

}

},400)

let formData=new FormData()

formData.append("file",file)

fetch("http://127.0.0.1:8000/analyze/",{

method:"POST",
body:formData

})
.then(res=>res.json())
.then(data=>{

localStorage.setItem("caption",data.caption)
localStorage.setItem("counts",JSON.stringify(data.counts))

setTimeout(function(){

window.location.href="result.html"

},800)

})

}