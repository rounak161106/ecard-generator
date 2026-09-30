<template>
  <div class="request-container">
    <div class="card-form-wrapper">
      <div class="header-section">
        <router-link to="/dashboard" class="back-link">← Back to Dashboard</router-link>
        <div class="icon-wrap">{{ cardMeta.icon }}</div>
        <h2>{{ cardMeta.title }}</h2>
        <p>{{ cardMeta.description }}</p>
      </div>

      <div v-if="successMsg" class="alert alert-success">
        {{ successMsg }}
      </div>
      <div v-if="errorMsg" class="alert alert-error">
        {{ errorMsg }}
      </div>

      <form @submit.prevent="submitRequest" class="form-content">
        <!-- Common Full Name -->
        <div class="form-group">
          <label for="fullname">Full Name *</label>
          <input
            id="fullname"
            type="text"
            v-model="formData.fullname"
            placeholder="Enter full legal name"
            required
          />
        </div>

        <!-- Aadhaar Specific Fields -->
        <template v-if="cardname === 'aadhar'">
          <div class="form-row">
            <div class="form-group">
              <label for="dob">Date of Birth *</label>
              <input
                id="dob"
                type="date"
                v-model="formData.dob"
                required
              />
            </div>
            <div class="form-group">
              <label for="gender">Gender *</label>
              <select id="gender" v-model="formData.gender" required>
                <option value="" disabled>Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label for="address">Permanent Address *</label>
            <textarea
              id="address"
              v-model="formData.address"
              placeholder="House/Street, City, State, PIN"
              rows="3"
              required
            ></textarea>
          </div>

          <div class="form-group">
            <label for="ph">Mobile Number *</label>
            <input
              id="ph"
              type="tel"
              v-model="formData.ph"
              placeholder="10-digit mobile number"
              pattern="[0-9]{10}"
              required
            />
          </div>
        </template>

        <!-- PAN Specific Fields -->
        <template v-else-if="cardname === 'pan'">
          <div class="form-group">
            <label for="dob">Date of Birth *</label>
            <input
              id="dob"
              type="date"
              v-model="formData.dob"
              required
            />
          </div>

          <div class="form-group">
            <label for="ph">Mobile Number *</label>
            <input
              id="ph"
              type="tel"
              v-model="formData.ph"
              placeholder="10-digit mobile number"
              pattern="[0-9]{10}"
              required
            />
          </div>
        </template>

        <!-- Voter ID Specific Fields -->
        <template v-else-if="cardname === 'voter' || cardname === 'election'">
          <div class="form-row">
            <div class="form-group">
              <label for="dob">Date of Birth *</label>
              <input
                id="dob"
                type="date"
                v-model="formData.dob"
                required
              />
            </div>
            <div class="form-group">
              <label for="ward">Ward / Constituency *</label>
              <input
                id="ward"
                type="text"
                v-model="formData.ward"
                placeholder="e.g. Ward 12 / South East"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label for="address">Residential Address *</label>
            <textarea
              id="address"
              v-model="formData.address"
              placeholder="Enter full electoral residential address"
              rows="3"
              required
            ></textarea>
          </div>

          <div class="form-group">
            <label for="ph">Mobile Number *</label>
            <input
              id="ph"
              type="tel"
              v-model="formData.ph"
              placeholder="10-digit mobile number"
              pattern="[0-9]{10}"
              required
            />
          </div>
        </template>

        <!-- Driving Licence Specific Fields -->
        <template v-else>
          <div class="form-row">
            <div class="form-group">
              <label for="v_no">Vehicle Registration No. *</label>
              <input
                id="v_no"
                type="text"
                v-model="formData.v_no"
                placeholder="e.g. OD-09-AB-1234"
                required
              />
            </div>
            <div class="form-group">
              <label for="type">Vehicle Class / Type *</label>
              <select id="type" v-model="formData.type" required>
                <option value="" disabled>Select Vehicle Type</option>
                <option value="LMV - Light Motor Vehicle">LMV (Light Motor Vehicle - Car)</option>
                <option value="MCWG - Motorcycle with Gear">MCWG (Motorcycle with Gear)</option>
                <option value="HMV - Heavy Motor Vehicle">HMV (Heavy Motor Vehicle)</option>
              </select>
            </div>
          </div>
        </template>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Submitting Request...' : 'Submit Card Request' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      cardname: this.$route.params.cardname || 'aadhar',
      formData: {
        fullname: '',
        dob: '',
        address: '',
        gender: '',
        ph: '',
        ward: '',
        v_no: '',
        type: ''
      },
      loading: false,
      errorMsg: '',
      successMsg: ''
    }
  },
  computed: {
    token() {
      return this.$store.state.token || localStorage.getItem('token')
    },
    cardMeta() {
      const c = this.cardname.toLowerCase()
      if (c === 'aadhar') {
        return {
          title: 'Aadhaar Card Request',
          description: 'Official Unique Identification Authority of India (UIDAI) Card',
          icon: '🇮🇳'
        }
      } else if (c === 'pan') {
        return {
          title: 'PAN Card Request',
          description: 'Permanent Account Number - Income Tax Department of India',
          icon: '💳'
        }
      } else if (c === 'voter' || c === 'election') {
        return {
          title: 'Voter ID Request',
          description: 'Elector Photo Identity Card (EPIC) - Election Commission',
          icon: '🗳️'
        }
      } else {
        return {
          title: 'Driving Licence Request',
          description: 'Regional Transport Office (RTO) Motor Driving Authorization',
          icon: '🚗'
        }
      }
    }
  },
  watch: {
    '$route.params.cardname'(newVal) {
      if (newVal) {
        this.cardname = newVal
        this.errorMsg = ''
        this.successMsg = ''
      }
    }
  },
  methods: {
    async submitRequest() {
      this.loading = true
      this.errorMsg = ''
      this.successMsg = ''

      try {
        const resp = await axios.post(
          `http://127.0.0.1:5000/api/request/${this.cardname}`,
          this.formData,
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${this.token}`
            }
          }
        )

        if (resp.status === 201 || resp.status === 200) {
          this.successMsg = `Your ${this.cardMeta.title} has been submitted successfully! Redirecting to dashboard...`
          setTimeout(() => {
            this.$router.push('/dashboard')
          }, 1500)
        }
      } catch (err) {
        if (err.response && err.response.data && err.response.data.error) {
          this.errorMsg = err.response.data.error
        } else {
          this.errorMsg = 'Failed to submit card request. Please check details and try again.'
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.request-container {
  min-height: 85vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f7f9fb;
  padding: 40px 20px;
}

.card-form-wrapper {
  width: 100%;
  max-width: 520px;
  background: white;
  padding: 36px 32px;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #eef2f6;
}

.back-link {
  display: inline-block;
  font-size: 14px;
  color: #42b883;
  text-decoration: none;
  font-weight: 600;
  margin-bottom: 16px;
  transition: 0.2s ease;
}

.back-link:hover {
  text-decoration: underline;
}

.header-section {
  text-align: center;
  margin-bottom: 24px;
}

.icon-wrap {
  font-size: 42px;
  margin-bottom: 8px;
}

.header-section h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 6px;
}

.header-section p {
  font-size: 14px;
  color: #6b7280;
}

.alert {
  padding: 12px 16px;
  border-radius: 6px;
  font-size: 14px;
  margin-bottom: 20px;
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

.form-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-row .form-group {
  flex: 1;
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

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
  font-family: inherit;
  transition: 0.2s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #42b883;
  box-shadow: 0 0 0 3px rgba(66, 184, 131, 0.15);
}

.submit-btn {
  margin-top: 10px;
  padding: 12px;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s ease;
}

.submit-btn:hover:not(:disabled) {
  background: #369f6e;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
