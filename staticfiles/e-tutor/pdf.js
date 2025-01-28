const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const readButton = document.getElementById('readButton');


dropZone.addEventListener('click', () => fileInput.click());


['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});


dropZone.addEventListener('dragover', () => {
    dropZone.classList.add('hover');
});
dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('hover');
});


dropZone.addEventListener('drop', (event) => {
    dropZone.classList.remove('hover');
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});


function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

let pdfText = '';
let speaking = false;
let speechRate = 1;
let speechPitch = 1;


function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 100);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}


function handleFile(file) {
    if (file.type !== 'application/pdf') {
        alert('Please upload a valid PDF file.');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        const pdfData = new Uint8Array(e.target.result);
        pdfjsLib.getDocument(pdfData).promise.then(pdf => {
            const numPages = pdf.numPages;
            document.getElementById('output').innerHTML = ''; 

            const processPage = (pageNum) => {
                pdf.getPage(pageNum).then(page => {
                    const scale = 1.5; 
                    const viewport = page.getViewport({ scale });
                    const canvas = document.createElement('canvas');
                    const context = canvas.getContext('2d');
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;
                    canvas.className = 'slide';

                    
                    page.render({ canvasContext: context, viewport: viewport }).promise.then(() => {
                        document.getElementById('output').appendChild(canvas);
                    });

                
                    page.getTextContent().then(textContent => {
                        const pageText = textContent.items.map(item => item.str).join(' ');
                        pdfText += pageText + '\n\n';
                    });
                });
            };

            
            for (let pageNum = 1; pageNum <= numPages; pageNum++) {
                processPage(pageNum);
            }

            
            readButton.disabled = false;
        });
    };
    reader.readAsArrayBuffer(file);
}


readButton.addEventListener('click', function() {
    if (speaking) {
        window.speechSynthesis.cancel();
        speaking = false;
        readButton.textContent = 'Read Aloud';
    } else {
        speakText(pdfText);
    }
});


function speakText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = speechRate;
    utterance.pitch = speechPitch;

    utterance.onend = () => {
        speaking = false;
        readButton.textContent = 'Read Aloud';
    };

    window.speechSynthesis.speak(utterance);
    speaking = true;
    readButton.textContent = 'Stop Reading';
}


function adjustRate(delta) {
    speechRate = Math.max(0.5, Math.min(2, speechRate + delta));
    showToast(`Speech rate: ${speechRate.toFixed(2)}x`);
}

function adjustPitch(delta) {
    speechPitch = Math.max(0.5, Math.min(2, speechPitch + delta));
    showToast(`Pitch: ${speechPitch.toFixed(2)}`);
}


const voiceControls = document.createElement('div');
voiceControls.className = 'voice-controls';
voiceControls.innerHTML = `
    <button class="voice-control" id="decreaseRate">🐌 Slower</button>
    <button class="voice-control" id="increaseRate">🐰 Faster</button>
    <button class="voice-control" id="decreasePitch">🔽 Lower Pitch</button>
    <button class="voice-control" id="increasePitch">🔼 Higher Pitch</button>
`;
document.querySelector('.container').insertBefore(voiceControls, readButton);


document.getElementById('decreaseRate').addEventListener('click', () => adjustRate(-0.25));
document.getElementById('increaseRate').addEventListener('click', () => adjustRate(0.25));
document.getElementById('decreasePitch').addEventListener('click', () => adjustPitch(-0.25));
document.getElementById('increasePitch').addEventListener('click', () => adjustPitch(0.25));
