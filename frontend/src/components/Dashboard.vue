<template>
  <div class="dashboard-page" v-if="token">
    <!-- USER DASHBOARD -->
    <div v-if="role === 'user'" class="dashboard-container">
      <div class="dashboard-header">
        <div class="welcome-box">
          <h2>Welcome, {{ userData.username }}! 👋</h2>
          <p>Manage your identity cards, track verification progress, and request new digital e-cards.</p>
        </div>
        <div class="header-action">
          <router-link to="/profile" class="btn-profile">View Profile</router-link>
        </div>
      </div>

      <!-- Quick Request Shortcuts -->
      <div class="quick-request-section">
        <h3>Request a New Identity Card</h3>
        <div class="request-grid">
          <router-link to="/request/aadhar" class="request-tile">
            <span class="tile-icon">🇮🇳</span>
            <div class="tile-info">
              <strong>Aadhaar Card</strong>
              <small>UIDAI Resident ID</small>
            </div>
            <span class="tile-arrow">→</span>
          </router-link>

          <router-link to="/request/pan" class="request-tile">
            <span class="tile-icon">💳</span>
            <div class="tile-info">
              <strong>PAN Card</strong>
              <small>Income Tax Dept</small>
            </div>
            <span class="tile-arrow">→</span>
          </router-link>

          <router-link to="/request/voter" class="request-tile">
            <span class="tile-icon">🗳️</span>
            <div class="tile-info">
              <strong>Voter ID</strong>
              <small>Election Commission</small>
            </div>
            <span class="tile-arrow">→</span>
          </router-link>

          <router-link to="/request/driving" class="request-tile">
            <span class="tile-icon">🚗</span>
            <div class="tile-info">
              <strong>Driving Licence</strong>
              <small>Transport Authority</small>
            </div>
            <span class="tile-arrow">→</span>
          </router-link>
        </div>
      </div>

      <!-- Notification message -->
      <div v-if="actionNotice" class="alert alert-info">
        {{ actionNotice }}
      </div>

      <!-- 1. Available / Generated E-Cards -->
      <div class="table-card">
        <div class="table-card-header">
          <h3>Generated Digital E-Cards</h3>
          <span class="badge-count">{{ (userData.available_cards || []).length }} Active</span>
        </div>

        <div v-if="userData.available_cards && userData.available_cards.length > 0">
          <table class="data-table">
            <thead>
              <tr>
                <th>Card Type</th>
                <th>Card Number / Key</th>
                <th>Status</th>
                <th style="text-align: right;">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="card in userData.available_cards" :key="card.cardname">
                <td class="font-bold card-title-cell">
                  <span class="card-type-icon">{{ getCardIcon(card.cardname) }}</span>
                  {{ formatCardName(card.cardname) }}
                </td>
                <td class="key-cell font-mono">
                  {{ card.key ? card.key : 'Verified' }}
                </td>
                <td>
                  <span class="status-badge status-generated">Generated</span>
                </td>
                <td style="text-align: right;">
                  <button class="btn-action btn-view" @click="viewCard(card.cardname)">
                    👁️ View Digital Card
                  </button>
                  <button class="btn-action btn-delete" @click="deleteUserCard(card.cardname)">
                    🗑️ Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="empty-box">
          <p>No generated cards yet. Once your requested cards are approved, they will appear here.</p>
        </div>
      </div>

      <!-- 2. Pending Requests -->
      <div class="table-card">
        <div class="table-card-header">
          <h3>Pending Card Requests</h3>
          <span class="badge-count">{{ (userData.card_requests || []).length }} In Progress</span>
        </div>

        <div v-if="userData.card_requests && userData.card_requests.length > 0">
          <table class="data-table">
            <thead>
              <tr>
                <th>Card Type</th>
                <th>Current Status</th>
                <th style="text-align: right;">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="card in userData.card_requests" :key="card.cardname">
                <td class="font-bold card-title-cell">
                  <span class="card-type-icon">{{ getCardIcon(card.cardname) }}</span>
                  {{ formatCardName(card.cardname) }}
                </td>
                <td>
                  <span :class="['status-badge', getStatusBadgeClass(card.status)]">
                    {{ formatStatus(card.status) }}
                  </span>
                </td>
                <td style="text-align: right;">
                  <button class="btn-action btn-delete" @click="deleteUserCard(card.cardname)">
                    Cancel Request
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="empty-box">
          <p>No active pending requests. Click any card above to submit a request.</p>
        </div>
      </div>
    </div>

    <!-- ADMIN DASHBOARD -->
    <div v-else class="dashboard-container">
      <div class="dashboard-header admin-header">
        <div class="welcome-box">
          <h2>Admin Control Center 🛡️</h2>
          <p>Administrator: <strong>{{ userData.admin_name }}</strong> | Verification and Card Issuance Portal</p>
        </div>
        <div class="header-action">
          <button class="btn-refresh" @click="loadData">🔄 Refresh Data</button>
        </div>
      </div>

      <!-- Admin Stat Metrics -->
      <div class="admin-metrics-grid">
        <div class="metric-card">
          <div class="metric-icon">👥</div>
          <div class="metric-val">{{ userData.users || 0 }}</div>
          <div class="metric-lbl">Citizen Users</div>
        </div>
        <div class="metric-card">
          <div class="metric-icon color-yellow">⏳</div>
          <div class="metric-val">{{ userData.card_requests || 0 }}</div>
          <div class="metric-lbl">Requested</div>
        </div>
        <div class="metric-card">
          <div class="metric-icon color-blue">🔍</div>
          <div class="metric-val">{{ userData.under_verification || 0 }}</div>
          <div class="metric-lbl">Under Verification</div>
        </div>
        <div class="metric-card">
          <div class="metric-icon color-purple">✅</div>
          <div class="metric-val">{{ userData.verified || 0 }}</div>
          <div class="metric-lbl">Verified</div>
        </div>
        <div class="metric-card">
          <div class="metric-icon color-green">🪪</div>
          <div class="metric-val">{{ userData.card_granted || 0 }}</div>
          <div class="metric-lbl">Cards Granted</div>
        </div>
      </div>

      <!-- Celery Async CSV Export Card -->
      <div class="export-banner">
        <div class="export-info">
          <h4>📊 Celery Asynchronous CSV Export</h4>
          <p>Export all card database records asynchronously using the Celery background worker.</p>
        </div>
        <div class="export-actions">
          <button class="btn-export" @click="triggerExport" :disabled="exportLoading">
            {{ exportLoading ? '⏳ Processing Celery Task...' : '📥 Export All Cards (CSV)' }}
          </button>
          <a
            v-if="exportDownloadUrl"
            :href="exportDownloadUrl"
            target="_blank"
            download
            class="btn-download"
          >
            💾 Download Ready CSV
          </a>
        </div>
      </div>
      <div v-if="exportStatusMsg" class="export-status-box">
        {{ exportStatusMsg }}
      </div>

      <!-- Notification message -->
      <div v-if="actionNotice" class="alert alert-info">
        {{ actionNotice }}
      </div>

      <!-- Requests Management Table -->
      <div class="table-card">
        <div class="table-card-header">
          <h3>Card Requests & Issuance</h3>
          <div class="search-box">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search by user or card..."
              class="search-input"
            />
          </div>
        </div>

        <div v-if="filteredRequests && filteredRequests.length > 0">
          <table class="data-table">
            <thead>
              <tr>
                <th>User ID</th>
                <th>Citizen Username</th>
                <th>Card Type</th>
                <th>Current Status</th>
                <th>Change Status</th>
                <th>Issue / Generate</th>
                <th style="text-align: right;">Remove</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="req in filteredRequests" :key="req.id || (req.user_id + '-' + req.cardname)">
                <td class="font-mono">#{{ req.user_id }}</td>
                <td class="font-bold">
                  {{ req.username }}
                  <small v-if="req.email" class="sub-email">{{ req.email }}</small>
                </td>
                <td class="font-bold card-title-cell">
                  <span class="card-type-icon">{{ getCardIcon(req.cardname) }}</span>
                  {{ formatCardName(req.cardname) }}
                </td>
                <td>
                  <span :class="['status-badge', getStatusBadgeClass(req.status)]">
                    {{ formatStatus(req.status) }}
                  </span>
                </td>
                <td>
                  <select
                    :value="req.status"
                    @change="updateStatus(req.cardname, req.user_id, $event.target.value)"
                    class="status-select"
                  >
                    <option value="requested">Requested</option>
                    <option value="under_verification">Under Verification</option>
                    <option value="verified">Verified</option>
                    <option value="generated">Generated</option>
                  </select>
                </td>
                <td>
                  <button
                    class="btn-action btn-generate"
                    :disabled="req.status === 'generated'"
                    @click="generateCard(req.cardname, req.user_id)"
                  >
                    {{ req.status === 'generated' ? '✓ Generated' : '⚡ Generate Key' }}
                  </button>
                </td>
                <td style="text-align: right;">
                  <button class="btn-action btn-delete" @click="deleteAdminCard(req.cardname, req.user_id)">
                    🗑️
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="empty-box">
          <p>No card requests found matching your filter.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      token: '',
      role: '',
      userData: {},
      searchQuery: '',
      actionNotice: '',
      exportLoading: false,
      exportStatusMsg: '',
      exportDownloadUrl: '',
      exportPollInterval: null
    }
  },
  computed: {
    filteredRequests() {
      const details = this.userData.card_request_details || []
      if (!this.searchQuery.trim()) return details
      const q = this.searchQuery.toLowerCase()
      return details.filter(d =>
        (d.username && d.username.toLowerCase().includes(q)) ||
        (d.cardname && d.cardname.toLowerCase().includes(q)) ||
        (d.status && d.status.toLowerCase().includes(q))
      )
    }
  },
  mounted() {
    this.loadToken()
    this.loadData()
  },
  beforeUnmount() {
    if (this.exportPollInterval) {
      clearInterval(this.exportPollInterval)
    }
  },
  methods: {
    loadToken() {
      const token = localStorage.getItem('token') || this.$store.state.token
      if (token) {
        this.token = token
      } else {
        this.$router.push('/login')
      }
    },
    async loadData() {
      try {
        const resp = await axios.get('http://127.0.0.1:5000/api/dashboard', {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${this.token}`
          }
        })
        if (resp.status === 200) {
          this.userData = resp.data
          this.role = resp.data.role
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.$store.dispatch('logout')
          this.$router.push('/login')
        }
      }
    },
    formatCardName(name) {
      if (!name) return ''
      if (name.toLowerCase() === 'aadhar') return 'Aadhaar Card'
      if (name.toLowerCase() === 'pan') return 'PAN Card'
      if (name.toLowerCase() === 'voter' || name.toLowerCase() === 'election') return 'Voter ID'
      if (name.toLowerCase() === 'driving') return 'Driving Licence'
      return name.charAt(0).toUpperCase() + name.slice(1)
    },
    formatStatus(status) {
      if (!status) return ''
      return status.replace(/_/g, ' ').toUpperCase()
    },
    getCardIcon(name) {
      if (!name) return '🪪'
      const n = name.toLowerCase()
      if (n === 'aadhar') return '🇮🇳'
      if (n === 'pan') return '💳'
      if (n === 'voter' || n === 'election') return '🗳️'
      if (n === 'driving') return '🚗'
      return '🪪'
    },
    getStatusBadgeClass(status) {
      if (status === 'generated') return 'status-generated'
      if (status === 'verified') return 'status-verified'
      if (status === 'under_verification') return 'status-under-verification'
      return 'status-requested'
    },
    viewCard(cardname) {
      this.$router.push(`/view/${cardname}`)
    },
    async deleteUserCard(cardname) {
      if (!confirm(`Are you sure you want to delete / cancel your ${this.formatCardName(cardname)}?`)) {
        return
      }
      try {
        const resp = await axios.post(
          `http://127.0.0.1:5000/api/delete/${cardname}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${this.token}`
            }
          }
        )
        if (resp.status === 200) {
          this.actionNotice = `Successfully removed ${this.formatCardName(cardname)}.`
          setTimeout(() => { this.actionNotice = '' }, 3000)
          this.loadData()
        }
      } catch (err) {
        alert('Failed to delete card.')
      }
    },
    async deleteAdminCard(cardname, userId) {
      if (!confirm(`Are you sure you want to delete ${this.formatCardName(cardname)} for user #${userId}?`)) {
        return
      }
      try {
        const resp = await axios.post(
          `http://127.0.0.1:5000/api/delete/${cardname}/${userId}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${this.token}`
            }
          }
        )
        if (resp.status === 200) {
          this.actionNotice = `Removed ${cardname} for user #${userId}.`
          setTimeout(() => { this.actionNotice = '' }, 3000)
          this.loadData()
        }
      } catch (err) {
        alert('Failed to delete card record.')
      }
    },
    async updateStatus(cardname, userId, newStatus) {
      try {
        const resp = await axios.post(
          `http://127.0.0.1:5000/api/update/${cardname}/${userId}`,
          { status: newStatus },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${this.token}`
            }
          }
        )
        if (resp.status === 200) {
          this.actionNotice = `Status updated to ${this.formatStatus(newStatus)} for user #${userId}.`
          setTimeout(() => { this.actionNotice = '' }, 3000)
          this.loadData()
        }
      } catch (err) {
        alert('Could not update status.')
      }
    },
    async generateCard(cardname, userId) {
      try {
        const resp = await axios.post(
          `http://127.0.0.1:5000/api/generate/${cardname}/${userId}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${this.token}`
            }
          }
        )
        if (resp.status === 200) {
          this.actionNotice = `Generated ${cardname} card for user #${userId}! Key: ${resp.data.key}`
          setTimeout(() => { this.actionNotice = '' }, 4000)
          this.loadData()
        }
      } catch (err) {
        alert('Failed to generate card.')
      }
    },
    async triggerExport() {
      this.exportLoading = true
      this.exportDownloadUrl = ''
      this.exportStatusMsg = 'Triggered Celery async export task. Waiting for background worker...'

      try {
        const resp = await axios.get('http://127.0.0.1:5000/export_csv', {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })
        const taskId = resp.data.id

        // Poll Celery status
        if (this.exportPollInterval) clearInterval(this.exportPollInterval)

        this.exportPollInterval = setInterval(async () => {
          try {
            const statusResp = await axios.get(`http://127.0.0.1:5000/api/csv_status/${taskId}`)
            const data = statusResp.data
            this.exportStatusMsg = `Task Status: ${data.state}...`

            if (data.ready) {
              clearInterval(this.exportPollInterval)
              this.exportLoading = false
              if (data.successful) {
                this.exportStatusMsg = `CSV Report successfully created: ${data.filename}`
                this.exportDownloadUrl = `http://127.0.0.1:5000/api/csv_result/${taskId}`
              } else {
                this.exportStatusMsg = 'CSV Generation failed in worker.'
              }
            }
          } catch (e) {
            clearInterval(this.exportPollInterval)
            this.exportLoading = false
            this.exportStatusMsg = 'Could not poll task status.'
          }
        }, 1500)
      } catch (err) {
        this.exportLoading = false
        this.exportStatusMsg = 'Could not trigger Celery CSV export task.'
      }
    }
  }
}
</script>

