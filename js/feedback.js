// // Star Rating
// document.addEventListener('DOMContentLoaded', () => {
//     const stars = document.querySelectorAll('.star-rating i');
//     const ratingInput = document.getElementById('fbRating');
//     stars.forEach(star => {
//         star.addEventListener('click', function() {
//             const val = parseInt(this.dataset.value);
//             ratingInput.value = val;
//             stars.forEach(s => s.classList.remove('active'));
//             for (let i = 0; i < val; i++) {
//                 stars[i].classList.add('active');
//                 stars[i].className = 'fa-solid fa-star active';
//             }
//             for (let i = val; i < 5; i++) {
//                 stars[i].className = 'fa-regular fa-star';
//             }
//         });
//     });

//     // Submit Feedback
//     document.getElementById('feedbackForm').addEventListener('submit', async(e) => {
//         e.preventDefault();
//         const name = document.getElementById('fbName').value;
//         const district = document.getElementById('fbDistrict').value;
//         const rating = parseInt(document.getElementById('fbRating').value);
//         const message = document.getElementById('fbMessage').value;

//         if (!name || !district || rating === 0 || !message) {
//             alert('Please fill all fields and give a rating.');
//             return;
//         }

//         const res = await fetch(`${API_BASE}/feedbacks/`, {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ name, district, rating, message, approved: false })
//         });
//         if (res.ok) {
//             alert('Thank you for your feedback! It will be reviewed.');
//             document.getElementById('feedbackForm').reset();
//             document.querySelectorAll('.star-rating i').forEach(s => s.className = 'fa-regular fa-star');
//         } else {
//             alert('Error submitting feedback.');
//         }
//     });

//     // Load approved feedbacks
//     fetch(`${API_BASE}/feedbacks/?approved=true`)
//         .then(res => res.json())
//         .then(data => {
//             const list = document.getElementById('feedbackList');
//             list.innerHTML = data.map(fb => `
//                 <div class="testimonial-card">
//                     <p>${fb.message}</p>
//                     <h4>${fb.name}, ${fb.district}</h4>
//                     <div>${'⭐'.repeat(fb.rating)}</div>
//                 </div>
//             `).join('');
//         });
// });

// const API_BASE = 'http://localhost:8000/api';

// // ===== STAR RATING =====
// document.addEventListener('DOMContentLoaded', function() {
//     const stars = document.querySelectorAll('.star-rating i');
//     const ratingInput = document.getElementById('fbRating');

//     stars.forEach(star => {
//         star.addEventListener('click', function() {
//             const val = parseInt(this.dataset.value);
//             ratingInput.value = val;
//             stars.forEach(s => {
//                 s.className = 'fa-regular fa-star';
//             });
//             for (let i = 0; i < val; i++) {
//                 stars[i].className = 'fa-solid fa-star active';
//             }
//         });
//     });

//     // ===== SUBMIT FEEDBACK =====
//     document.getElementById('feedbackForm').addEventListener('submit', async function(e) {
//         e.preventDefault();
//         const name = document.getElementById('fbName').value.trim();
//         const district = document.getElementById('fbDistrict').value.trim();
//         const rating = parseInt(document.getElementById('fbRating').value);
//         const message = document.getElementById('fbMessage').value.trim();

//         if (!name || !district || rating === 0 || !message) {
//             alert('Please fill all fields and give a rating.');
//             return;
//         }

//         try {
//             const response = await fetch(`${API_BASE}/feedbacks/`, {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify({ name, district, rating, message, approved: false })
//             });
//             if (response.ok) {
//                 alert('✅ Thank you for your feedback! It will be reviewed.');
//                 document.getElementById('feedbackForm').reset();
//                 document.querySelectorAll('.star-rating i').forEach(s => s.className = 'fa-regular fa-star');
//                 loadApprovedFeedbacks();
//             } else {
//                 alert('❌ Error submitting feedback');
//             }
//         } catch (error) {
//             alert('❌ Server error. Please try again.');
//         }
//     });

//     // ===== LOAD APPROVED FEEDBACKS =====
//     loadApprovedFeedbacks();
// });

// async function loadApprovedFeedbacks() {
//     try {
//         const response = await fetch(`${API_BASE}/feedbacks/?approved=true`);
//         const feedbacks = await response.json();
//         const list = document.getElementById('feedbackList');

//         if (feedbacks.length === 0) {
//             list.innerHTML = '<p style="text-align:center; color:#94a3b8; padding:40px;">No approved feedbacks yet.</p>';
//             return;
//         }

