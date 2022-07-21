// Open and close the todolists sidebar onclick
document.addEventListener('DOMContentLoaded', function() {
  let content = document.getElementById("myNav");
  let buttonopen = document.getElementById("buttonOpen");
  let buttonclose = document.getElementById("buttonClose");
  buttonopen.addEventListener("click", function() {
    content.style.width = "300px";
  }); 
  buttonclose.addEventListener("click", function() {
    content.style.width = "0%";
  });
});

