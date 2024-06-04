document.addEventListener("DOMContentLoaded", function() {
  function myFunction() {
      var x = document.getElementById("myLinks");
      if (x.style.display === "block") {
          x.style.display = "none";
      } else {
          x.style.display = "block";
      }
  }

  // Attach the function to the icon click event
  var icon = document.querySelector('.topnav .icon');
  icon.addEventListener('click', myFunction);
});