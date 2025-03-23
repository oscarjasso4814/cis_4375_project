<!-- CustomerProfile.vue -->
<template>
  <!-- Full page layout -->
  <div class="profile-container">
    <!-- Header with customer name and quick actions -->
    <header class="profile-header">
      <div class="customer-title">
        <h1>{{ customer.name }}</h1>
        <span class="customer-id">ID: {{ customer.id }}</span>
        <span class="badge" :class="customer.status.toLowerCase()">{{ customer.status }}</span>
        <span class="badge sub-status" v-if="customer.subStatus !== 'None'">{{ customer.subStatus }}</span>
      </div>
      <div class="quick-actions">
        <button class="icon-btn" title="Print Profile" @click="printProfile">
          <i class="fas fa-print"></i>
        </button>
        <button class="icon-btn" title="Video Call" @click="startVideoCall">
          <i class="fas fa-video"></i>
        </button>
      </div>
    </header>

    <!-- Main Layout -->
    <div class="profile-layout">
      <!-- Left Sidebar - Customer Info -->
      <div class="sidebar left-sidebar">
        <div class="sidebar-panel customer-panel">
          <h3>Customer Information</h3>
          <div class="customer-summary">
            <div class="info-section">
              <h4>Contact</h4>
              <div class="info-item">
                <i class="fas fa-mobile-alt"></i>
                <span>{{ customer.cell }}</span>
              </div>
              <div class="info-item">
                <i class="fas fa-envelope"></i>
                <span>{{ customer.email }}</span>
              </div>
            </div>
            
            <div class="info-section">
              <h4>Address</h4>
              <div class="info-item">
                <i class="fas fa-map-marker-alt"></i>
                <address>
                  {{ customer.address.street }}<br>
                  {{ customer.address.city }}, {{ customer.address.state }} {{ customer.address.zip }}
                </address>
              </div>
            </div>
            
            <div class="info-section">
              <h4>Personal Details</h4>
              <div class="info-item">
                <i class="fas fa-birthday-cake"></i>
                <span>DOB: {{ customer.dob }}</span>
              </div>
              <div class="info-item">
                <i class="fas fa-user"></i>
                <span>{{ customer.gender }}, {{ customer.maritalStatus }}</span>
              </div>
              <div class="info-item">
                <i class="fas fa-id-card"></i>
                <span>SSN: {{ customer.ssnTaxId }}</span>
              </div>
            </div>
            
            <div class="info-section">
              <h4>Account Details</h4>
              <div class="info-item">
                <i class="fas fa-users"></i>
                <span>Type: {{ customer.customerType }}</span>
              </div>
              <div class="info-item">
                <i class="fas fa-user-tie"></i>
                <span>Agent: {{ customer.agentOfRecord }}</span>
              </div>
              <div class="info-item">
                <i class="fas fa-calendar-alt"></i>
                <span>Added: {{ customer.dateAdded }}</span>
              </div>
            </div>
            
            <div class="info-section">
              <h4>Household</h4>
              <div class="info-item">
                <i class="fas fa-home"></i>
                <span>Size: {{ customer.householdSize }}</span>
              </div>
              <div class="info-item">
                <i class="fas fa-dollar-sign"></i>
                <span>Income: {{ customer.householdIncome }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Middle Content - Policy Information -->
      <div class="main-content">
        <!-- Insurance Type Tabs -->
        <div class="insurance-tabs">
          <button 
            v-for="type in insuranceTypes" 
            :key="type.value"
            class="tab-btn" 
            :class="{ active: activeInsuranceType === type.value }" 
            @click="activeInsuranceType = type.value"
          >
            <i :class="type.icon"></i>
            {{ type.label }}
          </button>
        </div>

        <!-- Policy Content Area -->
        <div class="policy-content">
          <div class="policy-header">
            <h3>{{ activeInsuranceType }} Insurance Policies</h3>
            <button class="add-policy-btn" @click="addNewPolicy">
              <i class="fas fa-plus"></i> Add Policy
            </button>
          </div>
          
          <div class="policy-list">
            <template v-if="getPolicies(activeInsuranceType).length > 0">
              <div v-for="policy in getPolicies(activeInsuranceType)" :key="policy.id" class="policy-card">
                <div class="policy-card-header">
                  <h4>{{ policy.name }}</h4>
                  <span class="policy-number">{{ policy.number }}</span>
                </div>
                <div class="policy-card-body">
                  <div class="policy-detail">
                    <span class="detail-label">Coverage:</span>
                    <span class="detail-value">{{ policy.coverage }}</span>
                  </div>
                  <div class="policy-detail">
                    <span class="detail-label">Premium:</span>
                    <span class="detail-value">{{ policy.premium }}</span>
                  </div>
                  <div class="policy-detail">
                    <span class="detail-label">Start Date:</span>
                    <span class="detail-value">{{ policy.startDate }}</span>
                  </div>
                  <div class="policy-detail" v-if="policy.beneficiary">
                    <span class="detail-label">Beneficiary:</span>
                    <span class="detail-value">{{ policy.beneficiary }}</span>
                  </div>
                </div>
                <div class="policy-card-footer">
                  <button class="small-btn">View Details</button>
                  <button class="small-btn">Edit</button>
                </div>
              </div>
            </template>
            <div v-else class="no-policies">
              <div class="empty-state">
                <i class="fas fa-folder-open"></i>
                <p>No {{ activeInsuranceType }} policies found</p>
                <button class="add-policy-btn" @click="addNewPolicy">
                  <i class="fas fa-plus"></i> Add New Policy
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Sidebar - Action Items -->
      <div class="sidebar right-sidebar">
        <div class="sidebar-panel action-panel">
          <h3>Actions</h3>
          <div class="action-list">
            <button class="action-btn" @click="addNewPolicy">
              <i class="fas fa-file-medical"></i>
              <span>New Policy</span>
            </button>
            <button class="action-btn" @click="addNote">
              <i class="fas fa-sticky-note"></i>
              <span>Add Note</span>
            </button>
            <button class="action-btn" @click="openACORDForms">
              <i class="fas fa-file-alt"></i>
              <span>ACORD Forms</span>
            </button>
            <button class="action-btn" @click="sendThankYouLetter">
              <i class="fas fa-envelope-open-text"></i>
              <span>Thank You</span>
            </button>
            <button class="action-btn" @click="addChangeRequest">
              <i class="fas fa-exchange-alt"></i>
              <span>Change Request</span>
            </button>
            <button class="action-btn" @click="openMailingServices">
              <i class="fas fa-mail-bulk"></i>
              <span>Mailing</span>
            </button>
          </div>
        </div>
        
        <div class="sidebar-panel recent-panel">
          <h3>Recent Activity</h3>
          <div class="activity-list">
            <div class="activity-item">
              <div class="activity-icon"><i class="fas fa-file-alt"></i></div>
              <div class="activity-content">
                <div class="activity-title">Policy Updated</div>
                <div class="activity-desc">Life insurance coverage increased</div>
                <div class="activity-time">2 days ago</div>
              </div>
            </div>
            <div class="activity-item">
              <div class="activity-icon"><i class="fas fa-phone"></i></div>
              <div class="activity-content">
                <div class="activity-title">Phone Call</div>
                <div class="activity-desc">Discussed policy options</div>
                <div class="activity-time">1 week ago</div>
              </div>
            </div>
            <div class="activity-item">
              <div class="activity-icon"><i class="fas fa-envelope"></i></div>
              <div class="activity-content">
                <div class="activity-title">Email Sent</div>
                <div class="activity-desc">Quote for new home policy</div>
                <div class="activity-time">Mar 15, 2025</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';

// Insurance type tabs with icons
const insuranceTypes = [
  { label: 'Life', value: 'LIFE', icon: 'fas fa-heartbeat' },
  { label: 'Health', value: 'Health', icon: 'fas fa-medkit' },
  { label: 'Medicare', value: 'Medicare', icon: 'fas fa-hospital' },
  { label: 'Auto', value: 'Auto', icon: 'fas fa-car' },
  { label: 'Home', value: 'HOME', icon: 'fas fa-home' },
  { label: 'Other', value: 'Other', icon: 'fas fa-umbrella' }
];

// Customer data (keeping the same data from your original component)
const customer = reactive({
  name: 'John Doe',
  address: {
    street: '13135 Dairy Ashford Rd',
    city: 'Sugar Land',
    state: 'TX',
    zip: '77478'
  },
  addressVerified: true,
  mailingAddress: '',
  email: 'john.doe@example.com',
  email2: '',
  cell: '(555) 123-4567',
  phone2: '',
  phone3: '',
  phone4: '',
  language: 'English',
  preferredContact: 'Email',
  ssnTaxId: '***-**-0000',
  maritalStatus: 'Single',
  gender: 'Male',
  id: '173565915',
  customerType: 'Personal Lines',
  accountType: 'Prospect',
  status: 'Active',
  subStatus: 'None',
  agentOfRecord: 'Amin Lalani',
  csr: 'Amin Lalani',
  keyedBy: 'Amin Lalani',
  office: 'Main Office',
  source: 'Personal Contacts',
  subSource: '',
  dateAdded: 'Thu Feb 06, 2025',
  dob: '01/15/1980',
  dl: '',
  dlState: '',
  dateLicensed: '',
  householdSize: '3',
  peopleApplying: '1',
  householdIncome: '$85,000',
  preferences: {
    'Do Not Email': 'No',
    'Do Not Text': 'No',
    'Do Not Call': 'No',
    'Do Not Mail': 'No',
    'Do Not Market': 'No',
    'Do Not Capture Email': 'No'
  },
  relationships: [],
  tags: []
});

// Sample policies data
const policies = reactive([
  {
    id: 1,
    type: 'LIFE',
    name: 'Term Life Insurance',
    number: 'LF-7832',
    coverage: '$750,000',
    premium: '$125/month',
    startDate: '03/01/2025',
    beneficiary: 'Jane Doe'
  },
  {
    id: 2,
    type: 'LIFE',
    name: 'Whole Life Policy',
    number: 'LF-7833',
    coverage: '$250,000',
    premium: '$175/month',
    startDate: '01/15/2025',
    beneficiary: 'Jane Doe'
  },
  {
    id: 3,
    type: 'Auto',
    name: 'Auto Insurance',
    number: 'AU-5429',
    coverage: 'Full Coverage',
    premium: '$98/month',
    startDate: '02/10/2025'
  },
  {
    id: 4,
    type: 'HOME',
    name: 'Homeowners Insurance',
    number: 'HO-3392',
    coverage: '$450,000',
    premium: '$145/month',
    startDate: '12/20/2024'
  }
]);

// Active insurance type tab
const activeInsuranceType = ref('LIFE');

// Get policies by type
const getPolicies = (type) => {
  return policies.filter(policy => policy.type === type);
};

// Action methods
const printProfile = () => {
  console.log('Printing customer profile...');
  // Implementation would go here
};

const startVideoCall = () => {
  console.log('Starting video call...');
  // Implementation would go here
};

const openACORDForms = () => {
  console.log('Opening ACORD/Custom Forms...');
  // Implementation would go here
};

const addNewPolicy = () => {
  console.log('Opening Add New Policy form...');
  // Implementation would go here
};

const addNote = () => {
  console.log('Opening Add Note form...');
  // Implementation would go here
};

const sendThankYouLetter = () => {
  console.log('Opening Thank You Letter template...');
  // Implementation would go here
};

const addChangeRequest = () => {
  console.log('Opening Add Change Request form...');
  // Implementation would go here
};

const openMailingServices = () => {
  console.log('Opening Mailing Services...');
  // Implementation would go here
};

// Lifecycle hook
onMounted(() => {
  console.log('Updated customer profile component mounted');
  // You could fetch customer data here
});
</script>

<style scoped>
/* Base Styles */
/* Base Styles */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}

