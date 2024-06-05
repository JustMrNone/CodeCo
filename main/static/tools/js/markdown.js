document.addEventListener('DOMContentLoaded', () => {
    const markdownInput = document.getElementById('markdown-input');
    const markdownPreview = document.getElementById('markdown-preview');

    markdownInput.addEventListener('input', () => {
        const markdownText = markdownInput.value;
        const html = marked(markdownText);
        markdownPreview.innerHTML = html;
    });
});