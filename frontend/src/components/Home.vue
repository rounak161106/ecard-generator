<template>
  <div class="landing">
    <div class="hero">
      <span class="badge">🚀 Fast & Official Digital E-Cards</span>
      <h1>E-Card Generator</h1>
      <p>Create, verify, and generate digital versions of your essential government and identity cards effortlessly.</p>
      <div v-if="token" class="hero-actions">
        <router-link to="/dashboard" class="btn-primary">Go to Dashboard →</router-link>
      </div>
      <div v-else class="hero-actions">
        <router-link to="/login" class="btn-primary">Get Started</router-link>
        <router-link to="/register" class="btn-secondary">Create Account</router-link>
      </div>
    </div>

    <div class="card-types">
      <div class="card">
        <div class="card-icon">🇮🇳</div>
        <h2>Aadhaar Card</h2>
        <p>12-digit unique identity proof for Indian residents with verification.</p>
        <button @click="goToCard('aadhar')">Request Aadhaar</button>
      </div>

      <div class="card">
        <div class="card-icon">💳</div>
        <h2>PAN Card</h2>
        <p>Permanent Account Number card issued by the Income Tax Department.</p>
        <button @click="goToCard('pan')">Request PAN</button>
      </div>

      <div class="card">
        <div class="card-icon">🗳️</div>
        <h2>Voter ID</h2>
        <p>Official Electoral Photo Identity Card (EPIC) with ward details.</p>
        <button @click="goToCard('voter')">Request Voter ID</button>
      </div>

      <div class="card">
        <div class="card-icon">🚗</div>
        <h2>Driving Licence</h2>
        <p>Official motor vehicle driving authorization with class and registration.</p>
        <button @click="goToCard('driving')">Request Licence</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    token() {
      return this.$store.state.token
    }
  },
  methods: {
    goToCard(cardname) {
      if (this.token) {
        this.$router.push(`/request/${cardname}`)
      } else {
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
.landing {
  text-align: center;
  padding: 50px 20px 80px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero {
  max-width: 680px;
  margin: 0 auto 50px;
}

.badge {
  display: inline-block;
  background: #ecfdf5;
  color: #059669;
  font-size: 13px;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 20px;
  margin-bottom: 16px;
  border: 1px solid #a7f3d0;
}

.landing h1 {
  font-size: 44px;
  font-weight: 800;
  color: #1f2937;
  margin-bottom: 14px;
  line-height: 1.2;
}

.landing p {
  color: #6b7280;
  font-size: 17px;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 25px;
}

.btn-primary {
  background: #42b883;
  color: white;
  padding: 11px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 15px;
  transition: 0.2s ease;
}

.btn-primary:hover {
  background: #369f6e;
}

.btn-secondary {
  background: white;
  color: #374151;
  padding: 11px 24px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  text-decoration: none;
  font-weight: 600;
  font-size: 15px;
  transition: 0.2s ease;
}

.btn-secondary:hover {
  background: #f9fafb;
}

.card-types {
  display: flex;
  justify-content: center;
  gap: 24px;
  flex-wrap: wrap;
}

.card {
  width: 250px;
  padding: 30px 22px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.card-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.card h2 {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 10px;
}

.card p {
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
  flex-grow: 1;
  margin-bottom: 20px;
}

.card button {
  width: 100%;
  padding: 11px 16px;
  border: none;
  border-radius: 6px;
  background: #42b883;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s ease;
}

.card button:hover {
  background: #369f6e;
}
</style>