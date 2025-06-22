// To hide messages
function messagesHider() {
    const message = document.getElementById('message');
    message.style.display = 'none';
}

const interval = setInterval(messagesHider, 5000);
// End