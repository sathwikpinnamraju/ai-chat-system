const API_BASE = "http://127.0.0.1:8000/api";

async function registerUser() {
    const username = document.getElementById("new-username").value.trim();
    const password = document.getElementById("new-password").value.trim();

    if (!username || !password) {
        alert("Please fill all fields");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/users/register/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();
        if (res.ok) {
            alert("Account created successfully! Please login.");
            window.location.href = "/login/";
        } else {
            alert(data.error || "Registration failed");
        }
    } catch (error) {
        alert("Error connecting to server");
    }
}
