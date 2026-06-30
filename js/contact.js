function loadPartners() {
    const searchInput = document.getElementById('partnerSearch');
    const search = searchInput ? searchInput.value : '';

    fetch(`${API_BASE}/partners/?search=${search}`)
        .then(res => res.json())
        .then(data => {
            const grid = document.getElementById('partnerGrid');
            if (data.length === 0) {
                grid.innerHTML = '<p style="text-align:center;">No partners found.</p>';
                return;
            }
            grid.innerHTML = data.map(p => `
                <div class="partner-card">
                    <h3>${p.name}</h3>
                    <p><i class="fas fa-phone"></i> ${p.mobile}</p>
                    <p><i class="fas fa-location-dot"></i> ${p.district}</p>
                </div>
            `).join('');
        })
        .catch(err => console.error('Error loading partners:', err));
}

document.addEventListener('DOMContentLoaded', loadPartners);