const API_BASE = "http://127.0.0.1:8000/api";
const tokenKey = "jwtToken";

document.getElementById("send-btn").addEventListener("click", sendMessage);

function logoutUser() {
    localStorage.removeItem(tokenKey);
    localStorage.removeItem("chatHistory");
    window.location.href = "/login/";
}

function clearHistory() {
    document.getElementById("chat-box").innerHTML = '';
    localStorage.removeItem("chatHistory");
    addMessage("Hello! I’m your AI assistant. How can I help you today?", "bot");
}

async function sendMessage() {
    const token = localStorage.getItem(tokenKey);
    if (!token) {
        alert("Please log in first!");
        window.location.href = "/login/";
        return;
    }

    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    const thinkingMsg = addMessage("...", "bot");

    try {
        const response = await fetch(`${API_BASE}/chat/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ message })
        });
        const data = await response.json();

        thinkingMsg.remove();
        addMessage(data.response || "Error from AI", "bot");
        updateTokenCount();
        saveChatHistory();
    } catch {
        thinkingMsg.remove();
        addMessage("Error connecting to server", "bot");
    }
}

function addMessage(text, sender) {
    const chatBox = document.getElementById("chat-box");
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;

    if (sender === "bot") {
        msg.innerHTML = marked.parse(text);  // Render markdown for bot
    } else {
        msg.innerText = text; // User text stays plain
    }

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msg;
}


async function updateTokenCount() {
    const token = localStorage.getItem(tokenKey);
    if (!token) return;
    try {
        const res = await fetch(`${API_BASE}/users/tokens/`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        document.getElementById("token-count").innerText = `Tokens: ${data.tokens}`;
    } catch {
        document.getElementById("token-count").innerText = "Tokens: N/A";
    }
}

function saveChatHistory() {
    const chatBox = document.getElementById("chat-box").innerHTML;
    localStorage.setItem("chatHistory", chatBox);
}

function loadChatHistory() {
    const saved = localStorage.getItem("chatHistory");
    if (saved) {
        document.getElementById("chat-box").innerHTML = saved;
    }
}

window.onload = function() {
    loadChatHistory();
    updateTokenCount();
};