<style scoped>
.dashboard-page {
  background: #f7f9fc;
  min-height: calc(100vh - 125px);
  padding: 30px 20px 60px;
}

.dashboard-container {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 24px 30px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
}

.welcome-box h2 {
  font-size: 24px;
  font-weight: 800;
  color: #1f2937;
  margin: 0 0 6px;
}

.welcome-box p {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}

.btn-profile,
.btn-refresh {
  padding: 9px 18px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: 0.2s ease;
}

.btn-profile {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-profile:hover {
  background: #e5e7eb;
}

.btn-refresh {
  background: #42b883;
  color: white;
  border: none;
}

.btn-refresh:hover {
  background: #369f6e;
}

/* Quick request cards */
.quick-request-section h3 {
  font-size: 16px;
  font-weight: 700;
  color: #374151;
  margin: 0 0 14px;
}

.request-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.request-tile {
  background: white;
  padding: 16px 18px;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 14px;
  transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

.request-tile:hover {
  transform: translateY(-2px);
  border-color: #42b883;
  box-shadow: 0 4px 12px rgba(66, 184, 131, 0.12);
}

.tile-icon {
  font-size: 28px;
}

.tile-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.tile-info strong {
  font-size: 14px;
  color: #1f2937;
}

.tile-info small {
  font-size: 11px;
  color: #6b7280;
}

.tile-arrow {
  font-size: 18px;
  color: #42b883;
  font-weight: 700;
}

/* Admin Metrics */
.admin-metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.metric-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

.metric-icon {
  font-size: 26px;
  margin-bottom: 6px;
}

.metric-val {
  font-size: 28px;
  font-weight: 800;
  color: #1f2937;
}

.metric-lbl {
  font-size: 12px;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  margin-top: 4px;
}

/* Celery Export Banner */
.export-banner {
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
  border-radius: 10px;
  padding: 18px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 14px;
}

.export-info h4 {
  margin: 0 0 4px;
  color: #065f46;
  font-size: 16px;
}

.export-info p {
  margin: 0;
  color: #047857;
  font-size: 13px;
}

.export-actions {
  display: flex;
  gap: 12px;
}

.btn-export {
  padding: 9px 18px;
  background: #059669;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  transition: 0.2s ease;
}

.btn-export:hover:not(:disabled) {
  background: #047857;
}

.btn-export:disabled {
  opacity: 0.6;
}

.btn-download {
  padding: 9px 18px;
  background: #2563eb;
  color: white;
  border-radius: 6px;
  font-weight: 600;
  font-size: 13px;
  text-decoration: none;
  transition: 0.2s ease;
}

.btn-download:hover {
  background: #1d4ed8;
}

.export-status-box {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #1e40af;
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
}

.alert-info {
  background: #f0fdf4;
  color: #166534;
  border: 1px solid #bbf7d0;
  padding: 12px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
}

/* Data Table Card */
.table-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
}

.table-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 24px;
  border-bottom: 1px solid #f3f4f6;
}

