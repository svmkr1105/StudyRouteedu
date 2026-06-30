function loadBSCC() {
    const searchInput = document.getElementById('bsccSearch');
    const search = searchInput ? searchInput.value : '';

    fetch(`${API_BASE}/bscc/?search=${search}`)
        .then(res => res.json())
        .then(data => {
            const grid = document.getElementById('bsccGrid');
            if (data.length === 0) {
                grid.innerHTML = '<p style="text-align:center;">No BSCC courses found.</p>';
                return;
            }
            grid.innerHTML = data.map(c => `
                <div class="bscc-card">
                    <h3>${c.course_name}</h3>
                    <p><strong>College:</strong> ${c.college_name}</p>
                    <p><strong>District:</strong> ${c.district}</p>
                    <p><strong>Eligibility:</strong> ${c.eligibility}</p>
                    <p><strong>Duration:</strong> ${c.duration}</p>
                </div>
            `).join('');
        })
        .catch(err => console.error('Error loading BSCC courses:', err));
}

document.addEventListener('DOMContentLoaded', loadBSCC);