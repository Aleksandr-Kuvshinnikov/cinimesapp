// AUTH

function switchAuth(mode) {
    document.getElementById('login-form').style.display = mode === 'login' ? 'block' : 'none'
    document.getElementById('register-form').style.display = mode === 'register' ? 'block' : 'none'
    document.getElementById('toggle-login').classList.toggle('active', mode === 'login')
    document.getElementById('toggle-register').classList.toggle('active', mode === 'register')
    hideAuthError()
}

function showAuthError(msg) {
    const el = document.getElementById('auth-error')
    el.textContent = msg
    el.classList.add('show')
}

function hideAuthError() {
    document.getElementById('auth-error').classList.remove('show')
}

async function login() {
    const email = document.getElementById('login-email').value.trim()
    const password = document.getElementById('login-password').value

    if (!email || !password) {
        showAuthError('Заполните все поля')
        return
    }

    try {
        const res = await apiLogin(email, password)
        const data = await res.json()

        if (!res.ok) {
            showAuthError(data.detail || 'Ошибка входа')
            return
        }

        localStorage.setItem('token', data.access_token)
        localStorage.setItem('username', email.split('@')[0])

        showLoggedIn(email.split('@')[0])
        showPage('popular')
        loadPopular()
        toast('Добро пожаловать!', 'success')

    } catch {
        showAuthError('Ошибка подключения к серверу')
    }
}

async function register() {
    const username = document.getElementById('reg-username').value.trim()
    const email = document.getElementById('reg-email').value.trim()
    const password = document.getElementById('reg-password').value

    if (!username || !email || !password) {
        showAuthError('Заполните все поля')
        return
    }

    try {
        const res = await apiRegister(username, email, password)
        const data = await res.json()

        if (!res.ok) {
            showAuthError(data.detail || 'Ошибка регистрации')
            return
        }

        toast('Аккаунт создан! Войдите.', 'success')
        switchAuth('login')

    } catch {
        showAuthError('Ошибка подключения к серверу')
    }
}

function logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('username')

    document.getElementById('nav-auth').style.display = 'flex'
    document.getElementById('nav-user').style.display = 'none'

    showPage('auth')
    toast('Вы вышли из аккаунта')
}

function showLoggedIn(username) {
    document.getElementById('nav-auth').style.display = 'none'
    document.getElementById('nav-user').style.display = 'flex'
    document.getElementById('nav-username').textContent = username || 'Пользователь'
}