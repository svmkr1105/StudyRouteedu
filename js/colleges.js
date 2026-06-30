function loadColleges() {
    const searchInput = document.getElementById('collegeSearch');
    const districtInput = document.getElementById('districtFilter');

    const search = searchInput ? searchInput.value : '';
    const district = districtInput ? districtInput.value : '';

    fetch(`${API_BASE}/colleges/?search=${search}&district=${district}`)
        .then(res => res.json())
        .then(data => {
            const grid = document.getElementById('collegeGrid');
            if (data.length === 0) {
                grid.innerHTML = '<p style="text-align:center;">No colleges found.</p>';
                return;
            }
            grid.innerHTML = data.map(c => `
                <div class="college-card">
                    <h3>${c.name}</h3>
                    <p><i class="fas fa-location-dot"></i> ${c.district}</p>
                    <p>${c.description || ''}</p>
                    <p><strong>Courses:</strong> ${c.courses ? c.courses.join(', ') : 'N/A'}</p>
                </div>
            `).join('');
        })
        .catch(err => console.error('Error loading colleges:', err));
}

document.addEventListener('DOMContentLoaded', loadColleges);