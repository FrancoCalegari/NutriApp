const apiUrl = "http://127.0.0.1:8000";

document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("register-username").value;
    const email = document.getElementById("register-email").value;
    const profile_picture = document.getElementById("register-profile").value;
    const password = document.getElementById("register-password").value;

    const res = await fetch(`${apiUrl}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, profile_picture, password })
    });

    const data = await res.json();
    document.getElementById("register-result").textContent = data.msg || data.detail;

    if (res.ok) {
        document.getElementById("user-details-form").classList.remove("hidden");
    }
});

document.getElementById("user-details-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const weight = parseFloat(document.getElementById("user-weight").value);
    const total_calories = parseInt(document.getElementById("user-calories").value);
    const username = document.getElementById("register-username").value;

    const res = await fetch(`${apiUrl}/update_user`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, weight, total_calories })
    });

    const data = await res.json();
    document.getElementById("details-result").textContent = data.msg || data.detail;
});

document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const res = await fetch(`${apiUrl}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (res.ok) {
        // Guardar datos usuario en localStorage
        localStorage.setItem("userData", JSON.stringify(data));
        // Redirigir a profile.html
        window.location.href = "profile.html";
    } else {
        document.getElementById("login-result").textContent = data.detail || "Error en el login";
    }
});
