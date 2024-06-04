document.addEventListener("DOMContentLoaded", function () {
    let cardHeaders = document.querySelectorAll(".card-header");

    cardHeaders.forEach(function (header) {
        header.addEventListener("click", function () {
            let cardBody = this.nextElementSibling;
            cardBody.classList.toggle("collapsed");
        });
    });
});