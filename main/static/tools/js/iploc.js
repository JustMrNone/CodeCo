document.addEventListener("DOMContentLoaded", function() {
    // Function to fetch IP information
    async function fetchIPInfo(ip = '') {
        const response = await fetch(`https://ipapi.co/${ip}/json/`);
        return response.json();
    }

    // Function to display IP information
    function displayIPInfo(data, elementId) {
        const infoElement = document.getElementById(elementId);
        infoElement.innerHTML = `
            <p><strong>IP:</strong> ${data.ip}</p>
            <p><strong>City:</strong> ${data.city}</p>
            <p><strong>Region:</strong> ${data.region}</p>
            <p><strong>Country:</strong> ${data.country_name}</p>
            <p><strong>ISP:</strong> ${data.org}</p>
        `;
    }

    // Fetch and display user's IP info
    fetchIPInfo().then(data => {
        displayIPInfo(data, 'user-ip-info');
    });

    // Form submission handler for IP lookup
    const ipForm = document.getElementById('ip-form');
    ipForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const ipInput = document.getElementById('ip-input').value.trim();
        if (ipInput) {
            fetchIPInfo(ipInput).then(data => {
                displayIPInfo(data, 'lookup-ip-info');
            });
        }
    });
});