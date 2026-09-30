<template>
  <div class="view-container">
    <div class="top-nav-bar no-print">
      <router-link to="/dashboard" class="btn-back">← Back to Dashboard</router-link>
      <button class="btn-print" @click="printCard">🖨️ Print / Download Card</button>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading card details...</p>
    </div>

    <div v-else-if="errorMsg" class="error-state">
      <p class="err-text">{{ errorMsg }}</p>
      <router-link to="/dashboard" class="btn-back">Return to Dashboard</router-link>
    </div>

    <div v-else class="card-display-area">
      <!-- 1. AADHAAR CARD DESIGN -->
      <div v-if="cardname === 'aadhar'" class="id-card aadhar-card" id="printable-card">
        <div class="aadhar-top-header">
          <div class="emblem-box">🏛️</div>
          <div class="header-titles">
            <h3>भारत सरकार</h3>
            <h4>GOVERNMENT OF INDIA</h4>
          </div>
          <div class="aadhaar-logo">
            <span class="logo-sun">☀️</span>
            <span class="logo-text">आधार</span>
          </div>
        </div>
        <div class="tricolor-stripe">
          <div class="stripe-saffron"></div>
          <div class="stripe-white"></div>
          <div class="stripe-green"></div>
        </div>

        <div class="aadhar-body">
          <div class="aadhar-photo-col">
            <div class="photo-frame">
              <span class="avatar-icon">👤</span>
            </div>
            <div class="qr-mockup">
              <div class="qr-pattern"></div>
              <span>QR Code</span>
            </div>
          </div>

          <div class="aadhar-info-col">
            <div class="info-row">
              <span class="label">Name / नाम:</span>
              <span class="value strong">{{ cardData.data.fullname || username }}</span>
            </div>
            <div class="info-row" v-if="cardData.data.dob">
              <span class="label">DOB / जन्म तिथि:</span>
              <span class="value">{{ cardData.data.dob }}</span>
            </div>
            <div class="info-row" v-if="cardData.data.gender">
              <span class="label">Gender / लिंग:</span>
              <span class="value">{{ cardData.data.gender }}</span>
            </div>
            <div class="info-row" v-if="cardData.data.ph">
              <span class="label">Mobile / मोबाइल:</span>
              <span class="value">{{ cardData.data.ph }}</span>
            </div>
            <div class="info-row" v-if="cardData.data.address">
              <span class="label">Address / पता:</span>
              <span class="value small-text">{{ cardData.data.address }}</span>
            </div>
          </div>
        </div>

        <div class="aadhar-footer">
          <div class="aadhar-number">
            {{ formatAadhaar(cardData.key || 'XXXX XXXX XXXX') }}
          </div>
          <div class="aadhar-motto">
            मेरा आधार, मेरी पहचान
          </div>
        </div>
      </div>

      <!-- 2. PAN CARD DESIGN -->
      <div v-else-if="cardname === 'pan'" class="id-card pan-card" id="printable-card">
        <div class="pan-header">
          <div class="pan-title-left">
            <h3>आयकर विभाग</h3>
            <h4>INCOME TAX DEPARTMENT</h4>
          </div>
          <div class="emblem-wrap">🏛️</div>
          <div class="pan-title-right">
            <h3>भारत सरकार</h3>
            <h4>GOVT. OF INDIA</h4>
          </div>
        </div>

        <div class="pan-body">
          <div class="pan-left">
            <div class="pan-chip">
              <div class="chip-line"></div>
              <div class="chip-line"></div>
            </div>
            <div class="pan-photo">
              <span class="avatar-icon">👤</span>
            </div>
          </div>

          <div class="pan-details">
            <div class="pan-field">
              <span class="p-label">Permanent Account Number Card / स्थायी लेखा संख्या</span>
              <div class="pan-number-box">
                {{ cardData.key || 'ABCDE1234F' }}
              </div>
            </div>

            <div class="pan-field">
              <span class="p-label">Name / नाम</span>
              <span class="p-val strong">{{ cardData.data.fullname || username }}</span>
            </div>

            <div class="pan-field" v-if="cardData.data.dob">
              <span class="p-label">Date of Birth / जन्म की तारीख</span>
              <span class="p-val">{{ cardData.data.dob }}</span>
            </div>

            <div class="pan-field" v-if="cardData.data.ph">
              <span class="p-label">Contact / सम्पर्क</span>
              <span class="p-val">{{ cardData.data.ph }}</span>
            </div>
          </div>

          <div class="pan-right">
            <div class="qr-mockup mini-qr">
              <div class="qr-pattern"></div>
            </div>
            <div class="signature-box">
              <span class="sign-font">{{ cardData.data.fullname || username }}</span>
              <small>Authorized Signature</small>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. VOTER ID DESIGN -->
      <div v-else-if="cardname === 'voter' || cardname === 'election'" class="id-card voter-card" id="printable-card">
        <div class="voter-header">
          <div class="voter-emblem">🏛️</div>
          <div class="voter-header-text">
            <h3>भारत निर्वाचन आयोग</h3>
            <h4>ELECTION COMMISSION OF INDIA</h4>
            <p>ELECTOR PHOTO IDENTITY CARD</p>
          </div>
        </div>

        <div class="voter-body">
          <div class="voter-photo-side">
            <div class="photo-frame">
              <span class="avatar-icon">👤</span>
            </div>
            <div class="voter-epic-code">
              {{ cardData.key || 'ABC1234567' }}
            </div>
          </div>

          <div class="voter-info-side">
            <div class="v-row">
              <span class="v-label">Elector's Name:</span>
              <span class="v-val strong">{{ cardData.data.fullname || username }}</span>
            </div>
            <div class="v-row" v-if="cardData.data.dob">
              <span class="v-label">Date of Birth:</span>
              <span class="v-val">{{ cardData.data.dob }}</span>
            </div>
            <div class="v-row" v-if="cardData.data.ward">
              <span class="v-label">Ward / Constituency:</span>
              <span class="v-val">{{ cardData.data.ward }}</span>
            </div>
            <div class="v-row" v-if="cardData.data.address">
              <span class="v-label">Residential Address:</span>
              <span class="v-val small-text">{{ cardData.data.address }}</span>
            </div>
          </div>
        </div>

        <div class="voter-footer">
          <span>Official Digital Identity Document</span>
          <span class="verified-tag">✓ Verified Voter</span>
        </div>
      </div>

      <!-- 4. DRIVING LICENCE DESIGN -->
      <div v-else class="id-card dl-card" id="printable-card">
        <div class="dl-header">
          <div class="dl-flag">🇮🇳</div>
          <div class="dl-titles">
            <h3>UNION OF INDIA - DRIVING LICENCE</h3>
            <p>Regional Transport Authority - Form 7</p>
          </div>
          <div class="dl-badge">RTO</div>
        </div>

        <div class="dl-body">
          <div class="dl-photo-box">
            <div class="photo-frame">
              <span class="avatar-icon">👤</span>
            </div>
            <div class="chip-mini"></div>
          </div>

          <div class="dl-info-box">
            <div class="dl-licence-num">
              <span class="d-label">DL No.:</span>
              <span class="d-num">{{ cardData.key || 'AB-12-2025-1234567' }}</span>
            </div>

            <div class="dl-grid">
              <div class="d-field">
                <span class="d-label">Holder's Name:</span>
                <span class="d-val strong">{{ cardData.data.fullname || username }}</span>
              </div>
              <div class="d-field" v-if="cardData.data.v_no">
                <span class="d-label">Vehicle Registration:</span>
                <span class="d-val">{{ cardData.data.v_no }}</span>
              </div>
              <div class="d-field" v-if="cardData.data.type">
                <span class="d-label">Authorized Vehicle Class:</span>
                <span class="d-val highlight-val">{{ cardData.data.type }}</span>
              </div>
              <div class="d-field">
                <span class="d-label">Validity:</span>
                <span class="d-val">Valid Throughout India (Non-Transport)</span>
              </div>
            </div>
          </div>
        </div>

        <div class="dl-footer">
          <span>Digital Driving Authorization</span>
          <span>Security Chip Embedded</span>
        </div>
      </div>

      <div class="card-status-banner no-print">
        <span class="status-pill status-generated">Status: {{ cardData.status }}</span>
        <span class="status-tip">This digital e-card is signed and valid for online verification.</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      cardname: this.$route.params.cardname || 'aadhar',
      loading: true,
      errorMsg: '',
      cardData: {
        cardname: '',
        username: '',
        key: '',
        status: '',
        data: {}
      }
    }
  },
  computed: {
    token() {
      return this.$store.state.token || localStorage.getItem('token')
    },
    username() {
      return this.$store.state.username || localStorage.getItem('username') || ''
    }
  },
  mounted() {
    this.fetchCard()
  },
  methods: {
    async fetchCard() {
      this.loading = true
      this.errorMsg = ''
      try {
        const resp = await axios.get(
          `http://127.0.0.1:5000/api/view/${this.cardname}`,
          {
            headers: {
              Authorization: `Bearer ${this.token}`
            }
          }
        )
        if (resp.status === 200) {
          this.cardData = resp.data
        }
      } catch (err) {
        if (err.response && err.response.data && err.response.data.error) {
          this.errorMsg = err.response.data.error
        } else {
          this.errorMsg = 'Could not load card details. Please ensure the card request exists.'
        }
      } finally {
        this.loading = false
      }
    },
    formatAadhaar(key) {
      if (!key) return 'XXXX XXXX XXXX'
      const cleaned = key.toString().replace(/\s+/g, '')
      if (cleaned.length === 12) {
        return `${cleaned.slice(0, 4)} ${cleaned.slice(4, 8)} ${cleaned.slice(8, 12)}`
      }
      return key
    },
    printCard() {
      window.print()
    }
  }
}
</script>