.profile-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
  background-color: #121212;
  color: #f5f5f5;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Header */
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background-color: #1e1e1e;
  border-bottom: 1px solid #333;
  height: 60px;
  width: 100%;
  box-sizing: border-box;
}

.customer-title {
  display: flex;
  align-items: center;
  gap: 15px;
}

.customer-title h1 {
  font-size: 18px;
  margin: 0;
  color: #fff;
  font-weight: 600;
}

.customer-id {
  color: #aaa;
  font-size: 14px;
}

.quick-actions {
  display: flex;
  gap: 10px;
}

.icon-btn {
  background-color: #2d2d2d;
  border: none;
  color: #f5f5f5;
  width: 36px;
  height: 36px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.icon-btn:hover {
  background-color: #444;
}

/* Badge */
.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
  background-color: #2b90c5;
  color: white;
}

.badge.active {
  background-color: #2ecc71;
}

.badge.inactive {
  background-color: #e74c3c;
}

.sub-status {
  background-color: #444;
}

/* Main Layout */
.profile-layout {
  display: flex;
  flex: 1;
  width: 100%;
  overflow: hidden;
  box-sizing: border-box;
}

/* Sidebar Styling */
.sidebar {
  width: 20%;
  min-width: 240px;
  overflow-y: auto;
  padding: 16px;
  background-color: #121212;
  box-sizing: border-box;
}

