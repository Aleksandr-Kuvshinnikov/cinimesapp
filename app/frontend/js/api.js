


const API = 'http://localhost:8000'

async function request(url, options = {}){

    const token= localStorage.getItem('token')
    const headers = {'Content-Type' : 'application/json', ...options.headers}

    if (token){
        headers['Authorization'] = `Bearer ${token}`
    }

    const res= await fetch(API + url, {...options, headers })
    return res
}



async function apiLogin(email, password){
    const form = new FormData()
    form.append('username', email)
    form.append('password', password)
    return await fetch(API + '/auth/login', {method : 'POST', body : form})
}

async function apiRegister(username, email, password){
    return await request('/auth/register', {method: 'POST', body: JSON.stringify({username, email, password})})
}



// MOVIES
async function apiGetPopular() {
    return await request('/movies/popular')
}

async function apiSearch(query) {
    return await request(`/search/?query=${encodeURIComponent(query)}`)
}

async function apiGetMovie(id) {
    return await request(`/movies/${id}`)
}

// WATCHLIST
async function apiGetWatchlist() {
    return await request('/watchlist/')
}

async function apiAddToWatchlist(movieId, status) {
    return await request('/watchlist/', {
        method: 'POST',
        body: JSON.stringify({ movie_id: movieId, status })
    })
}

async function apiUpdateWatchlist(id, movieId, status) {
    return await request(`/watchlist/${id}`, {
        method: 'PUT',
        body: JSON.stringify({ movie_id: movieId, status })
    })
}

async function apiDeleteWatchlist(id) {
    return await request(`/watchlist/${id}`, { method: 'DELETE' })
}

// REVIEWS
async function apiGetReviews(movieId) {
    return await request(`/movies/${movieId}/reviews`)
}

async function apiAddReview(movieId, text, rating) {
    return await request(`/movies/${movieId}/reviews`, {
        method: 'POST',
        body: JSON.stringify({ text, rating })
    })
}

// LIKES
async function apiGetLikes(movieId) {
    return await request(`/movies/${movieId}/likes`)
}

async function apiToggleLike(movieId) {
    return await request(`/movies/${movieId}/like`, { method: 'POST' })
}

async function apiDeleteLike(movieId) {
    return await request(`/movies/${movieId}/like`, { method: 'DELETE' })
}
