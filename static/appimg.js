// UI
const sendbtn = document.getElementById('send-btn');
const userinput = document.getElementById('userinput');
const displaybox = document.getElementById('displaybox');
const clearhistory =  document.getElementById('clear-history')

// https://fastapi.tiangolo.com/advanced/websockets/#in-production
// for localhost
// var ws = new WebSocket("ws://localhost:8000/ws");

// for cloud server https deployment
var websocketstring = '';

if(window.location.hostname === "localhost" || window.location.hostname === '127.0.0.1' ){
	websocketstring = 'ws://localhost:8000/image';

}else{
	websocketstring = `wss://${window.location.hostname}/image`;
}

let ws = new WebSocket(websocketstring);


let lastmessagediv = null;
let isnewinput = true ;

ws.onopen = function () {

	console.log('websocket connection established');

};

ws.onerror = function (err) {

	console.log('websocket connection error',err);
	document.getElementById('loading-spinner').style.display = "none";

}

ws.onclose = function (event) {

	console.log('websocket connection established',event);
	document.getElementById('loading-spinner').style.display = "none";


};

ws.onmessage = function (event) {

    let message = event.data;
    // console.log(event);
    // console.log(message);

    // console.log("Message Event",event.data)

    let img = document.createElement("img");
        img.src = message;
        img.className = 'responseimg';
        displaybox.appendChild(img); 

        savetolocal('ai-response',message);

    document.getElementById('loading-spinner').style.display = 'none';

}

console.log('hello');

sendbtn.addEventListener('click',function(e){
	e.preventDefault();

	let getinputval = userinput.value.trim();
	console.log(getinputval);

	if(getinputval){

		let userinputdiv = document.createElement('div');
		userinputdiv.className = "p-3 ms-3 chat-message user-input";
		userinputdiv.textContent = getinputval;
		displaybox.appendChild(userinputdiv);

		ws.send(getinputval)

		savetolocal('user-input',getinputval)

		userinput.value = "";
		userinput.focus();

		document.getElementById('loading-spinner').style.display="block";

	}

})

// 6AP
// 7OT

window.onload = function(){

	// console.log('hello')

	let storagedatas = JSON.parse(localStorage.getItem('imghistory') || "[]" );

	if(storagedatas.length > 0){

		let currole = null;
		let curcontent = '';

		storagedatas.forEach((storagedata,idx)=>{

			if(storagedata.role === currole){
				curcontent += storagedata.content;
			}else{
				console.log(currole)

				if(currole){
					
					if(currole === 'user-input'){
						let messagediv = document.createElement('div');
						messagediv.className = "p-3 ms-3 chat-message "+ currole;
						messagediv.textContent = curcontent;
						displaybox.appendChild(messagediv);
					}else if (currole === 'ai-response'){
						let img = document.createElement("img");
				    	img.src = curcontent;
					    img.className = 'responseimg';
					    displaybox.appendChild(img); 
					}

				}

				currole = storagedata.role;
				curcontent = storagedata.content;



			}

				if(idx === storagedatas.length -1){
					let img = document.createElement("img");
				    	img.src = curcontent;
					    img.className = 'responseimg';
					    displaybox.appendChild(img); 
				}

		})

	}else{

		displaybox.innerHTML = `<small class="text-muted" >How can I help you ?</small>`

	} 
}

function savetolocal(role,content){
 
	let getdatas = JSON.parse(localStorage.getItem('imghistory') || "[]" ) ;
	getdatas.push({role:role,content:content});
	localStorage.setItem('imghistory',JSON.stringify(getdatas));
	// {role:'user-input',content:"hello"}

}

clearhistory.addEventListener('click',function(){
	localStorage.removeItem('imghistory');
	location.reload();
})

// 9TT
// 9TV