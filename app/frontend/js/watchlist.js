// WATCHLIST

async function loadWatchlist() {
    const container = document.getElementById('watchlist-list')
    container.innerHTML = '<div class="loader"><div class="spinner"></div>Загрузка...</div>'

    const token = localStorage.getItem('token')
    if (!token) {
        showPage('auth')
        return
    }

    try {
        const res = await apiGetWatchlist()
        const items = await res.json()

        if (!items.length) {
            container.innerHTML = `
                <div class="empty">
                    <div class="empty-icon">🎬</div>
                    <div class="empty-title">Вотчлист пуст</div>
                    <div class="empty-text">Добавьте фильмы из поиска или популярных</div>
                </div>`
            return
        }

        container.innerHTML = items.map(item => `
            <div class="watchlist-item" id="witem-${item.id}">
                <div class="watchlist-thumb" style="background:var(--surface2);display:flex;align-items:center;justify-content:center;font-size:20px;border-radius:6px;width:50px;height:75px;flex-shrink:0">🎬</div>
                <div class="watchlist-info">
                    <div class="watchlist-title">Фильм #${item.movie_id}</div>
                    <span class="status-badge status-${item.status}">${statusLabel(item.status)}</span>
                </div>
                <div class="watchlist-actions">
                    <select class="status-select" onchange="updateWatchlist(${item.id}, ${item.movie_id}, this.value)">
                        <option value="want" ${item.status === 'want' ? 'selected' : ''}>Хочу</option>
                        <option value="watching" ${item.status === 'watching' ? 'selected' : ''}>Смотрю</option>
                        <option value="watched" ${item.status === 'watched' ? 'selected' : ''}>Посмотрел</option>
                    </select>
                    <button class="btn btn-danger" onclick="removeWatchlist(${item.id})" style="font-size:12px;padding:6px 12px">Удалить</button>
                </div>
            </div>
        `).join('')

    } catch {
        container.innerHTML = '<div class="empty"><div class="empty-icon">⚠️</div><div class="empty-title">Ошибка загрузки</div></div>'
    }
}

function statusLabel(s) {
    return { want: 'Хочу посмотреть', watching: 'Смотрю', watched: 'Посмотрел' }[s] || s
}

async function updateWatchlist(id, movieId, status) {
    try {
        await apiUpdateWatchlist(id, movieId, status)
        toast('Статус обновлён', 'success')
        loadWatchlist()
    } catch {
        toast('Ошибка', 'error')
    }
}

async function removeWatchlist(id) {
    try {
        await apiDeleteWatchlist(id)
        toast('Удалено из вотчлиста')
        loadWatchlist()
    } catch {
        toast('Ошибка', 'error')
    }
}