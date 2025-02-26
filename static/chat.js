// static/js/chat.js

async function sendMessage() {
    const userInput = document.getElementById("userInput").value;

    const responseContainer = document.getElementById("response");
    responseContainer.innerHTML = ''; // Clear previous response

    const formData = new FormData();
    formData.append('user_input', userInput);

    const response = await fetch('/chat', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    const message = data.message;

    // Simulate typing animation in the front-end
    let index = 0;
    const typingSpeed = 50; // Milliseconds between characters
    function typeCharacter() {
        if (index < message.length) {
            responseContainer.innerHTML += message[index];  // Use innerHTML to allow HTML tags
            index++;
            setTimeout(typeCharacter, typingSpeed);
        }
    }

    typeCharacter();
}
