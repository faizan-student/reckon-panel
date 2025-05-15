let currentChat = "support";
let chatData = {
    support: [],
    sales: []
};

let typingTimeout;
let isTyping = false;

function openChat(chatId) {
    currentChat = chatId;

    // Update header title
    document.getElementById("chatHeader").querySelector("h2").innerText = capitalize(chatId);

    // Remove .active class from all chat items
    document.querySelectorAll(".chat-item").forEach(item => {
        item.classList.remove("active");
    });

    // Add .active class to the clicked chat
    const selectedChat = document.querySelector(`.chat-item[data-chat="${chatId}"]`);
    if (selectedChat) {
        selectedChat.classList.add("active");
    }

    renderMessages();
}


function renderMessages() {
    const container = document.getElementById("chat-messages");
    container.innerHTML = "";
    chatData[currentChat].forEach(msg => {
        const div = document.createElement("div");
        div.className = `message ${msg.from}`;

        let ticks = "";
        if (msg.from === "sent") {
            ticks = `<span class="tick-status">${msg.status || "•"}</span>`;
        }

        div.innerHTML = `<div>${msg.text}</div><div class="timestamp">${msg.time} ${ticks}</div>`;
        container.appendChild(div);
    });
    container.scrollTop = container.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById("messageInput");
    const text = input.value.trim();
    if (text === "") return;

    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const message = {
        from: "sent",
        text: text,
        time: time,
        status: "•"
    };

    chatData[currentChat].push(message);
    input.value = "";
    renderMessages();

    setTimeout(() => {
        message.status = "✔✔"; // delivered
        renderMessages();
    }, 1000);

    setTimeout(() => {
        message.status = `<span style="color:#34b7f1;">✔✔</span>`; // read
        renderMessages();
    }, 2000);

    setTimeout(() => {
        receiveMessage("Auto reply from " + capitalize(currentChat));
    }, 3000);
}

function receiveMessage(text) {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    chatData[currentChat].push({
        from: "received",
        text: text,
        time: time
    });

    renderMessages();
}

function sendFile(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const message = {
            from: "sent",
            text: `<img src="${e.target.result}" style="max-width:100%; border-radius:10px;" />`,
            time: time,
            status: "•"
        };

        chatData[currentChat].push(message);
        renderMessages();

        setTimeout(() => {
            message.status = "✔✔";
            renderMessages();
        }, 1000);

        setTimeout(() => {
            message.status = `<span style="color:#34b7f1;">✔✔</span>`;
            renderMessages();
        }, 2000);

        setTimeout(() => {
            receiveMessage("Nice pic from " + capitalize(currentChat));
        }, 3000);
    };
    reader.readAsDataURL(file);
}

function addEmoji(emoji) {
    const input = document.getElementById("messageInput");
    input.value += emoji;
    input.focus();
}

function showTypingIndicator() {
    const typingIndicator = document.getElementById("typing-indicator");
    typingIndicator.style.display = "block";
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
        typingIndicator.style.display = "none";
    }, 2000);
}

function capitalize(word) {
    return word.charAt(0).toUpperCase() + word.slice(1);
}
