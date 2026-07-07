// Navbar Toggle
document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('navToggle');
    const links = document.getElementById('navLinks');
    if (toggle && links) {
        toggle.addEventListener('click', () => {
            links.classList.toggle('active');
        });
    }
});

// API Base URL

// const API_BASE = 'http://localhost:8000/api';
const API_BASE = 'https://studyroute-backend.onrender.com/api';