// frontend/static/js/main.js
// document.addEventListener('DOMContentLoaded', function () {
//     fetch('/api/yourmodel/')
//         .then(response => response.json())
//         .then(data => {
//             const container = document.getElementById('data-container');
//             data.forEach(item => {
//                 const p = document.createElement('p');
//                 p.textContent = item.name; // جایگزین با فیلدهای مدل خود
//                 container.appendChild(p);
//             });
//         })
//         .catch(error => console.error('Error:', error));
// });


async function register(username, password, email) {
    const response = await fetch("http://127.0.0.1:8000/account/registration/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password1: password,
            password2: password,
            email: email
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error);
    }

    const data = await response.json();
    localStorage.setItem('accessToken', data.access);
    localStorage.setItem('refreshToken', data.refresh);
    return data;
}

async function login(username, password) {
    const response = await fetch('http://127.0.0.1:8000/account/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: username,
            password: password
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error);
    }

    const data = await response.json();
    localStorage.setItem('accessToken', data.access);
    localStorage.setItem('refreshToken', data.refresh);
    return data;
}

async function logout() {
    const token = localStorage.getItem('accessToken');
    const response = await fetch('/api/auth/logout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error);
    }

    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    return await response.json();
}

async function changePassword(oldPassword, newPassword) {
    const token = localStorage.getItem('accessToken');
    const response = await fetch('/api/auth/password/change/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            old_password: oldPassword,
            new_password1: newPassword,
            new_password2: newPassword
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error);
    }

    return await response.json();
}

async function resetPassword(email) {
    const response = await fetch('/api/auth/password/reset/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error);
    }

    return await response.json();
}

async function confirmResetPassword(uid, token, newPassword) {
    const response = await fetch('/api/auth/password/reset/confirm/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            uid: uid,
            token: token,
            new_password1: newPassword,
            new_password2: newPassword
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error);
    }

    return await response.json();
}

async function verifyEmail(key) {
    const response = await fetch('/api/auth/registration/verify-email/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            key: key
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error);
    }

    return await response.json();
}

async function getUser() {
    const token = localStorage.getItem('accessToken');
    const response = await fetch('/api/auth/user/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error);
    }

    return await response.json();
}

async function refreshToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    const response = await fetch('/api/auth/token/refresh/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            refresh: refreshToken
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error);
    }

    const data = await response.json();
    localStorage.setItem('accessToken', data.access);
    return data.access;
}

async function fetchWithAuth(url, options = {}) {
    let token = localStorage.getItem('accessToken');
    const now = Math.floor(Date.now() / 1000);

    // چک کردن زمان انقضای توکن
    const tokenExp = JSON.parse(atob(token.split('.')[1])).exp;
    if (tokenExp < now) {
        token = await refreshToken();
    }

    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };

    return fetch(url, {
        ...options,
        headers
    });
}

// اضافه کردن لیسنر به فرم ثبت‌نام
// const registerForm = document.getElementById('register-form');
// registerForm.addEventListener('submit', async (e) => {
//     e.preventDefault();
//     const username = document.getElementById('id-username').value;
//     const password1 = document.getElementById('id-password1').value;
//     const password2 = document.getElementById('id-password2').value;
//     const email = document.getElementById('id-email').value;
//     if(password1 !== password2) {
//         console.error("Passwords do not match!")
//     }
//     try {
//         const data = await register(username, password1, email);
//         console.log('Registered:', data);
//     } catch (error) {
//         console.error('Error registering:', error);
//     }
// });

// اضافه کردن لیسنر به فرم ورود
const loginForm = document.getElementById('login-form');
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formdata = new FormData(loginForm);
    const username = formdata.get('login');
    const password = formdata.get('password');
    try {
        const data = await login(username, password);
        console.log('Logged in:', data);
        window.location.href ='index.html';
    } catch (error) {
        console.error('Error logging in:', error);
    }
});
