document.getElementById('login-btn').addEventListener('click', async function () {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const data = {
        username: username,
        password: password
    };

    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            localStorage.setItem('token', result.access_token); // Guardar el token
            showShortener(); // Mostrar el formulario de URL shortener
        } else {
            document.getElementById('login-error').innerText = result.error;
        }
    } catch (error) {
        document.getElementById('login-error').innerText = 'Error logging in';
    }
});

document.getElementById('register-btn').addEventListener('click', async function () {
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;

    const data = {
        username: username,
        password: password
    };

    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById('register-error').innerText = 'User registered successfully';
        } else {
            document.getElementById('register-error').innerText = result.error;
        }
    } catch (error) {
        document.getElementById('register-error').innerText = 'Error registering user';
    }
});

document.getElementById('shorten-btn').addEventListener('click', async function () {
    const original_url = document.getElementById('original_url').value;
    const custom_slug = document.getElementById('custom_slug').value;
    const token = localStorage.getItem('token'); // Obtener el token del localStorage

    const data = {
        url: original_url,
        slug: custom_slug
    };

    try {
        const response = await fetch('/api/urls/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` // Agregar el token JWT
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById('result').innerHTML = `<p>Shortened URL: <a href="${result.short_url}" target="_blank">${result.short_url}</a></p>`;
        } else {
            document.getElementById('result').innerText = `Error: ${result.error}`;
        }
    } catch (error) {
        document.getElementById('result').innerText = 'Error shortening the URL';
    }
});

document.getElementById('logout-btn').addEventListener('click', function () {
    localStorage.removeItem('token'); // Eliminar el token
    hideShortener();
});

function showShortener() {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('shorten-form').style.display = 'block';
    document.getElementById('logout-btn').style.display = 'block';
}

function hideShortener() {
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('register-form').style.display = 'block';
    document.getElementById('shorten-form').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'none';
}

// Verificar si ya hay un token al cargar la página
if (localStorage.getItem('token')) {
    showShortener();
}
