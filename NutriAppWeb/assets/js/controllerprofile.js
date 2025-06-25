document.addEventListener("DOMContentLoaded", () => {
    

    const userDataJSON = localStorage.getItem("userData");

    if (!userDataJSON) {
        window.location.href = "login.html";
        return;
    }

    const userData = JSON.parse(userDataJSON);
    const apiUrl = "http://127.0.0.1:8000";

    document.getElementById("profile-username").textContent = userData.username || "";
    document.getElementById("edit-email").value = userData.email || "";
    document.getElementById("edit-profile-picture").value = userData.profile_picture || "";
    document.getElementById("edit-weight").value = userData.weight || "";
    document.getElementById("edit-calories").value = userData.total_calories || "";

    const profileImg = document.getElementById("profile-picture");
    profileImg.src = userData.profile_picture?.trim() !== "" ? userData.profile_picture : "./assets/imgs/default-profile.png";

    document.getElementById("logout-btn").addEventListener("click", () => {
        localStorage.removeItem("userData");
        window.location.href = "login.html";
    });

    document.getElementById("update-btn").addEventListener("click", async () => {
        const email = document.getElementById("edit-email").value;
        const profile_picture = document.getElementById("edit-profile-picture").value;
        const weight = parseFloat(document.getElementById("edit-weight").value);
        const total_calories = parseInt(document.getElementById("edit-calories").value);

        const updatedUser = {
            username: userData.username,
            email,
            profile_picture,
            weight,
            total_calories
        };

        const res = await fetch(`${apiUrl}/update_profile`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedUser)
        });

        const result = await res.json();
        document.getElementById("update-result").textContent = result.msg || result.detail;

        if (res.ok) {
            localStorage.setItem("userData", JSON.stringify(updatedUser));
            window.location.reload();
        }
    });
});


