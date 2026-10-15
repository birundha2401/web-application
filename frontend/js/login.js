document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    const messageDiv = document.getElementById('form-message');

    form.addEventListener('submit', (e) => {
        e.preventDefault(); // Stop standard form submission

        messageDiv.className = 'message hidden';

        const data = {
            email: document.getElementById('email').value,
            password: document.getElementById('password').value
        };

        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                return response.json().then(json => ({ status: response.status, body: json }));
            })
            .then(({ status, body }) => {
                if (status === 200) {
                    // Success
                    messageDiv.textContent = body.message || 'Login successful!';
                    messageDiv.className = 'message success';
                    form.reset();
                } else if (status === 401) {
                    // Authentication Failed
                    messageDiv.textContent = body.error || 'Invalid email or password.';
                    messageDiv.className = 'message error';
                } else {
                    // Other server errors
                    messageDiv.textContent = body.error || 'An error occurred during login.';
                    messageDiv.className = 'message error';
                }
            })
            .catch(err => {
                messageDiv.textContent = 'Network error. Make sure the backend is running.';
                messageDiv.className = 'message error';
                console.error(err);
            });
    });
});