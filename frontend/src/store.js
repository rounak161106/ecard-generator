import { createStore } from 'vuex'

const store = createStore({
	state: {
		token: localStorage.getItem('token') || '',
		role: localStorage.getItem('role') || '',
		username: localStorage.getItem('username') || '',
	},
	actions: {
		setAuth(context, payload) {
			const token = payload.token || ''
			const role = payload.role || ''
			const username = payload.username || ''
			localStorage.setItem('token', token)
			localStorage.setItem('role', role)
			localStorage.setItem('username', username)
			context.commit('setAuth', { token, role, username })
		},
		setToken(context, token) {
			localStorage.setItem('token', token)
			context.commit('setToken', token)
		},
		logout(context) {
			localStorage.removeItem('token')
			localStorage.removeItem('role')
			localStorage.removeItem('username')
			context.commit('clearAuth')
		},
	},
	mutations: {
		setAuth(state, payload) {
			state.token = payload.token
			state.role = payload.role
			state.username = payload.username
		},
		setToken(state, token) {
			state.token = token
		},
		clearAuth(state) {
			state.token = ''
			state.role = ''
			state.username = ''
		},
		clearToken(state) {
			state.token = ''
			state.role = ''
			state.username = ''
		},
	},
})

export default store

