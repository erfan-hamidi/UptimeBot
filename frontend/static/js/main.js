// frontend/static/js/main.js
document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/yourmodel/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('data-container');
            data.forEach(item => {
                const p = document.createElement('p');
                p.textContent = item.name; // جایگزین با فیلدهای مدل خود
                container.appendChild(p);
            });
        })
        .catch(error => console.error('Error:', error));
});
