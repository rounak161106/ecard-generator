<template>
  <div class="profile-container">
    <div class="profile-card">
      <div class="profile-header">
        <div class="avatar-circle">
          <span>{{ (profile.username || 'U')[0].toUpperCase() }}</span>
        </div>
        <h2>User Profile</h2>
        <span class="role-badge" :class="{ 'admin-badge': profile.role === 'admin' }">
          {{ profile.role === 'admin' ? '🛡️ Administrator' : '👤 Citizen User' }}
        </span>
      </div>

      <!-- Quick Stats -->
      <div class="stats-row">
        <div class="stat-box">
          <span class="stat-number">{{ profile.total_cards || 0 }}</span>
          <span class="stat-label">Total Cards</span>
        </div>
        <div class="stat-box">
          <span class="stat-number color-green">{{ profile.generated_cards || 0 }}</span>
          <span class="stat-label">Active / Generated</span>
        </div>
        <div class="stat-box">
          <span class="stat-number color-yellow">{{ profile.pending_cards || 0 }}</span>
          <span class="stat-label">Pending Verification</span>
        </div>
      </div>

      <div v-if="successMsg" class="alert alert-success">{{ successMsg }}</div>
      <div v-if="errorMsg" class="alert alert-error">{{ errorMsg }}</div>

      <!-- Profile Update Form -->
      <form @submit.prevent="updateProfile" class="profile-form">
        <div class="form-group">
          <label>Username</label>
          <input type="text" :value="profile.username" disabled class="input-disabled" />
          <small class="help-text">Username cannot be changed.</small>
        </div>

        <div class="form-group">
          <label for="email">Email Address</label>
          <input
            id="email"
            type="email"
            v-model="formData.email"
            placeholder="Enter your email"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Change Password</label>
          <input
            id="password"
            type="password"
            v-model="formData.password"
            placeholder="Leave blank to keep current password"
          />
          <small class="help-text">Minimum 4 characters if changing.</small>
        </div>

        <button type="submit" class="btn-save" :disabled="loading">
          {{ loading ? 'Saving Changes...' : 'Update Profile' }}
        </button>
      </form>

      <div class="profile-footer">
        <router-link to="/dashboard" class="btn-secondary-link">← Go to Dashboard</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      profile: {
        username: '',
        email: '',
        role: '',
        total_cards: 0,
        generated_cards: 0,
        pending_cards: 0
      },
      formData: {
        email: '',
        password: ''
      },
      loading: false,
      successMsg: '',
      errorMsg: ''
    }
  },
  computed: {
    token() {
      return this.$store.state.token || localStorage.getItem('token')
    }
  },
  mounted() {
    this.fetchProfile()
  },
  methods: {
    async fetchProfile() {
      try {
        const resp = await axios.get('http://127.0.0.1:5000/api/user/profile', {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })
        if (resp.status === 200) {
          this.profile = resp.data
          this.formData.email = resp.data.email
        }
      } catch (err) {
        this.errorMsg = 'Could not load profile details.'
      }
    },
    async updateProfile() {
      this.loading = true
      this.errorMsg = ''
      this.successMsg = ''

      try {
        const payload = {
          email: this.formData.email
        }
        if (this.formData.password) {
          payload.password = this.formData.password
        }

        const resp = await axios.post('http://127.0.0.1:5000/api/user/update', payload, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${this.token}`
          }
        })

        if (resp.status === 200) {
          this.successMsg = 'Profile updated successfully!'
          this.formData.password = ''
          this.fetchProfile()
        }
      } catch (err) {
        if (err.response && err.response.data && err.response.data.error) {
          this.errorMsg = err.response.data.error
        } else {
          this.errorMsg = 'Failed to update profile.'
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.profile-container {
  min-height: 85vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f7f9fb;
  padding: 40px 20px;
}

.profile-card {
  width: 100%;
  max-width: 480px;
  background: white;
  padding: 36px 32px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #eef2f6;
}

.profile-header {
  text-align: center;
  margin-bottom: 24px;
}

.avatar-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #42b883;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  margin: 0 auto 12px;
}

.profile-header h2 {
  font-size: 22px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 6px;
}

.role-badge {
  display: inline-block;
  font-size: 13px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
  background: #f0fdf4;
  color: #15803d;
  border: 1px solid #bbf7d0;
}

.admin-badge {
  background: #fef3c7;
  color: #92400e;
  border-color: #fde68a;
}

.stats-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 24px;
  padding: 16px 12px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.stat-box {
  flex: 1;
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 20px;
  font-weight: 800;
  color: #1f2937;
}

.color-green {
  color: #15803d;
}

.color-yellow {
  color: #b45309;
}

.stat-label {
  font-size: 11px;
  color: #64748b;
  text-transform: uppercase;
  font-weight: 600;
}

.alert {
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 13px;
  margin-bottom: 16px;
  text-align: center;
}

.alert-success {
  background: #ecfdf5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.alert-error {
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
}

.form-group input {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
  transition: 0.2s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #42b883;
}

.input-disabled {
  background: #f3f4f6;
  color: #6b7280;
  cursor: not-allowed;
}

.help-text {
  font-size: 11px;
  color: #6b7280;
  margin-top: 4px;
}

.btn-save {
  padding: 11px;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s ease;
  margin-top: 6px;
}

.btn-save:hover:not(:disabled) {
  background: #369f6e;
}

.btn-save:disabled {
  opacity: 0.6;
}

.profile-footer {
  text-align: center;
  margin-top: 24px;
}

.btn-secondary-link {
  font-size: 14px;
  color: #4b5563;
  text-decoration: none;
  font-weight: 600;
}

.btn-secondary-link:hover {
  color: #42b883;
}
</style>