<style scoped>
.view-container {
  min-height: 85vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f1f5f9;
  padding: 40px 20px 80px;
}

.top-nav-bar {
  width: 100%;
  max-width: 650px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.btn-back {
  color: #4b5563;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  padding: 8px 14px;
  background: white;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  transition: 0.2s ease;
}

.btn-back:hover {
  background: #f3f4f6;
}

.btn-print {
  background: #42b883;
  color: white;
  border: none;
  font-weight: 600;
  font-size: 14px;
  padding: 9px 18px;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.2s ease;
}

.btn-print:hover {
  background: #369f6e;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.spinner {
  width: 36px;
  height: 36px;
  border: 4px solid #e5e7eb;
  border-top-color: #42b883;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.err-text {
  color: #dc2626;
  font-weight: 600;
  margin-bottom: 20px;
}

.card-display-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

/* SHARED CARD STYLING */
.id-card {
  width: 540px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
  overflow: hidden;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  position: relative;
}

.photo-frame {
  width: 90px;
  height: 110px;
  background: #e2e8f0;
  border: 2px solid #cbd5e1;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-icon {
  font-size: 55px;
}

.qr-mockup {
  width: 70px;
  height: 70px;
  background: #0f172a;
  border-radius: 4px;
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 10px;
}

.qr-pattern {
  width: 50px;
  height: 50px;
  background-image: radial-gradient(white 20%, transparent 20%),
                    radial-gradient(white 20%, transparent 20%);
  background-size: 10px 10px;
  background-position: 0 0, 5px 5px;
}

/* 1. AADHAAR CARD */
.aadhar-card {
  border: 1px solid #e2e8f0;
  background: #fffdfa;
}

.aadhar-top-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px 8px;
  background: #fafaf9;
}

