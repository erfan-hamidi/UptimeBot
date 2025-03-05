// frontend/static/js/main.js
// document.addEventListener('DOMContentLoaded', function () {
//     fetch('/api/yourmodel/')
//         .then(response => response.json())
//         .then(data => {
//             const container = document.getElementById('data-container');
//             data.forEach(item => {
//                 const p = document.createElement('p');
//                 p.textContent = item.name; 
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

function updateHeader() {
    const username = localStorage.getItem('username') || sessionStorage.getItem('username');
    
    if (username) {
        // Hide login and signup links
        document.getElementById('login-link').style.display = 'none';
        document.getElementById('signup-link').style.display = 'none';
        
        // Show the username
        const usernameElement = document.getElementById('username');
        usernameElement.textContent = `${username}`;
        usernameElement.style.display = 'inline'; // Make sure the username is visible
        
        // Optionally, show the logout button
        document.getElementById('logout-button').style.display = 'inline';
    } else {
        // Ensure login/signup links are visible if no username
        document.getElementById('login-link').style.display = 'inline';
        document.getElementById('signup-link').style.display = 'inline';
        document.getElementById('username').style.display = 'none';
        document.getElementById('logout-button').style.display = 'none';
    }
}

function loadHeader() {
    fetch('static/html/header.htm')
        .then(response => response.text())
        .then(data => {
            document.getElementById('header-container').innerHTML = data;
            updateHeader();  // Update the header after loading it
        });
}

async function logout() {
    // Clear the stored username and tokens
    localStorage.removeItem('username');
    sessionStorage.removeItem('username');
    localStorage.removeItem('accessToken');
    sessionStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    sessionStorage.removeItem('refreshToken');

    // Update the header to show login/signup links again
    updateHeader();
}


document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const rememberMe = document.getElementById('rememberMe').checked;

    try {
        const data = await login(email, password, rememberMe);
        console.log("Login successful:", data);

        // Redirect to dashboard or another page
        window.location.href = "login.htm";
    } catch (error) {
        console.error("Login failed:", error.message);

        // Display an error message to the user
        alert("Login failed: " + error.message);
    }
});

async function login(username, password, rememberMe) {
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
    console.log(data.access)
     // Check if "Remember Me" is checked
     if (rememberMe) {
        localStorage.setItem('accessToken', data.access);
        localStorage.setItem('refreshToken', data.refresh);
        localStorage.setItem('username', username); 
    } else {
        sessionStorage.setItem('accessToken', data.access);
        sessionStorage.setItem('refreshToken', data.refresh);
        localStorage.setItem('username', username); 
    }

    return data;
}

// async function logout() {
//     const token = localStorage.getItem('accessToken');
//     const response = await fetch('/api/auth/logout/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'Authorization': `Bearer ${token}`
//         }
//     });

//     if (!response.ok) {
//         const error = await response.json();
//         throw new Error(error);
//     }

//     localStorage.removeItem('accessToken');
//     localStorage.removeItem('refreshToken');
//     return await response.json();
// }

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

async function fetchWithAuth(url, options = {}) {
    let token = localStorage.getItem('accessToken');
    const now = Math.floor(Date.now() / 1000);

    // Check token expiration time
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

// Add the list to the registration form
const registerForm = document.getElementById('register-form');
registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formdata = new FormData(registerForm);
    const username = formdata.get('username');
    const password1 = formdata.get('password1');
    const password2 = formdata.get('password2');
    const email = formdata.get('email');
    const passwordStrengthMessages = document.getElementById('password-strength-messages');
    passwordStrengthMessages.style.display = 'none';
    if(password1 !== password2) {
        passwordStrengthMessages.innerHTML = '<li style="color:red;">Passwords do not match!</li>';
        passwordStrengthMessages.style.display = 'block';
        return
    }

    const passwordStrength = getPasswordStrength(password1);
    if (!passwordStrength.strength) {
        passwordStrengthMessages.innerHTML = passwordStrength.message; // Update messages
        passwordStrengthMessages.style.display = 'block';
        return; // Prevent form submission if password is weak
    }

    try {
        const data = await register(username, password1, email);
        console.log('Registered:', data);
    } catch (error) {
        console.error('Error registering:', error);
    }
});


const loginForm = document.getElementById('login-form');
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formdata = new FormData(loginForm);
    const username = formdata.get('login');
    const password = formdata.get('password');
    const rememberMe = formdata.get('remember') === 'on';
    console.log('sas',rememberMe)
    try {
        const data = await login(username, password, rememberMe);
        console.log('Logged in:', data);
       // window.location.href ='login.htm';
    } catch (error) {
        console.error('Error logging in:', error);
    }
});

