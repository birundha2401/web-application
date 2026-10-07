// Vanilla JS Health Check Client

document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
});

function checkHealth() {
    const backendBadge = document.getElementById('backend-status');
    const dbBadge = document.getElementById('db-status');
    const lastChecked = document.getElementById('last-checked');

    // Set pending state
    backendBadge.className = 'badge badge-pending';
    backendBadge.textContent = 'Checking...';
    dbBadge.className = 'badge badge-pending';
    dbBadge.textContent = 'Checking...';

    fetch('/api/health')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Update Backend Status
            if (data.status === 'UP') {
                backendBadge.className = 'badge badge-success';
                backendBadge.textContent = 'Online - UP';
            } else {
                backendBadge.className = 'badge badge-danger';
                backendBadge.textContent = 'DOWN';
            }

            // Update Database Status
            if (data.database === 'CONNECTED') {
                dbBadge.className = 'badge badge-success';
                dbBadge.textContent = 'CONNECTED';
            } else {
                dbBadge.className = 'badge badge-danger';
                dbBadge.textContent = 'DISCONNECTED';
            }

            lastChecked.textContent = new Date().toLocaleTimeString();
        })
        .catch(error => {
            console.error('Health check failed:', error);
            backendBadge.className = 'badge badge-danger';
            backendBadge.textContent = 'Offline / Error';
            dbBadge.className = 'badge badge-danger';
            dbBadge.textContent = 'Unavailable';
            lastChecked.textContent = new Date().toLocaleTimeString();
        });
}