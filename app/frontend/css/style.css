// MAIN — навигация и инициализация

function showPage(name) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'))
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'))
    document.getElementById('page-' + name).classList.add('active')

    const tabs = { popular: 0, search: 1, watchlist: 2 }
    if (tabs[name] !== undefined) {
        document.querySelectorAll('.nav-tab')[tabs[name]].classList.add('active')
    }

    if (name === 'popular') loadPopular()
    if (name === 'watchlist') loadWatchlist()
}

function toast(msg, type = '') {
    const el = document.getElementById('toast')
    el.textContent = msg
    el.className = `toast ${type} show`
    setTimeout(() => el.classList.remove('show'), 3000)
}

// ИНИЦИАЛИЗАЦИЯ при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token')
    const username = localStorage.getItem('username')

    if (token) {
        showLoggedIn(username)
        showPage('popular')
    } else {
        showPage('auth')
    }
})