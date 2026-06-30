const API = 'http://localhost:8000/api';
let token = localStorage.getItem('adminToken');

function getHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// Login
async function adminLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const res = await fetch(`${API}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (res.ok) {
        localStorage.setItem('adminToken', data.access_token);
        token = data.access_token;
        window.location.href = 'dashboard.html';
    } else {
        alert('Login failed');
    }
}

// Dashboard Stats
async function loadDashboard() {
    const res = await fetch(`${API}/admin/stats`, { headers: getHeaders() });
    const data = await res.json();
    document.getElementById('totalColleges').innerText = data.colleges || 0;
    document.getElementById('totalCourses').innerText = data.courses || 0;
    document.getElementById('totalBSCC').innerText = data.bscc || 0;
    document.getElementById('totalPartners').innerText = data.partners || 0;
    document.getElementById('totalFeedbacks').innerText = data.feedbacks || 0;
}

// Generic CRUD helpers
async function fetchItems(endpoint, containerId) {
    const res = await fetch(`${API}/${endpoint}`, { headers: getHeaders() });
    const data = await res.json();
    // Render logic varies, but this is a placeholder
    return data;
}

// Add/Edit/Delete functions follow similar pattern...
// For brevity, these can be expanded.