import { createWebHistory, createRouter } from 'vue-router'
import Home from './components/Home.vue'
import LoginPage from './components/LoginPage.vue'
import RegisterPage from './components/RegisterPage.vue'
import Dashboard from './components/Dashboard.vue'
import UserProfile from './components/UserProfile.vue'
import RequestCard from './components/RequestCard.vue'
import ViewCard from './components/ViewCard.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: LoginPage, meta: { guestOnly: true } },
  { path: '/register', component: RegisterPage, meta: { guestOnly: true } },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/profile', component: UserProfile, meta: { requiresAuth: true } },
  { path: '/request/:cardname', component: RequestCard, meta: { requiresAuth: true } },
  { path: '/view/:cardname', component: ViewCard, meta: { requiresAuth: true } },
  // Fallback to home
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.guestOnly && token) {
    next('/dashboard')
  } else {
    next()
  }
})