document.addEventListener('DOMContentLoaded', function() {
    let searchType = 'title';

    window.setSearchOption = function(option) {
        document.getElementById('searchOption').textContent = option;
        searchType = option.toLowerCase().includes('title') ? 'title' : 'category';
    }

    window.performSearch = function() {
        const searchTerm = document.getElementById('searchInput').value;
        if (searchTerm) {
            alert(`Searching for ${searchTerm} in ${searchType}`);
            // Here you can add your search logic, e.g., making an API call or redirecting to another page
        } else {
            alert('Please enter a search term');
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