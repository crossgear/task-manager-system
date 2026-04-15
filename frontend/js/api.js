const API_URL = "http://127.0.0.1:8000/api/v1";

function getToken() {
    return localStorage.getItem("token");
}

export async function apiRequest(endpoint, method = "GET", data = null) {
    const options = {
        method,
        headers: {
            "Content-Type": "application/json"
        }
    };

    const token = getToken();

    if (token) {
        options.headers["Authorization"] = `Token ${token}`;
    }

    if (data) {
        options.body = JSON.stringify(data);
    }

    const res = await fetch(`${API_URL}${endpoint}`, options);

    if (res.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "/";
        return;
    }

    return res.json();
}