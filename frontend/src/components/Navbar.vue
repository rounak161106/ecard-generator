<template>
  <nav class="navbar">
    <div class="logo">
      E-Card Generator
    </div>

    <div class="nav-links" v-if="!token">
      <router-link to="/login">Login</router-link>
      <router-link to="/register">Register</router-link>
    </div>
    <div v-else>
      <button @click="logout">Logout</button>
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
}

.logo {
  font-size: 21px;
  font-weight: 600;
  color: #42b883;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 30px;
}

.nav-links a {
  text-decoration: none;
  color: #555;
  font-size: 15px;
  transition: 0.2s ease;
}

.nav-links a:hover {
  color: #42b883;
}
</style>

<script>
    export default {
        computed: {
          token() {
            return this.$store.state.token
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