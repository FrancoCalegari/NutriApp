document.addEventListener("DOMContentLoaded", async () => {
    const userDataJSON = localStorage.getItem("userData");

    if (!userDataJSON) {
        window.location.href = "login.html";
        return;
    }

    const userData = JSON.parse(userDataJSON);
    const apiUrl = "http://127.0.0.1:8000";
    const userId = userData.id;

    try {
        // Petición a la API para obtener los datos actualizados del usuario
        const response = await fetch(`${apiUrl}/users/${userId}`);
        if (!response.ok) throw new Error("Error al obtener los datos del usuario");

        const user = await response.json();

        // Actualizar campos de configuración
        document.getElementById("profile-username").textContent = user.username || "";
        document.getElementById("edit-email").value = user.email || "";
        document.getElementById("edit-profile-picture").value = user.profile_picture || "";
        document.getElementById("edit-weight").value = user.weight || "";
        document.getElementById("edit-calories").value = user.total_calories || "";

        const profileImg = document.getElementById("profile-picture");
        profileImg.src = user.profile_picture?.trim() !== "" ? user.profile_picture : "./assets/imgs/default-profile.png";

        // Rellenar datos en la vista principal (home)
        document.getElementById("welcome-username").textContent = user.username || "";
        document.getElementById("welcome-fullname").textContent = user.full_name || "";
        document.getElementById("welcome-height").textContent = user.height || "";
        document.getElementById("welcome-weight").textContent = user.weight || "";
        document.getElementById("welcome-email").textContent = user.email || "";

        const welcomeImg = document.getElementById("welcome-profile-picture");
        welcomeImg.src = user.profile_picture?.trim() !== "" ? user.profile_picture : "./assets/imgs/default-profile.png";

    } catch (error) {
        console.error("Error cargando datos del usuario:", error);
    }

    // Secciones a controlar
    const sections = {
        home: document.querySelector(".home"),
        recetas: document.querySelector(".recetas"),
        medicInfo: document.querySelector(".medic-info"),
        settings: document.querySelector(".settings-section")
    };

    // Botones
    const buttons = {
        home: document.getElementById("home-btn"),
        recetas: document.getElementById("recetas-btn"),
        medicInfo: document.getElementById("medic-info-btn"),
        settings: document.getElementById("settings-btn")
    };

    // Función para ocultar todas las secciones
    const hideAllSections = () => {
        Object.values(sections).forEach(section => {
            section.style.display = "none";
        });
    };

    // Mostrar solo home al inicio
    hideAllSections();
    sections.home.style.display = "block";

    // Eventos de los botones
    buttons.home.addEventListener("click", () => {
        hideAllSections();
        sections.home.style.display = "block";
    });

    buttons.recetas.addEventListener("click", () => {
        hideAllSections();
        sections.recetas.style.display = "block";
    });

    buttons.medicInfo.addEventListener("click", () => {
        hideAllSections();
        sections.medicInfo.style.display = "block";
    });

    buttons.settings.addEventListener("click", () => {
        hideAllSections();
        sections.settings.style.display = "block";
    });
});