async function refreshToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        // Handle case where refresh token is not available
        return null;
    }

    const response = await fetch('http://127.0.0.1:8000/account/token/refresh/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            refresh: refreshToken
        })
    });

    if (!response.ok) {
        // Handle refresh token failure (e.g., logout user, redirect to login page)
        return null;
    }

    const data = await response.json();
    localStorage.setItem('accessToken', data.access);
    return data.access; // Return the new access token
}

async function handleApiRequest() {
    let accessToken = localStorage.getItem('accessToken');

    // Check if access token is expired or not present
    const tokenExpired = accessToken ? isTokenExpired(accessToken) : true;

    if (tokenExpired) {
        // Attempt to refresh the token
        accessToken = await refreshToken();
        if (!accessToken) {
            // Handle refresh token failure (e.g., logout user, redirect to login page)
            return;
        }
    }

    // Make your API request using the access token
    try {
        const response = await fetch('http://127.0.0.1:8000/api/endpoint/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        const responseData = await response.json();
        console.log('API Response:', responseData);
    } catch (error) {
        console.error('Error making API request:', error);
    }
}

function isTokenExpired(token) {
    // Implement your logic to check if the token is expired
    // For JWT tokens, you can decode the token and check the expiration claim (exp)
    // Return true if the token is expired, false otherwise
    const decodedToken = decodeJwt(token);
    if (!decodedToken || !decodedToken.exp) {
        return true; // Token is invalid or doesn't have an expiration claim
    }
    const expirationTimestamp = decodedToken.exp * 1000; // Convert expiration time to milliseconds
    return Date.now() >= expirationTimestamp;
}

function decodeJwt(token) {
    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch (error) {
        console.error('Error decoding JWT:', error);
        return null;
    }
}


function getPasswordStrength(password) {
    // Check if the password contains at least 8 characters
    const hasMinLength = password.length >= 8;

    // Check if the password is entirely numeric
    const isNumericOnly = /^\d+$/.test(password);

    // Define common passwords (you can extend this list as needed)
    const commonPasswords = ['password', '123456', 'qwerty', 'abc123', 'letmein', 'admin', 'welcome'];

    // Check if the password is too similar to personal information or a commonly used password
    const isSimilarToPersonalInfo = false; // Implement this check based on your requirements
    const isCommonPassword = commonPasswords.includes(password.toLowerCase());

    // Build the password strength message based on the checks
    let strength = true
    let strengthMessage = '';
    if (!hasMinLength) {
        strengthMessage += '<li style="color:red;">Your password must contain at least 8 characters.</li>';
        strength = false
    }
    if (isNumericOnly) {
        strengthMessage += '<li style="color:red;">Your password can’t be entirely numeric.</li>';
        strength = false
    }
    if (isSimilarToPersonalInfo) {
        strengthMessage += '<li style="color:red;">Your password can’t be too similar to your other personal information.</li>';
        strength = false
    }
    if (isCommonPassword) {
        strengthMessage += '<li style="color:red;">Your password can’t be a commonly used password.</li>';
        strength = false
    }
    console.log(strength,'\n' , strengthMessage)
    return {
        strength: strength, // Determine password strength based on messages
        message: strengthMessage // Return the generated strength message
    };
}

document.getElementById('monitor-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Retrieve the JWT token from sessionStorage or localStorage
    const accessToken = sessionStorage.getItem('accessToken') || localStorage.getItem('accessToken');

    if (!accessToken) {
        alert('Access token not found. Please log in.');
        return;
    }

    // Collect form data
    const formData = {
        name: document.getElementById('monitor-name').value,
        type: document.getElementById('monitor-type').value,
        url: document.getElementById('monitor-url').value,
        interval: document.getElementById('check-interval').value,
        alert_types: getSelectedAlertTypes(),
    };

    // Send the data via fetch API
    fetch('http://127.0.0.1:8000/monitors/', { // Use the specified endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`, // Use the retrieved token
        },
        body: JSON.stringify(formData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Monitor created successfully:', data);
        alert('Monitor created successfully!');
    })
    .catch(error => {
        console.error('There was a problem creating the monitor:', error);
        alert('Failed to create monitor. Please check the console for details.');
    });
});

// Helper function to get selected alert types
function getSelectedAlertTypes() {
    const alertTypes = [];
    if (document.getElementById('alert-email').checked) {
        alertTypes.push(1); // Replace 1 with the ID of the "email" AlertType
    }
    if (document.getElementById('alert-phone').checked) {
        alertTypes.push(2); // Replace 2 with the ID of the "phone" AlertType
    }
    if (document.getElementById('alert-sms').checked) {
        alertTypes.push(3); // Replace 3 with the ID of the "sms" AlertType
    }
    return alertTypes;
}