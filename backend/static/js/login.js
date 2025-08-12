const API_BASE = "http://127.0.0.1:8000/api";

async function loginUser() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const statusEl = document.getElementById("status");

    if (!username || !password) {
        statusEl.innerText = "Please enter username and password";
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/token/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();

        if (data.access) {
            localStorage.setItem("jwtToken", data.access);
            statusEl.innerText = " Login successful! Redirecting...";
            setTimeout(() => {
                window.location.href = "/chat-ui/";
            }, 1000);
        } else {
            statusEl.innerText = " Invalid login credentials";
        }
    } catch (error) {
        statusEl.innerText = "Error connecting to server";
    }
}
