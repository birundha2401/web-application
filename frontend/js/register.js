document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('register-form');
    const messageDiv = document.getElementById('form-message');

    form.addEventListener('submit', (e) => {
        e.preventDefault(); // Stop standard form submission

        messageDiv.className = 'message hidden';

        const data = {
            name: document.getElementById('name').value,
            phone: document.getElementById('phone').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value
        };

        fetch('/api/register', {
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
                if (status === 201) {
                    messageDiv.textContent = 'Registration successful! (Login not yet implemented)';
                    messageDiv.className = 'message success';
                    form.reset(); // clear form fields
                } else if (status === 409) {
                    messageDiv.textContent = 'Error: Email already exists.';
                    messageDiv.className = 'message error';
                } else {
                    messageDiv.textContent = body.error || 'An error occurred during registration.';
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