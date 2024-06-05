document.addEventListener("DOMContentLoaded", function() {
    const regexForm = document.getElementById('regex-form');
    const regexPatternInput = document.getElementById('regex-pattern');
    const testStringInput = document.getElementById('test-string');
    const caseInsensitiveCheckbox = document.getElementById('case-insensitive');
    const globalSearchCheckbox = document.getElementById('global-search');
    const multiLineCheckbox = document.getElementById('multi-line');
    const regexResults = document.getElementById('regex-results');

    // Function to test the regex
    function testRegex(pattern, testString, flags) {
        try {
            const regex = new RegExp(pattern, flags);
            const matches = testString.match(regex);
            if (matches) {
                return matches.join('\n');
            } else {
                return 'No matches found.';
            }
        } catch (e) {
            return 'Invalid regex pattern.';
        }
    }

    // Form submission handler
    regexForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const pattern = regexPatternInput.value;
        const testString = testStringInput.value;
        let flags = '';
        if (caseInsensitiveCheckbox.checked) flags += 'i';
        if (globalSearchCheckbox.checked) flags += 'g';
        if (multiLineCheckbox.checked) flags += 'm';

        const results = testRegex(pattern, testString, flags);
        regexResults.value = results;
    });
});