import { apiRequest } from "./api.js";

// Redirect to login if not authenticated
const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "/";
}

async function loadProjects() {
    const data = await apiRequest("/projects/");
    const projects = data.results || data;
    //console.log(projects);

    const container = document.getElementById("projects");
    container.innerHTML = "";

    projects.forEach(renderProject);

    /*projects.forEach(p => {
        const li = document.createElement("li");
        li.innerText = p.name;

        li.onclick = () => {
            window.location.href = `/project?id=${p.id}`;
        };

        list.appendChild(li);
    });*/
}

function renderProject(project) {
    const div = document.createElement("div");
    div.className = "column";

    div.innerHTML = `
        <h3>${project.name}</h3>
        <p style="color: gray;">${project.description || "No description"}</p>
        <button class="delete-btn">Delete</button>
    `;

    div.querySelector(".delete-btn").addEventListener("click", async (e) => {
        e.stopPropagation();

        const confirmDelete = confirm("Delete this project?");

        if (!confirmDelete) return;

        try {
            await apiRequest(`/projects/${project.id}/`, "DELETE");
            loadProjects();

        } catch (err) {
            console.error(err);
            alert("Error deleting project");
        }
    });

    div.onclick = () => {
        window.location.href = `/project/?id=${project.id}`;
    };

    document.getElementById("projects").appendChild(div);
}

window.createProject = async function () {
    const name = prompt("Project name");

    if (!name) return;

    await apiRequest("/projects/", "POST", { name });

    loadProjects();
};

window.logout = function () {
    localStorage.removeItem("token");
    window.location.href = "/";
};

loadProjects();