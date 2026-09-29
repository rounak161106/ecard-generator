import { createStore } from 'vuex'

const store = createStore({
	state: {
		token: localStorage.getItem('token') || '',
	},
	actions: {
		setToken(context, token) {
			localStorage.setItem('token', token)
			context.commit('setToken', token)
		},
		logout(context) {
			localStorage.removeItem('token')
			context.commit('clearToken')
		},
	},
	mutations: {
		setToken(state, token) {
			state.token = token
		},
		clearToken(state) {
			state.token = ''
		},
	},
})

export default store