.emblem-box {
  font-size: 26px;
}

.header-titles {
  text-align: center;
}

.header-titles h3 {
  font-size: 14px;
  margin: 0;
  color: #1c1917;
}

.header-titles h4 {
  font-size: 11px;
  margin: 0;
  color: #57534e;
  letter-spacing: 0.5px;
}

.aadhaar-logo {
  display: flex;
  align-items: center;
  gap: 4px;
}

.logo-sun {
  font-size: 22px;
  color: #ea580c;
}

.logo-text {
  font-size: 16px;
  font-weight: 800;
  color: #ea580c;
}

.tricolor-stripe {
  height: 4px;
  display: flex;
  width: 100%;
}

.stripe-saffron { flex: 1; background: #ff9933; }
.stripe-white { flex: 1; background: #ffffff; }
.stripe-green { flex: 1; background: #138808; }

.aadhar-body {
  display: flex;
  padding: 18px 22px;
  gap: 20px;
}

.aadhar-photo-col {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.aadhar-info-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 7px;
  justify-content: center;
}

.info-row {
  display: flex;
  font-size: 13px;
  line-height: 1.4;
}

.info-row .label {
  width: 110px;
  color: #78716c;
  font-weight: 500;
}

.info-row .value {
  color: #1c1917;
  flex: 1;
}

.info-row .value.strong {
  font-weight: 700;
  font-size: 15px;
}

.small-text {
  font-size: 12px;
}

.aadhar-footer {
  border-top: 1px solid #f5f5f4;
  background: #f5f5f4;
  padding: 12px 20px;
  text-align: center;
}

.aadhar-number {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: 3px;
  color: #1c1917;
}

.aadhar-motto {
  font-size: 11px;
  color: #78716c;
  margin-top: 2px;
}

/* 2. PAN CARD */
.pan-card {
  background: #f0f7ff;
  border: 1px solid #bfdbfe;
}

.pan-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: #1e3a8a;
  color: white;
}

.pan-title-left h3, .pan-title-right h3 {
  font-size: 11px;
  margin: 0;
}

.pan-title-left h4, .pan-title-right h4 {
  font-size: 9px;
  margin: 0;
  opacity: 0.85;
}

.emblem-wrap {
  font-size: 24px;
}

.pan-body {
  display: flex;
  padding: 18px 20px;
  gap: 16px;
}

.pan-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.pan-chip {
  width: 44px;
  height: 32px;
  background: linear-gradient(135deg, #d4af37, #fef08a);
  border-radius: 4px;
  border: 1px solid #ca8a04;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  padding: 2px 4px;
  box-sizing: border-box;
}

.chip-line {
  height: 1px;
  background: #854d0e;
}

.pan-photo {
  width: 80px;
  height: 95px;
  background: #e2e8f0;
  border: 1px solid #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pan-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.pan-field {
  display: flex;
  flex-direction: column;
}

.p-label {
  font-size: 10px;
  text-transform: uppercase;
  color: #475569;
  letter-spacing: 0.5px;
}

.p-val {
  font-size: 13px;
  color: #0f172a;
}

.p-val.strong {
  font-size: 15px;
  font-weight: 700;
}

.pan-number-box {
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 2px;
  color: #1e3a8a;
  margin-top: 2px;
  font-family: monospace;
}

.pan-right {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.mini-qr {
  width: 55px;
  height: 55px;
}

.signature-box {
  border-bottom: 1px solid #334155;
  text-align: center;
  padding-bottom: 2px;
}

.sign-font {
  font-family: "Brush Script MT", cursive, sans-serif;
  font-size: 18px;
  color: #0f172a;
  display: block;
}

.signature-box small {
  font-size: 9px;
  color: #64748b;
}

/* 3. VOTER CARD */
.voter-card {
  border: 2px solid #047857;
  background: #f0fdf4;
}

.voter-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 20px;
  background: #065f46;
  color: white;
}

.voter-emblem {
  font-size: 30px;
}

.voter-header-text h3 {
  font-size: 13px;
  margin: 0;
}

.voter-header-text h4 {
  font-size: 11px;
  margin: 0;
  opacity: 0.9;
}

.voter-header-text p {
  font-size: 10px;
  margin: 2px 0 0;
  letter-spacing: 1px;
  color: #a7f3d0;
}

.voter-body {
  display: flex;
  padding: 18px 22px;
  gap: 20px;
}

.voter-photo-side {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.voter-epic-code {
  font-family: monospace;
  font-weight: 800;
  font-size: 14px;
  background: #dcfce7;
  color: #065f46;
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid #86efac;
}

.voter-info-side {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.v-row {
  display: flex;
  flex-direction: column;
  font-size: 13px;
}

.v-label {
  font-size: 11px;
  color: #4b5563;
}

.v-val.strong {
  font-weight: 700;
  font-size: 15px;
  color: #111827;
}

.voter-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 20px;
  background: #dcfce7;
  font-size: 11px;
  color: #065f46;
  font-weight: 600;
}

.verified-tag {
  color: #047857;
}

/* 4. DRIVING LICENCE */
.dl-card {
  border: 1px solid #fed7aa;
  background: #fffaf5;
}

.dl-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  background: #ea580c;
  color: white;
}

.dl-flag {
  font-size: 24px;
}

.dl-titles h3 {
  font-size: 13px;
  margin: 0;
  letter-spacing: 0.5px;
}

.dl-titles p {
  font-size: 10px;
  margin: 0;
  opacity: 0.85;
}

.dl-badge {
  font-size: 13px;
  font-weight: 800;
  background: white;
  color: #ea580c;
  padding: 3px 8px;
  border-radius: 4px;
}

.dl-body {
  display: flex;
  padding: 18px 20px;
  gap: 18px;
}

.dl-photo-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.chip-mini {
  width: 40px;
  height: 28px;
  background: linear-gradient(135deg, #d4af37, #fef08a);
  border-radius: 4px;
  border: 1px solid #ca8a04;
}

.dl-info-box {
  flex: 1;
}

.dl-licence-num {
  margin-bottom: 12px;
  padding-bottom: 6px;
  border-bottom: 1px dashed #fed7aa;
}

.dl-licence-num .d-label {
  font-size: 11px;
  color: #7c2d12;
  font-weight: 600;
  margin-right: 8px;
}

.dl-licence-num .d-num {
  font-family: monospace;
  font-size: 16px;
  font-weight: 800;
  color: #9a3412;
}

.dl-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.d-field {
  display: flex;
  flex-direction: column;
}

.d-label {
  font-size: 11px;
  color: #6b7280;
}

.d-val {
  font-size: 13px;
  color: #1f2937;
}

.d-val.strong {
  font-weight: 700;
  font-size: 14px;
}

.highlight-val {
  color: #c2410c;
  font-weight: 600;
}

.dl-footer {
  display: flex;
  justify-content: space-between;
  padding: 8px 20px;
  background: #ffedd5;
  font-size: 11px;
  color: #9a3412;
  font-weight: 600;
}

/* Status banner */
.card-status-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  padding: 12px 20px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.status-pill {
  font-size: 12px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 20px;
  text-transform: uppercase;
}

.status-generated {
  background: #dcfce7;
  color: #15803d;
}

.status-tip {
  font-size: 13px;
  color: #64748b;
}

/* PRINT MEDIA QUERY */
@media print {
  .no-print {
    display: none !important;
  }
  .view-container {
    background: transparent !important;
    padding: 0 !important;
  }
  .id-card {
    box-shadow: none !important;
    border: 1px solid #aaa !important;
  }
}
</style>
