// // Navbar Toggle
// document.addEventListener('DOMContentLoaded', function() {
//     const toggle = document.getElementById('navToggle');
//     const links = document.getElementById('navLinks');
//     if (toggle && links) {
//         toggle.addEventListener('click', () => {
//             links.classList.toggle('active');
//         });
//     }
// });

// // API Base URL

// // const API_BASE = 'http://localhost:8000/api';
// const API_BASE = 'https://studyrouteedu.onrender.com/api'




// ===== API BASE URL =====
const API_BASE = 'https://studyrouteedu.onrender.com/api';

// ===== NAVBAR TOGGLE =====
document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('navToggle');
    const links = document.getElementById('navLinks');
    if (toggle && links) {
        toggle.addEventListener('click', () => {
            links.classList.toggle('active');
        });
    }
});