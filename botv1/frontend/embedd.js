var stringSource = `
<div id="botBody"> 
  <style>
    .button1{border:0;
    color:#fff;
    line-height:1;
    cursor:pointer;
    font-size:19px;
    font-weight:500;
    padding:7px 15px;
    border-radius:30px;
    font-family:"Open Sans",sans-serif;
    background:#650010;
    box-shadow:2px 3px 4px 0 rgba(0,0,0,.25)}
  </style>
  <div id="vitapchatbot" style="display: block;
    position: fixed; visibility: visible; z-index: 2147483647;
    transition: none 0s ease 0s; background: transparent none repeat scroll 0% 0%;
    bottom: 0px; left: 0px; width: 360px; height: 500px;" data-trid="702" width="" >
    <button id='botActivator' class="button1" onclick="toggle()">Have Any Questions?</button>
  </div>

  <script>
  </script>

</div>
`;
document.body.insertAdjacentHTML('afterbegin', stringSource);

var isOpen = false;

var parent = document.getElementById("vitapchatbot");
var activator = document.getElementById("botActivator");
var iframeSource = "<iframe id='botIframe' src='https://vitapchatbot.duckdns.org/' style='border: medium none;width:360px;height:440px;'><br>";
var iframe = null;
function shrinkParent(){
  parent.style.height = "50px";
  parent.style.width = "240px"; 
}

function expandParent(){
  parent.style.height="500px";
  parent.style.width ="360px";
}

function toggle(){
  if(isOpen){
    iframe.style.display = "none";
    activator.innerHTML = "Have Any Questions?"
    shrinkParent();
  } else {
    if(iframe!=null){
      iframe.style.display = "block";
      } else {
        activator.insertAdjacentHTML("beforebegin",iframeSource);
        iframe = document.getElementById("botIframe");
      }
      activator.innerHTML = "Close Bot"
      expandParent();
  }
  isOpen=!isOpen;
}

shrinkParent();

