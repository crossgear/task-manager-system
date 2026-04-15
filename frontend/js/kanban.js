import { apiRequest } from "./api.js";
let currentTask = null;

if (!localStorage.getItem("token")) {
    window.location.href = "/";
}

const params = new URLSearchParams(window.location.search);
const projectId = params.get("id");

function clearColumns() {
    document.getElementById("backlog").innerHTML = "";
    document.getElementById("in_progress").innerHTML = "";
    document.getElementById("done").innerHTML = "";
}

function renderTask(task) {
    console.log("Rendering task:", task);
    const div = document.createElement("div");
    div.className = "task";

    div.innerHTML = `
    <strong>${task.title}</strong>
    <br>
    <small>${task.assigned_to_username || ""}</small>`;

    div.onclick = () => openModal(task);

    div.innerText = task.title;

    div.draggable = true;

    div.ondragstart = (event) => {
        event.dataTransfer.setData("taskId", task.id);
    };

    document.getElementById(task.status).appendChild(div);
}

async function loadTasks() {
    const tasks = await apiRequest(`/projects/${projectId}/tasks/`);

    clearColumns();

    tasks.forEach(renderTask);
}

async function moveTask(task) {
    let newStatus = "backlog";

    if (task.status === "backlog") newStatus = "in_progress";
    else if (task.status === "in_progress") newStatus = "done";
    else if (task.status === "done") newStatus = "backlog";
    try {
        await apiRequest(`/tasks/${task.id}/`, "PATCH", {
            status: newStatus
        });
    } catch (error) {
        console.error("Error moving task:", error);
    }

    loadTasks();
}

window.createTask = async function () {
    const title = document.getElementById("taskTitle").value;

    if (!title) return;

    await apiRequest(`/projects/${projectId}/tasks/`, "POST", {
        title
    });

    document.getElementById("taskTitle").value = "";
    loadTasks();
};

loadTasks();

window.allowDrop = function (event) {
    event.preventDefault();
};

window.drop = async function (event, newStatus) {
    event.preventDefault();

    console.log("DROP FUNCIONA");

    const taskId = event.dataTransfer.getData("taskId");

    console.log("DROP:", taskId, newStatus);

    try {
        const res = await apiRequest(`/tasks/${taskId}/`, "PATCH", {
            status: newStatus
        });

        console.log("PATCH OK:", res);

        await loadTasks();

    } catch (err) {
        console.error("PATCH ERROR:", err);
        alert(JSON.stringify(err));
    }
};

async function loadMembers() {
    const members = await apiRequest(`/projects/${projectId}/members-list/`);

    const select = document.getElementById("editAssigned");
    select.innerHTML = `<option value="">Unassigned</option>`;

    members.forEach(user => {
        const option = document.createElement("option");
        option.value = user.id;
        option.innerText = user.username;
        select.appendChild(option);
    });
}

window.openModal = async function (task) {
    currentTask = task;

    document.getElementById("editTitle").value = task.title;
    document.getElementById("editDescription").value = task.description || "";
    document.getElementById("editStatus").value = task.status;

    await loadMembers();

    document.getElementById("editAssigned").value = task.assigned_to || "";

    document.getElementById("taskModal").style.display = "flex";
};

window.closeModal = function () {
    document.getElementById("taskModal").style.display = "none";
};

window.saveTask = async function () {
    const title = document.getElementById("editTitle").value;
    const status = document.getElementById("editStatus").value;
    const description = document.getElementById("editDescription").value;

    try {
        await apiRequest(`/tasks/${currentTask.id}/`, "PATCH", {
            title,
            description,
            status,
            assigned_to: document.getElementById("editAssigned").value || null
        });

        closeModal();
        loadTasks();

    } catch (err) {
        console.error(err);
        alert("Error updating task");
    }
};

window.deleteTask = async function () {
    if (!currentTask) return;

    const confirmDelete = confirm("Delete this task?");

    if (!confirmDelete) return;

    try {
        await apiRequest(`/tasks/${currentTask.id}/`, "DELETE");

        closeModal();
        loadTasks();

    } catch (err) {
        console.error(err);
        alert("Error deleting task");
    }
};


window.logout = function () {
    localStorage.removeItem("token");
    window.location.href = "/";
};


