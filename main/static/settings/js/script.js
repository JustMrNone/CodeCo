document.addEventListener("DOMContentLoaded", function () {
    let cardHeaders = document.querySelectorAll(".card-header");
    const fileInput = document.getElementById('id_profile_picture');
    const fileInputText = document.querySelector('.file-input-text');

    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            fileInputText.textContent = fileInput.files[0].name;
        } else {
            fileInputText.textContent = 'No file chosen';
        }
    });
    cardHeaders.forEach(function (header) {
        header.addEventListener("click", function () {
          let cardBody = this.nextElementSibling;
          cardBody.classList.toggle("collapsed");
      
          // Update arrow icon based on collapse state
          const arrowIcon = this.querySelector('i.arrowdown');
      
          // Toggle the arrow icon classes
          if (cardBody.classList.contains("collapsed")) {
            arrowIcon.classList.remove('fa-arrow-down');
            arrowIcon.classList.add('fa-arrow-up');
          } else {
            arrowIcon.classList.remove('fa-arrow-up');
            arrowIcon.classList.add('fa-arrow-down');
          }
        });
      });
});