.table-card-header h3 {
  font-size: 17px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.badge-count {
  background: #f3f4f6;
  color: #4b5563;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.search-input {
  padding: 7px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 13px;
  width: 220px;
}

.search-input:focus {
  outline: none;
  border-color: #42b883;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.data-table th {
  background: #f9fafb;
  padding: 12px 20px;
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  border-bottom: 1px solid #e5e7eb;
}

.data-table td {
  padding: 14px 20px;
  font-size: 14px;
  color: #374151;
  border-bottom: 1px solid #f3f4f6;
  vertical-align: middle;
}

.card-title-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-type-icon {
  font-size: 18px;
}

.font-bold {
  font-weight: 600;
}

.font-mono {
  font-family: monospace;
}

.sub-email {
  display: block;
  font-size: 11px;
  color: #6b7280;
  font-weight: normal;
}

/* Status Badges */
.status-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-generated {
  background: #dcfce7;
  color: #15803d;
}

.status-verified {
  background: #e0e7ff;
  color: #4338ca;
}

.status-under-verification {
  background: #fef3c7;
  color: #92400e;
}

.status-requested {
  background: #fee2e2;
  color: #991b1b;
}

.status-select {
  padding: 6px 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 13px;
  background: white;
}

/* Action Buttons */
.btn-action {
  padding: 7px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: 0.2s ease;
  margin-left: 6px;
}

.btn-view {
  background: #42b883;
  color: white;
}

.btn-view:hover {
  background: #369f6e;
}

.btn-generate {
  background: #3b82f6;
  color: white;
}

.btn-generate:hover:not(:disabled) {
  background: #2563eb;
}

.btn-generate:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn-delete {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.btn-delete:hover {
  background: #fee2e2;
}

.empty-box {
  padding: 40px 20px;
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
}
</style>