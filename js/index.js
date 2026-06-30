// Stats Animation
document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('.stat-number');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        let current = 0;
        const increment = target / 60;
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.innerText = Math.ceil(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.innerText = target;
            }
        };
        updateCounter();
    });

    // Load Testimonials
    fetch(`${API_BASE}/feedbacks/?approved=true`)
        .then(res => res.json())
        .then(data => {
            const grid = document.getElementById('testimonialGrid');
            grid.innerHTML = data.slice(0, 4).map(fb => `
                <div class="testimonial-card">
                    <p>"${fb.message}"</p>
                    <h4>- ${fb.name}, ${fb.district}</h4>
                    <div>${'⭐'.repeat(fb.rating)}</div>
                </div>
            `).join('');
        })
        .catch(err => console.error('Error loading testimonials:', err));
});