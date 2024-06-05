const loremIpsumText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum vestibulum. Cras venenatis euismod malesuada. Nullam ac erat ante. Proin ac malesuada ante. Nulla facilisi. Sed faucibus metus id bibendum facilisis. Proin ac dignissim arcu, vel feugiat libero. Vestibulum ac lacus sed ligula congue efficitur. Nam sed bibendum elit. Mauris vehicula nisi at ex auctor, in volutpat dolor scelerisque. Etiam nec nisi vel velit malesuada scelerisque. Quisque auctor, ligula nec venenatis consequat, libero nulla dapibus lectus, et tempus dolor ipsum et nisl. Aenean ac sem et libero euismod laoreet. Ut eget elit ut libero varius dapibus. Morbi gravida sapien et nisl fermentum, a pellentesque libero scelerisque.";

function updateRangeValue(value) {
    document.getElementById('rangeValue').innerText = `Length: ${value} words`;
}

function generateLoremIpsum() {
    const length = parseInt(document.getElementById('lengthRange').value, 10);
    const outputElement = document.getElementById('output');
    const words = loremIpsumText.split(' ');

    let generatedText = [];
    while (generatedText.length < length) {
        generatedText = generatedText.concat(words);
    }

    generatedText = generatedText.slice(0, length).join(' ');
    outputElement.innerText = generatedText;
}