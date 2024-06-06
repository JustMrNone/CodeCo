document.addEventListener("DOMContentLoaded", function(){
    $(document).ready(function () {
        function hexToRgb(hex) {
            let bigint = parseInt(hex.slice(1), 16);
            let r = (bigint >> 16) & 255;
            let g = (bigint >> 8) & 255;
            let b = bigint & 255;
            return `rgb(${r}, ${g}, ${b})`;
        }
    
        function rgbToCmyk(r, g, b) {
            let c = 1 - (r / 255);
            let m = 1 - (g / 255);
            let y = 1 - (b / 255);
            let k = Math.min(c, Math.min(m, y));
            c = (c - k) / (1 - k);
            m = (m - k) / (1 - k);
            y = (y - k) / (1 - k);
            return `cmyk(${(c * 100).toFixed(0)}%, ${(m * 100).toFixed(0)}%, ${(y * 100).toFixed(0)}%, ${(k * 100).toFixed(0)}%)`;
        }
    
        function rgbToHsv(r, g, b) {
            r /= 255, g /= 255, b /= 255;
            let max = Math.max(r, g, b), min = Math.min(r, g, b);
            let h, s, v = max;
            let d = max - min;
            s = max == 0 ? 0 : d / max;
            if (max == min) {
                h = 0;
            } else {
                switch (max) {
                    case r: h = (g - b) / d + (g < b ? 6 : 0); break;
                    case g: h = (b - r) / d + 2; break;
                    case b: h = (r - g) / d + 4; break;
                }
                h /= 6;
            }
            return `hsv(${(h * 360).toFixed(0)}°, ${(s * 100).toFixed(0)}%, ${(v * 100).toFixed(0)}%)`;
        }
    
        function rgbToHsl(r, g, b) {
            r /= 255, g /= 255, b /= 255;
            let max = Math.max(r, g, b), min = Math.min(r, g, b);
            let h, s, l = (max + min) / 2;
            if (max == min) {
                h = s = 0;
            } else {
                let d = max - min;
                s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
                switch (max) {
                    case r: h = (g - b) / d + (g < b ? 6 : 0); break;
                    case g: h = (b - r) / d + 2; break;
                    case b: h = (r - g) / d + 4; break;
                }
                h /= 6;
            }
            return `hsl(${(h * 360).toFixed(0)}°, ${(s * 100).toFixed(0)}%, ${(l * 100).toFixed(0)}%)`;
        }
    
        function updateValues(hex) {
            let rgb = hexToRgb(hex);
            let rgbArr = rgb.match(/\d+/g).map(Number);
            let cmyk = rgbToCmyk(...rgbArr);
            let hsv = rgbToHsv(...rgbArr);
            let hsl = rgbToHsl(...rgbArr);
    
            $('#colorCanvas').css('background-color', hex);
            $('#rgbValue').val(rgb);
            $('#cmykValue').val(cmyk);
            $('#hsvValue').val(hsv);
            $('#hslValue').val(hsl);
        }
    
        $('#colorPicker').on('input', function () {
            let hex = $(this).val();
            $('#hexValue').val(hex);
            updateValues(hex);
        });
    
        $('#hexValue').on('input', function () {
            let hex = $(this).val();
            if (/^#[0-9A-F]{6}$/i.test(hex)) {
                $('#colorPicker').val(hex);
                updateValues(hex);
            }
        });
    
        updateValues('#4287f5'); // Initial color update
    });

})