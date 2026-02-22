/**
 * Authentication Logic for Oscar Legal Practitioners
 */

const API_BASE_URL = '/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signup-form');
    const signinForm = document.getElementById('signin-form');

    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const userData = {
                full_name: document.getElementById('full_name').value,
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                role: signupForm.querySelector('input[name="role"]:checked').value
            };

            try {
                const response = await fetch(`${API_BASE_URL}/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(userData)
                });

                if (response.ok) {
                    alert('Registration successful! Please sign in.');
                    window.location.href = 'signin.html';
                } else {
                    const error = await response.json();
                    alert(`Registration failed: ${error.detail || 'Unknown error'}`);
                }
            } catch (err) {
                console.error('Signup error:', err);
                alert('An error occurred during registration. Please try again.');
            }
        });
    }

    if (signinForm) {
        signinForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // OAuth2 expects form data for login
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            try {
                const response = await fetch(`${API_BASE_URL}/auth/login`, {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    localStorage.setItem('access_token', data.access_token);
                    localStorage.setItem('token_type', data.token_type);

                    // Retrieve user info and store it
                    await fetchUserInfo(data.access_token);

                    window.location.href = 'dashboard.html';
                } else {
                    const error = await response.json();
                    alert(`Login failed: ${error.detail || 'Invalid credentials'}`);
                }
            } catch (err) {
                console.error('Login error:', err);
                alert('An error occurred during login. Please try again.');
            }
        });
    }

    async function fetchUserInfo(token) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/me`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                const user = await response.json();
                localStorage.setItem('user', JSON.stringify(user));
            }
        } catch (err) {
            console.error('Error fetching user info:', err);
        }
    }
});
