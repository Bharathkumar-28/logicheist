const messagesContainer = document.getElementById('messages');
const userInput = document.getElementById('user-input');
const micBtn = document.getElementById('mic-btn');
const sendBtn = document.getElementById('send-btn');
let isListening = false;

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US';

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    userInput.value = transcript;
    toggleVoiceInput();
};

function toggleVoiceInput() {
    isListening = !isListening;
    isListening ? recognition.start() : recognition.stop();
    micBtn.classList.toggle('active', isListening);
}

function appendMessage(role, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    messageDiv.textContent = text;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTo({ top: messagesContainer.scrollHeight, behavior: 'smooth' });
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    appendMessage('outgoing', text);
    userInput.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await response.json();
        appendMessage('incoming', data.reply);
    } catch (error) {
        appendMessage('incoming', 'Error processing your request');
    }
}

// Event Listeners
sendBtn.addEventListener('click', sendMessage);
micBtn.addEventListener('click', toggleVoiceInput);
userInput.addEventListener('keypress', (e) => e.key === 'Enter' && sendMessage());