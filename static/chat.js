document.addEventListener("DOMContentLoaded", function () {
    const userInputElem = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const sendButton = document.getElementById("send-button");
    const notesTextarea = document.getElementById("notes-textarea");

    async function sendMessage() {
        const userInput = userInputElem.value.trim();
        if (!userInput) return;

        appendMessage("user", userInput);
        userInputElem.value = "";
        sendButton.disabled = true; // Disable send button while processing

        // Add animated typing indicator
        const typingBubble = appendMessage("ai", '<span class="typing-indicator">Thinking<span>.</span><span>.</span><span>.</span></span>');

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `user_input=${encodeURIComponent(userInput)}`
            });

            const data = await response.json();
            typingBubble.remove();
            appendMessage("ai", data.message.replace(/\n/g, "<br>"));
        } catch (error) {
            typingBubble.remove();
            console.error("Error:", error);
            appendMessage("ai", "<i>Sorry, something went wrong. Please try again.</i>");
        } finally {
            sendButton.disabled = false; // Re-enable send button after response
        }
    }

    async function clearMemory() {
        try {
            const response = await fetch("/purge", {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            });

            const data = await response.json();
            alert(data.message);
            chatBox.innerHTML = ""; // Clear chat log in UI
        } catch (error) {
            console.error("Error:", error);
        }
    }

    function clearNotes() {
        notesTextarea.value = ""; // Clear notes textarea
    }

    function appendMessage(sender, text) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);
        messageDiv.innerHTML = `<div class="${sender}">${text}</div>`;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageDiv;
    }

    userInputElem.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    window.sendMessage = sendMessage;
    window.clearMemory = clearMemory;
    window.clearNotes = clearNotes;
});
