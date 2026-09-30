<template>
  <nav class="navbar">
    <router-link to="/" class="logo-link">
      <div class="logo">
        <span class="logo-icon">🪪</span> E-Card Generator
      </div>
    </router-link>

    <div class="nav-links" v-if="!token">
      <router-link to="/">Home</router-link>
      <router-link to="/login">Login</router-link>
      <router-link to="/register" class="btn-register">Register</router-link>
    </div>
    <div class="nav-links" v-else>
      <router-link to="/dashboard">Dashboard</router-link>
      <router-link to="/profile" v-if="role !== 'admin'">Profile</router-link>
      <span class="user-badge" :class="{ 'admin-badge': role === 'admin' }">
        {{ role === 'admin' ? '🛡️ Admin' : '👤 ' + (username || 'User') }}
      </span>
      <button class="logout-btn" @click="logout">Logout</button>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  width: 100%;
  height: 65px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  box-sizing: border-box;
  background: white;
  border-bottom: 1px solid #e5e5e5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo-link {
  text-decoration: none;
}

.logo {
  font-size: 21px;
  font-weight: 700;
  color: #42b883;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 22px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav-links a {
  text-decoration: none;
  color: #555;
  font-size: 15px;
  font-weight: 500;
  transition: 0.2s ease;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #42b883;
}

.btn-register {
  padding: 7px 16px;
  background: #42b883;
  color: white !important;
  border-radius: 6px;
  transition: 0.2s ease;
}

.btn-register:hover {
  background: #369f6e;
}

.user-badge {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  padding: 5px 12px;
  border-radius: 20px;
}

.admin-badge {
  background: #fef3c7;
  border-color: #fde68a;
  color: #92400e;
}

.logout-btn {
  padding: 7px 16px;
  border: 1px solid #e5e5e5;
  background: #f9f9f9;
  color: #555;
  font-size: 14px;
  font-weight: 500;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.2s ease;
}

.logout-btn:hover {
  background: #fee2e2;
  color: #dc2626;
  border-color: #fca5a5;
}
</style>

<script>
export default {
  computed: {
    token() {
      return this.$store.state.token
    },
    role() {
      return this.$store.state.role || localStorage.getItem('role') || ''
    },
    username() {
      return this.$store.state.username || localStorage.getItem('username') || ''
    }
  },
  methods: {
    async logout() {
      await this.$store.dispatch('logout')
      this.$router.push('/login')
    }
  }
}
</script>