.sidebar-panel {
  background-color: #1e1e1e;
  border: 1px solid #333;
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 16px;
}

.sidebar-panel h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 15px;
  color: #fff;
  font-weight: 600;
}

.sidebar-panel h4 {
  font-size: 13px;
  color: #aaa;
  margin: 10px 0 5px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

/* Customer Info Panel */
.customer-panel {
  height: auto;
}

.info-section {
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #333;
}

.info-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 8px;
  font-size: 13px;
  color: #f5f5f5;
}

.info-item i {
  width: 16px;
  color: #aaa;
}

.info-item address {
  font-style: normal;
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 16px;
  background-color: #121212;
  min-width: 50%;
  box-sizing: border-box;
}

/* Insurance Type Tabs */
.insurance-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 16px;
  background-color: #1e1e1e;
  padding: 6px;
  border-radius: 6px;
}

.tab-btn {
  padding: 8px 16px;
  border: none;
  background-color: transparent;
  color: #aaa;
  cursor: pointer;
  font-size: 13px;
  border-radius: 4px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.tab-btn i {
  font-size: 14px;
}

.tab-btn:hover {
  background-color: #2d2d2d;
  color: #fff;
}

.tab-btn.active {
  background-color: #2d2d2d;
  color: #fff;
  font-weight: 500;
}

/* Policy Content Area */
.policy-content {
  flex: 1;
  background-color: #1e1e1e;
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.policy-header {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #333;
}

.policy-header h3 {
  margin: 0;
  font-size: 16px;
  color: #fff;
}

.add-policy-btn {
  background-color: #2b90c5;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background-color 0.2s;
}

.add-policy-btn:hover {
  background-color: #1e7eb1;
}

.add-policy-btn i {
  font-size: 12px;
}

/* Policy List */
.policy-list {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.policy-card {
  background-color: #2d2d2d;
  border-radius: 6px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.policy-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.policy-card-header {
  padding: 12px 16px;
  background-color: #333;
  border-bottom: 1px solid #444;
}

.policy-card-header h4 {
  margin: 0 0 4px 0;
  font-size: 14px;
  color: #fff;
}

.policy-number {
  font-size: 12px;
  color: #aaa;
}

.policy-card-body {
  padding: 16px;
}

.policy-detail {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
}

.detail-label {
  color: #aaa;
}

.detail-value {
  font-weight: 500;
}

.policy-card-footer {
  padding: 12px 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  border-top: 1px solid #444;
}

.small-btn {
  padding: 6px 12px;
  background-color: transparent;
  color: #f5f5f5;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.small-btn:hover {
  background-color: #444;
}

/* Empty State */
.no-policies {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}

.empty-state {
  text-align: center;
  padding: 30px;
}

.empty-state i {
  font-size: 48px;
  color: #555;
  margin-bottom: 16px;
}

.empty-state p {
  color: #aaa;
  margin-bottom: 16px;
}

/* Right Sidebar */
.right-sidebar {
  background-color: #121212;
  width: 20%;
  min-width: 240px;
}

/* Action Items */
.action-panel {
  margin-bottom: 16px;
}

.action-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.action-btn {
  padding: 12px;
  background-color: #2d2d2d;
  color: #f5f5f5;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  text-align: left;
  font-size: 13px;
  transition: background-color 0.2s;
}

.action-btn i {
  width: 16px;
  text-align: center;
  color: #2b90c5;
}

.action-btn:hover {
  background-color: #3a3a3a;
}

/* Recent Activity */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  gap: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #333;
}

.activity-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #2d2d2d;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2b90c5;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 13px;
  font-weight: 500;
  color: #f5f5f5;
  margin-bottom: 2px;
}

.activity-desc {
  font-size: 12px;
  color: #aaa;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 11px;
  color: #777;
}

/* Responsive Layout */
@media (max-width: 1200px) {
  .policy-list {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  }
  
  .sidebar {
    width: 25%;
  }
}

@media (max-width: 992px) {
  .sidebar {
    width: 30%;
    min-width: 200px;
  }
}

@media (max-width: 768px) {
  .profile-layout {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    max-height: none;
    overflow: visible;
    padding: 8px 16px;
    min-width: unset;
  }
  
  .main-content {
    padding: 8px 16px;
    min-width: unset;
  }
  
  .policy-list {
    grid-template-columns: 1fr;
  }
  
  .action-list {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .profile-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    height: auto;
    padding: 12px 16px;
  }
  
  .quick-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .action-list {
    grid-template-columns: 1fr;
  }
  
  .insurance-tabs {
    overflow-x: auto;
    padding: 4px;
  }
  
  .tab-btn {
    padding: 8px 12px;
    white-space: nowrap;
  }
}
</style>