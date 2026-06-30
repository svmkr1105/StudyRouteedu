function loadCourses() {
    const searchInput = document.getElementById('courseSearch');
    const search = searchInput ? searchInput.value : '';

    fetch(`${API_BASE}/courses/?search=${search}`)
        .then(res => res.json())
        .then(data => {
            const grid = document.getElementById('courseGrid');
            if (data.length === 0) {
                grid.innerHTML = '<p style="text-align:center;">No courses found.</p>';
                return;
            }
            grid.innerHTML = data.map(c => `
                <div class="course-card">
                    <h3>${c.name}</h3>
                    <p><strong>Duration:</strong> ${c.duration}</p>
                    <p><strong>Eligibility:</strong> ${c.eligibility}</p>
                    <p><strong>Fees:</strong> ${c.fees || 'N/A'}</p>
                    <p><strong>College:</strong> ${c.college_name || 'N/A'}</p>
                </div>
            `).join('');
        })
        .catch(err => console.error('Error loading courses:', err));
}

document.addEventListener('DOMContentLoaded', loadCourses);