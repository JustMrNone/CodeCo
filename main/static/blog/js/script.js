document.addEventListener('DOMContentLoaded', function() {
    let searchType = 'title'; // Default search option

    window.setSearchOption = function(option) {
        const searchOptionButton = document.getElementById('searchOption');
        searchOptionButton.textContent = option;

        if (option === 'Search by Title') {
            searchType = 'title';
        } else if (option === 'Search by Category') {
            searchType = 'category';
        } else if (option === 'Search by Word') {
            searchType = 'word';
        }
    }

    window.performSearch = function() {
        const searchInput = document.getElementById('searchInput').value;
        if (searchInput) {
            const searchForm = document.getElementById('searchForm');
            searchForm.querySelector('input[name="option"]').value = searchType;
            searchForm.querySelector('input[name="query"]').value = searchInput;
            searchForm.submit();
        } else {
            document.getElementById('searchMessage').textContent = 'Please enter a search term';
        }
    }

    // Close dropdown when clicking outside of it
    document.addEventListener('click', function(event) {
        const dropdownButton = document.querySelector('.dropdown-toggle');
        const dropdownMenu = document.querySelector('.dropdown-menu');
        if (!dropdownButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove('show');
        }
    });

    // Toggle dropdown menu when clicking the dropdown button
    document.querySelector('.dropdown-toggle').addEventListener('click', function() {
        const dropdownMenu = document.querySelector('.dropdown-menu');
        if (dropdownMenu.classList.contains('show')) {
            dropdownMenu.classList.remove('show');
        } else {
            dropdownMenu.classList.add('show');
        }
    });

    // Handle click on dropdown items
    document.querySelectorAll('.dropdown-item').forEach(function(item) {
        item.addEventListener('click', function() {
            window.setSearchOption(item.textContent);
        });
    });

    // Handle search button click
    document.querySelector('.btn-primary').addEventListener('click', window.performSearch);
});