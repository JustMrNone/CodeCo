document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('searchButton').addEventListener('click', filterCards);

    function filterCards() {
        let searchTitle = document.getElementById('searchTitle').value.toLowerCase();
        
        let cards = document.querySelectorAll('.card');

        cards.forEach(function(card) {
            let title = card.querySelector('.card-title').textContent.toLowerCase();

            if (title.includes(searchTitle) || searchTitle === '') {
                card.parentElement.style.display = 'block';
            } else {
                card.parentElement.style.display = 'none';
            }
        });
    }
});