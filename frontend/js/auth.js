import { apiRequest } from "./api.js";

// Check if user is already logged in
if (localStorage.getItem("token") && window.location.pathname === "/") {
    window.location.href = "/dashboard/";
}

document.addEventListener("DOMContentLoaded", () => {
    // login form is only on index.html, so we check if the elements exist before adding event listeners
    window.login = async function () {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        try {
            const data = await apiRequest("/auth/login/", "POST", {
                username,
                password
            });

            // Save token to localStorage
            localStorage.setItem("token", data.token);

            // Redirect to dashboard
            window.location.href = "/dashboard";

        } catch (err) {
            document.getElementById("error").innerText = "Login failed";
        }
    };
    // Register form is only on register.html, so we check if the element exists before adding event listener
    document.getElementById("registerBtn")?.addEventListener("click", async () => {
        console.log("CLICK REGISTER"); //debug

        const username = document.getElementById("regUsername").value.trim();
        const password = document.getElementById("regPassword").value.trim();
        const errorEl = document.getElementById("error");

        errorEl.innerText = "";

        if (!username || !password) {
            errorEl.innerText = "Username and password required";
            return;
        }

        try {
            await apiRequest("/auth/register/", "POST", {
                username,
                password
            });

            errorEl.style.color = "green";
            errorEl.innerText = "User created";

        } catch (err) {
            console.error(err);
            errorEl.innerText = err?.detail || "Error registering";
        }
    });

});