//         list.innerHTML = feedbacks.map(fb => `
//             <div class="testimonial-card">
//                 <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
//                     <h4>${fb.name}</h4>
//                     <span style="font-size:0.85rem; color:#94a3b8;">${fb.district}</span>
//                 </div>
//                 <div style="color:#f59e0b; margin:6px 0;">${'⭐'.repeat(fb.rating)}</div>
//                 <p style="font-style:italic;">"${fb.message}"</p>
//                 ${fb.reply ? `
//                     <div style="background:#dbeafe; padding:10px 14px; border-radius:8px; margin-top:8px; border-left:3px solid #2563eb;">
//                         <strong style="color:#2563eb;">💬 Admin Reply:</strong>
//                         <span style="color:#334155;">${fb.reply}</span>
//                     </div>
//                 ` : ''}
//             </div>
//         `).join('');
//     } catch (error) {
//         console.error('Error loading feedbacks:', error);
//         document.getElementById('feedbackList').innerHTML = '<p style="text-align:center; color:#ef4444;">Error loading feedbacks</p>';
//     }
// }






<
script >
    const API_BASE = 'http://localhost:8000/api';

// ===== STAR RATING =====
document.querySelectorAll('.star-rating i').forEach(star => {
    star.addEventListener('click', function() {
        const val = parseInt(this.dataset.value);
        document.getElementById('fbRating').value = val;

        document.querySelectorAll('.star-rating i').forEach(s => {
            s.className = 'fa-regular fa-star';
        });
        for (let i = 0; i < val; i++) {
            document.querySelectorAll('.star-rating i')[i].className = 'fa-solid fa-star active';
        }
    });
});

// ===== SUBMIT FEEDBACK =====
document.getElementById('feedbackForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const name = document.getElementById('fbName').value.trim();
    const district = document.getElementById('fbDistrict').value.trim();
    const rating = parseInt(document.getElementById('fbRating').value);
    const message = document.getElementById('fbMessage').value.trim();

    console.log('📤 Submitting feedback:', { name, district, rating, message });

    if (!name || !district || rating === 0 || !message) {
        alert('Please fill all fields and give a rating.');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/feedbacks/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, district, rating, message, approved: false })
        });

        const data = await response.json();
        console.log('📥 Response:', data);

        if (response.ok) {
            alert('✅ Thank you for your feedback! It will be reviewed.');
            document.getElementById('feedbackForm').reset();
            document.querySelectorAll('.star-rating i').forEach(s => s.className = 'fa-regular fa-star');
            document.getElementById('fbRating').value = 0;
            loadApprovedFeedbacks();
        } else {
            alert('❌ Error submitting feedback: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('❌ Error:', error);
        alert('❌ Server error. Please try again.');
    }
});

// ===== LOAD APPROVED FEEDBACKS =====
async function loadApprovedFeedbacks() {
    try {
        const response = await fetch(`${API_BASE}/feedbacks/?approved=true`);
        const feedbacks = await response.json();
        const list = document.getElementById('feedbackList');

        if (feedbacks.length === 0) {
            list.innerHTML = '<p style="text-align:center; color:#94a3b8; padding:40px;">No approved feedbacks yet.</p>';
            return;
        }

        list.innerHTML = feedbacks.map(fb => `
                <div class="testimonial-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                        <h4>${fb.name}</h4>
                        <span style="font-size:0.85rem; color:#94a3b8;">${fb.district}</span>
                    </div>
                    <div style="color:#f59e0b; margin:6px 0;">${'⭐'.repeat(fb.rating)}</div>
                    <p style="font-style:italic;">"${fb.message}"</p>
                    ${fb.reply ? `
                        <div style="background:#dbeafe; padding:10px 14px; border-radius:8px; margin-top:8px; border-left:3px solid #2563eb;">
                            <strong style="color:#2563eb;">💬 Admin Reply:</strong>
                            <span style="color:#334155;">${fb.reply}</span>
                        </div>
                    ` : ''}
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading feedbacks:', error);
            document.getElementById('feedbackList').innerHTML = '<p style="text-align:center; color:#ef4444;">Error loading feedbacks</p>';
        }
    }

    // ===== LOAD ON PAGE LOAD =====
    document.addEventListener('DOMContentLoaded', function() {
        loadApprovedFeedbacks();
        console.log('✅ Feedback page loaded');
    });
</script>