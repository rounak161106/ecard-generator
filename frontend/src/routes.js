import {createWebHistory, createRouter} from 'vue-router';
import Home from './components/Home.vue';
import LoginPage from './components/LoginPage.vue';
import RegisterPage from './components/RegisterPage.vue';
import Dashboard from './components/Dashboard.vue';
// import UserProfile from './components/UserProfile.vue';
// import RequestCard from './components/RequestCard.vue';
// import ViewCard from './components/ViewCard.vue';


const routes = [
    { path: '/', component: Home },
    { path: '/login', component: LoginPage },
    { path: '/register', component: RegisterPage },
    { path: '/dashboard', component: Dashboard },
    // { path: '/user', components: [
    //     { path: "", component: UserProfile },
    //     { path: "request/:cardname", component: RequestCard },
    //     { path: "view/:cardname", component: ViewCard },
    // ] },
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})