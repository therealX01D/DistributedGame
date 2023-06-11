let userid = "";
let username = "";
window.addEventListener("DOMContentLoaded",function(e){
  const inputspace = document.querySelector('#txt_input');
  const outputspace = document.querySelector('#extmsg');

  const websocket = new WebSocket("ws://13.37.101.135:8001/");
  //while (websocket.readyState != WebSocket.OPEN);
  sendChat(inputspace,websocket);
  recievingChat(outputspace,websocket);
  initializeuser(websocket);
});
function initializeuser(websocket){
  const handleSend = () => {
    if (websocket.readyState === WebSocket.OPEN) {
      eel.getUN()().then((r)=>{
        username = r;
      });
      const event={
      "type":"adduser",
      "usrname":username
    };
    websocket.send(JSON.stringify(event));
    }
    else if (websocket.readyState == WebSocket.CONNECTING) {
      // Wait for the open event, maybe do something with promises
      // depending on your use case. I believe in you developer!
      websocket.addEventListener('open', () => handleSend())
    }
     else {
      // Queue a retry
      setTimeout(() => { handleSend() }, 1000)
    }
  };
  handleSend();
}
function scrollToElm(container, elm, duration){
  var pos = getRelativePos(elm);
  scrollTo( container, pos.top , 2);  // duration in seconds
}

function getRelativePos(elm){
  var pPos = elm.parentNode.getBoundingClientRect(), // parent pos
      cPos = elm.getBoundingClientRect(), // target pos
      pos = {};

  pos.top    = cPos.top    - pPos.top + elm.parentNode.scrollTop,
  pos.right  = cPos.right  - pPos.right,
  pos.bottom = cPos.bottom - pPos.bottom,
  pos.left   = cPos.left   - pPos.left;

  return pos;
}
    
function scrollTo(element, to, duration, onDone) {
    var start = element.scrollTop,
        change = to - start,
        startTime = performance.now(),
        val, now, elapsed, t;

    function animateScroll(){
        now = performance.now();
        elapsed = (now - startTime)/1000;
        t = (elapsed/duration);

        element.scrollTop = start + change * easeInOutQuad(t);

        if( t < 1 )
            window.requestAnimationFrame(animateScroll);
        else
            onDone && onDone();
    };

    animateScroll();
}

function easeInOutQuad(t){ return t<.5 ? 2*t*t : -1+(4-2*t)*t };
///////////////////////
function addchat(name,date,text,chat,otherchat){
        //let date =new Date().toISOString();
        let newmessage=document.createElement("div");
        let namespan = document.createElement("span");
        namespan.id="namemsg";
        namespan.textContent=name;
        let datespan = document.createElement("span");
        datespan.id="datemsg";
        datespan.textContent=date;
        newmessage.className="msg";
        newmessage.textContent=text;
        newmessage.appendChild(datespan);
        newmessage.appendChild(namespan);
        chat.appendChild(newmessage);
        newmessagepseudo= newmessage.cloneNode(true);
        otherchat.appendChild(newmessagepseudo);

        let lastchild = chat.lastElementChild;
        let lastchildchat = otherchat.lastElementChild;
        lastchildchat.id = "visnon";
        scrollToElm(chat,lastchild,600);
        scrollToElm(otherchat,lastchildchat,600);
       

        
}
function sendChat(input, websocket) {
  // When clicking a column, send a "play" event for a move in that column.
  input.addEventListener("keypress", ( e ) => {
    if (e.key === 'Enter') {
      // code for enter
        let userchat =document.querySelector('#usermsg');
        let otherchat =document.querySelector('#extmsg'); 
        if (!document.querySelector('#txt_input').value) {
            return ;
        }
        let inputxt=document.querySelector('#txt_input').value;
        let date= new Date().toISOString();
        addchat(username,date,inputxt,userchat,otherchat);
        const event = 
        {
          "type": "chat",
          "userid":userid,
          "text": inputxt,
          "Date": date
        }
        websocket.send(JSON.stringify(event));
    }
    
  });
}
function showMessage(message) {
  window.setTimeout(() => window.alert(message), 50);
}

function recievingChat(outputspace,websocket){
  console.log("entered function")
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    let extchat =document.querySelector('#extmsg');
    let otherchat =document.querySelector('#usermsg');

    console.log(data);
    switch (event.type) {
      
      case "chat":
        // Update the UI with the move.

        if (event.userid!=userid){
          addchat(event.usrname,event.Date,event.text,extchat,otherchat);
        }
        break;
      case "acceptinit":
        userid = event.userid;
        // No further messages are expected; close the WebSocket connection.
        break;
      case "error":
        showMessage(event.message);
        break;
      default:
        throw new Error(`Unsupported event type: ${event.type}.`);
    }
  });
}
// document.querySelector('#txt_input').addEventListener('keypress', function (e) {

//     if (e.key === 'Enter') {
//       // code for enter
//         if (document.querySelector('#txt_input').value) {
//           let newmessage=document.createElement("div");
//           let datespan = document.createElement("span");
//           datespan.id="datemsg";
//           datespan.textContent=new Date().toISOString();
//           newmessage.className="msg";
//           newmessage.textContent=document.querySelector('#txt_input').value;
//           newmessage.appendChild(datespan);
  
//           userchat.appendChild(newmessage);
//           let lastchild = userchat.lastElementChild;
//           lastchild.scrollIntoView({ behavior: 'smooth' })
//         }
//     }
// });