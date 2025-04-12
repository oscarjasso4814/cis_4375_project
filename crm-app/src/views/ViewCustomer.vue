<template>
  <div class="view-customer-container">
  <div class="customer-profile-container">
    <!-- Header with customer name and actions -->
    <header class="profile-header">
      <div class="customer-info">
        <h1>{{ customer.name }}</h1>
        <span class="customer-id">ID: {{ customer.id }}</span>
        <span :class="['status-badge', customer.status.toLowerCase()]">{{ customer.status }}</span>
      </div>
      <div class="header-actions">
        <button class="icon-btn" title="Print Profile" @click="printProfile">
          <i class="fas fa-print"></i>
        </button>
        <button class="icon-btn" title="Video Call" @click="startVideoCall">
          <i class="fas fa-video"></i>
        </button>
      </div>
    </header>

    <!-- Main Content Area -->
    <div class="profile-content">
      <!-- Left Column - Customer Info -->
      <div class="left-column">
        <div class="box customer-details">
          <div class="box-header">
            <h2>Contact</h2>
          </div>
          <div class="box-content">
            <div class="info-row">
              <div class="info-label">Name:</div>
              <div class="info-value">{{ customer.name }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">Cell:</div>
              <div class="info-value">{{ customer.cell }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">Phone 2:</div>
              <div class="info-value">{{ customer.phone2 || 'N/A' }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">Email:</div>
              <div class="info-value">{{ customer.email }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">Physical Address:</div>
              <div class="info-value">
                {{ customer.address.street }}<br>
                {{ customer.address.city }}, {{ customer.address.state }} {{ customer.address.zip }}
              </div>
            </div>
            <div class="info-row">
              <div class="info-label">Mailing Address:</div>
              <div class="info-value">{{ customer.mailingAddress || 'Same as physical address' }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">DOB:</div>
              <div class="info-value">{{ customer.dob }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">Gender:</div>
              <div class="info-value">{{ customer.gender }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">Marital Status:</div>
              <div class="info-value">{{ customer.maritalStatus }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">SSN/Tax ID:</div>
              <div class="info-value">{{ customer.ssnTaxId }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">Agent of Record:</div>
              <div class="info-value">{{ customer.agentOfRecord }}</div>
            </div>
            <div class="info-row">
              <div class="info-label">Date Added:</div>
              <div class="info-value">{{ customer.dateAdded }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Center Column - Policies -->
      <div class="center-column">
        <div class="box">
          <div class="box-header">
            <div class="insurance-tabs">
              <button 
                v-for="type in insuranceTypes" 
                :key="type.value"
                :class="['tab-btn', { active: activeInsuranceType === type.value }]" 
                @click="activeInsuranceType = type.value"
              >
                <i :class="type.icon"></i>
                {{ type.label }}
              </button>
            </div>
          </div>
          <div class="box-content">
            <div class="policies-header">
              <h3>{{ activeInsuranceType }} Insurance Policies</h3>
              <button class="primary-btn" @click="addNewPolicy">
                <i class="fas fa-plus"></i> Add Policy
              </button>
            </div>
            
            <!-- Line item view for policies -->
            <div class="policies-list">
              <div v-if="getPolicies(activeInsuranceType).length > 0">
                <table class="policies-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Policy #</th>
                      <th>Coverage</th>
                      <th>Premium</th>
                      <th>Start Date</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="text-color" v-for="policy in getPolicies(activeInsuranceType)" :key="policy.id">
                      <td>{{ policy.name }}</td>
                      <td>{{ policy.number }}</td>
                      <td>{{ policy.coverage }}</td>
                      <td>{{ policy.premium }}</td>
                      <td>{{ policy.startDate }}</td>
                      <td>
                        <div class="dropdown">
                          <button class="dropdown-btn">
                            Action <i class="fas fa-caret-down"></i>
                          </button>
                          <div class="dropdown-content">
                            <a href="#" @click.prevent="rewritePolicy(policy.id)">Re-write</a>
                            <a href="#" @click.prevent="renewPolicy(policy.id)">Re-new</a>
                            <a href="#" @click.prevent="cancelPolicy(policy.id)">Cancel</a>
                          </div>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="no-policies">
                <p>No {{ activeInsuranceType }} policies found for this customer</p>
                <button class="primary-btn" @click="addNewPolicy">
                  <i class="fas fa-plus"></i> Add Policy
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Combined Notes, Attachments and Tasks Section with toggle -->
        <div class="box combined-section">
          <div class="box-header">
            <div class="tab-toggle">
              <button 
                :class="['toggle-btn', { active: activeTab === 'notes' }]" 
                @click="activeTab = 'notes'"
              >
                <i class="fas fa-sticky-note"></i> Notes
              </button>
              <button 
                :class="['toggle-btn', { active: activeTab === 'attachments' }]" 
                @click="activeTab = 'attachments'"
              >
                <i class="fas fa-paperclip"></i> Attachments
              </button>
              <button 
                :class="['toggle-btn', { active: activeTab === 'tasks' }]" 
                @click="activeTab = 'tasks'"
              >
                <i class="fas fa-tasks"></i> Tasks
              </button>
            </div>
            <div>
              <button v-if="activeTab === 'notes'" class="primary-btn" @click="addNote">
                <i class="fas fa-plus"></i> Add Note
              </button>
              <button v-if="activeTab === 'attachments'" class="primary-btn">
                <i class="fas fa-plus"></i> Add Attachment
              </button>
              <button v-if="activeTab === 'tasks'" class="primary-btn" @click="showModal = true">
                <i class="fas fa-plus"></i> Add Task
              </button>
            </div>
          </div>
          <div class="box-content" :style="{ height: contentSectionHeight + 'px' }">
            <!-- Notes Content -->
            <div v-if="activeTab === 'notes'" class="tab-content">
              <p class="placeholder-text">Customer notes will appear here</p>
              <!-- Notes will be implemented later -->
            </div>
            
            <!-- Attachments Content -->
            <div v-if="activeTab === 'attachments'" class="tab-content">
              <p class="placeholder-text">Customer attachments will appear here</p>
              <!-- Attachments will be implemented later -->
            </div>
            
            <!-- Tasks Content -->
            <div v-if="activeTab === 'tasks'" class="tab-content">
              <p class="placeholder-text">Customer tasks will appear here</p>
              <!-- Tasks will be implemented later -->
            </div>
            
            <!-- Resizer handle at the bottom of the box -->
            <div class="resizer" @mousedown="startResize"></div>
          </div>
        </div>
      </div>

      <!-- Right Column - Action Items -->
      <div class="right-column">
        <div class="box action-items">
          <div class="box-header">
            <h2>Action Items</h2>
          </div>
          <div class="box-content">
            <div class="action-buttons">
              <button class="action-btn" @click="addNewPolicy">
                <i class="fas fa-file-medical"></i>
                Add Policy
              </button>
              <button class="action-btn" @click="showModal = true">
                <i class="fas fa-tasks"></i>
                Add Task
              </button>
              <button class="action-btn" @click="addNote">
                <i class="fas fa-sticky-note"></i>
                Add Note
              </button>
              <button class="action-btn" @click="openACORDForms">
                <i class="fas fa-file-alt"></i>
                ACORD Forms
              </button>
              <button class="action-btn" @click="addChangeRequest">
                <i class="fas fa-exchange-alt"></i>
                Change Request
              </button>
              <button class="action-btn" @click="openMailingServices">
                <i class="fas fa-mail-bulk"></i>
                Mailing
              </button>
            </div>
          </div>
        </div>

        <!-- Customs Forms Section -->
        <div class="box custom-forms">
          <div class="box-header">
            <h2>Custom Forms</h2>
          </div>
          <div class="box-content">
            <div class="form-buttons">
              <button class="form-btn">Form 1</button>
              <button class="form-btn">Form 2</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for Add Task -->
    <AddTask
      v-if="showModal"
      :customer-id="customer.CustomerID"
      :customer-name="customer.FirstName + ' ' + customer.LastName"
      :created-by-rep="loggedInRepId"
      :created-by-name="loggedInRepName"
      :representatives="repList"
      @close="showModal = false"
    />
  </div>
</div>
</template>

<script setup>
import AddTask from '@/components/AddTask.vue'
import { ref, reactive, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from "axios";
import { url } from "../api/apiurl";

const route = useRoute();
const showModal = ref(false);
const loggedInRepId = ref(1); // This should be obtained from your user store
const loggedInRepName = ref("Agent Name"); // This should be obtained from your user store
const repList = ref([]); // This should be populated with representatives from your DB

// Insurance type tabs with icons
const insuranceTypes = [
  { label: 'Life', value: 'LIFE', icon: 'fas fa-heartbeat' },
  { label: 'Health', value: 'HEALTH', icon: 'fas fa-medkit' },
  { label: 'Medicare', value: 'MEDICARE', icon: 'fas fa-hospital' },
  { label: 'Home', value: 'HOME', icon: 'fas fa-home' },
  { label: 'Auto', value: 'AUTO', icon: 'fas fa-car' },
  { label: 'Other', value: 'OTHER', icon: 'fas fa-umbrella' }
];

// Customer data structure
const customer = reactive({
  name: '',
  address: {
    street: '',
    city: '',
    state: '',
    zip: ''
  },
  addressVerified: false,
  mailingAddress: '',
  email: '',
  email2: '',
  cell: '',
  phone2: '',
  phone3: '',
  phone4: '',
  language: '',
  preferredContact: '',
  ssnTaxId: '',
  maritalStatus: '',
  gender: '',
  id: '',
  customerType: '',
  accountType: '',
  status: 'Active',
  subStatus: '',
  agentOfRecord: '',
  csr: '',
  keyedBy: '',
  office: '',
  source: '',
  subSource: '',
  dateAdded: '',
  dob: '',
  dl: '',
  dlState: '',
  dateLicensed: '',
  householdSize: '',
  peopleApplying: '',
  householdIncome: '',
  preferences: {
    'Do Not Email': 'No',
    'Do Not Text': 'No',
    'Do Not Call': 'No',
    'Do Not Mail': 'No',
    'Do Not Market': 'No',
    'Do Not Capture Email': 'No'
  },
  relationships: [],
  tags: [],
  // Additional fields to match backend data
  CustomerID: '',
  FirstName: '',
  LastName: ''
});

// Sample policies data
const policies = ref([]);

// Active insurance type tab
const activeInsuranceType = ref('LIFE');

// Fetch policies from backend
async function getPoliciesFromDB(custid) {
  try {
    const response = await axios.get(`${url}/api/customers/${custid}/policies`);
    policies.value = response.data.map(policy => ({
      id: policy.PolicyID,
      type: policy.CategoryName?.toUpperCase() || 'OTHER',
      name: policy.CompanyName || policy.Issuer || 'Unknown',
      number: policy.PolicyNumber,
      coverage: policy.AdditionalInfo || 'N/A',
      premium: 'N/A', // placeholder
      startDate: policy.EffectiveDate || 'N/A'
    }));
  } catch (err) {
    console.error("Error loading policies:", err);
  }
}

// Used by UI to filter by tab type
const getPolicies = (type) => {
  return policies.value.filter(policy => policy.type === type);
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

const addChangeRequest = () => {
  console.log('Opening Add Change Request form...');
  // Implementation would go here
};

const openMailingServices = () => {
  console.log('Opening Mailing Services...');
  // Implementation would go here
};

// New policy action methods
const rewritePolicy = (policyId) => {
  console.log(`Rewriting policy ${policyId}...`);
  // Implementation would go here
};

const renewPolicy = (policyId) => {
  console.log(`Renewing policy ${policyId}...`);
  // Implementation would go here
};

const cancelPolicy = (policyId) => {
  console.log(`Cancelling policy ${policyId}...`);
  // Implementation would go here
};

// Function to fetch and update customer information
async function getCustomer(custid) {
  try {
    const response = await axios.get(`${url}/api/customer/${custid}`);
    const customerData = response.data[0];

    if (customerData) {
      // Update the customer object with fetched data
      customer.CustomerID = customerData.CustomerID || '';
      customer.FirstName = customerData.FirstName || '';
      customer.LastName = customerData.LastName || '';
      customer.name = `${customerData.FirstName} ${customerData.LastName}`.trim() || '';
      customer.address.street = customerData.Address || '';
      customer.address.city = customerData.City || '';
      customer.address.state = customerData.State || '';
      customer.address.zip = customerData.Zip || '';
      customer.mailingAddress = customerData.MailingAddress || '';
      customer.email = customerData.Email1 || '';
      customer.email2 = customerData.Email2 || '';
      customer.cell = customerData.Phone1 || '';
      customer.phone2 = customerData.Phone2 || '';
      customer.phone3 = customerData.Phone3 || '';
      customer.phone4 = customerData.BadPhone4 || '';
      customer.language = customerData.Language || '';
      customer.preferredContact = customerData.PrefferedContact || '';
      customer.ssnTaxId = customerData.SocialSecurityNum || '';
      customer.maritalStatus = customerData.MaritalStatus || '';
      customer.gender = customerData.Gender || '';
      customer.id = customerData.CustomerID || '';
      customer.customerType = customerData.Type || '';
      customer.accountType = customerData.AccountType || '';
      customer.status = customerData.ActiveStatus ? 'Active' : 'Inactive';
      customer.subStatus = customerData.SubsStatus || '';
      customer.agentOfRecord = customerData.AgentRecordID || '';
      customer.csr = customerData.RepresentativeID || '';
      customer.office = customerData.Office || '';
      customer.source = customerData.Source || '';
      customer.subSource = customerData.SubSource || '';
      customer.dateAdded = customerData.DateAdded || '';
      customer.dob = customerData.DateOfBirth || '';
      customer.dl = customerData.DriversLicenseNum || '';
      customer.dlState = customerData.DriversLicenseState || '';
      customer.householdSize = customerData.HouseholdSize || '';
      customer.householdIncome = customerData.HouseholdIncome || '';

      customer.preferences = {
        'Do Not Email': customerData.DoNotEmail ? 'Yes' : 'No',
        'Do Not Text': customerData.DoNotText ? 'Yes' : 'No',
        'Do Not Call': customerData.DoNotCall ? 'Yes' : 'No',
        'Do Not Mail': customerData.UndeliverableMail ? 'Yes' : 'No',
        'Do Not Market': customerData.DoNotMarket ? 'Yes' : 'No',
        'Do Not Capture Email': customerData.DoNotCaptureEmail ? 'Yes' : 'No'
      };
    } else {
      throw new Error("No customer data returned");
    }
  } catch (error) {
    console.error('Error fetching customer data:', error);
  }
}

// Watch for changes in the route parameter and fetch the customer data
watch(
  () => route.params.id,
  async (newId) => {
    if (newId) {
      await getCustomer(newId);
      await getPoliciesFromDB(newId);
    }
  }
);

// Lifecycle hook
onMounted( async () => {
  console.log('Customer profile component mounted');
  
  // Get the customer ID from the route params
  const customerId = route.params.id;
  
  await getCustomer(customerId);
  await getPoliciesFromDB(customerId);

  console.log("Fetched policies:", policies.value);
  
  // If no ID in route, use a default
  if (customerId) {
    getCustomer(customerId);
  } else {
    // Use a default ID for the ex_cust route
    getCustomer(2);
  }
  
  // Fetch representatives for the AddTask component
  // This should be implemented to fetch actual representatives from your database
  repList.value = [
    { RepresentativeID: 1, FirstName: 'Amin', LastName: 'Lalani' },
    { RepresentativeID: 2, FirstName: 'John', LastName: 'Doe' }
  ];
});
</script>

<style scoped>
.view-customer-container {
  height: 100%;
  width: 100%;
}

.text-color{
  color: #333;
}
/* Main Container */
.customer-profile-container {
  max-width: 100%;
  margin: 60px auto 0;
  padding: 0 20px 20px;
  background-color: #f5f5f5;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Header */
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.customer-info h1 {
  font-size: 24px;
  margin: 0 0 5px 0;
  color: #333;
}

.customer-id {
  font-size: 14px;
  color: #666;
  margin-right: 10px;
}

.status-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  background-color: #e0e0e0;
}

.status-badge.active {
  background-color: #4caf50;
  color: white;
}

.status-badge.inactive {
  background-color: #f44336;
  color: white;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.icon-btn {
  width: 36px;
  height: 36px;
  border-radius: 4px;
  background-color: #fff;
  border: 1px solid #ddd;
  color: #007bff;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
}

.icon-btn:hover {
  background-color: #f0f0f0;
}

/* Content Layout */
.profile-content {
  display: flex;
  gap: 20px;
}

.left-column {
  width: 25%;
  min-width: 250px;
}

.center-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.right-column {
  width: 20%;
  min-width: 200px;
}

/* Box Styling */
.box {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  overflow: hidden;
}

.box-header {
  padding: 12px 15px;
  border-bottom: 1px solid #e0e0e0;
  background-color: #f8f9fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.box-header h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.box-content {
  padding: 15px;
}

/* Customer Details */
.info-row {
  display: flex;
  margin-bottom: 8px;
  font-size: 14px;
  line-height: 1.4;
}

.info-label {
  width: 130px;
  font-weight: 600;
  color: #555;
}

.info-value {
  flex: 1;
  color: #333;
}

/* Insurance Tabs */
.insurance-tabs {
  display: flex;
  gap: 5px;
  overflow-x: auto;
  padding-bottom: 5px;
}

.tab-btn {
  padding: 8px 12px;
  background-color: #f0f0f0;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  color: #555;
  cursor: pointer;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 5px;
}

.tab-btn i {
  font-size: 14px;
}

.tab-btn.active {
  background-color: #007bff;
  color: white;
}

/* Policies Section */
.policies-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.policies-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.policies-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.policies-table th,
.policies-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.policies-table th {
  font-weight: 600;
  color: #555;
  background-color: #f5f5f5;
}

.no-policies {
  text-align: center;
  padding: 30px;
  color: #666;
}

/* Dropdown Button */
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-btn {
  background-color: #007bff;
  color: white;
  padding: 6px 12px;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.dropdown-content {
  display: none;
  position: absolute;
  right: 0;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
  border-radius: 4px;
}

.dropdown-content a {
  color: black;
  padding: 8px 12px;
  text-decoration: none;
  display: block;
  font-size: 14px;
}

.dropdown-content a:hover {
  background-color: #f1f1f1;
}

.dropdown:hover .dropdown-content {
  display: block;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.action-btn {
  padding: 10px 15px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s;
  text-align: left;
}

.action-btn i {
  color: #007bff;
  width: 16px;
  text-align: center;
}

.action-btn:hover {
  background-color: #f8f9fa;
  border-color: #c0c0c0;
}

/* Form Buttons */
.form-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-btn {
  padding: 10px 15px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: all 0.2s;
}

.form-btn:hover {
  background-color: #f8f9fa;
  border-color: #c0c0c0;
}

/* Primary Button */
.primary-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: background-color 0.2s;
}

.primary-btn:hover {
  background-color: #0069d9;
}

/* Combined Section Styles */
.combined-section {
  position: relative;
}

.tab-toggle {
  display: flex;
  gap: 5px;
}

.toggle-btn {
  padding: 8px 12px;
  background-color: #f0f0f0;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  color: #555;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}

.toggle-btn.active {
  background-color: #007bff;
  color: white;
}

.tab-content {
  height: 100%;
  overflow-y: auto;
}

/* Resizer styles */
.resizer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 8px;
  background-color: transparent;
  cursor: ns-resize;
  transition: background-color 0.2s;
}

.resizer:hover {
  background-color: rgba(0, 123, 255, 0.1);
}

.resizer:after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 30px;
  height: 4px;
  border-radius: 2px;
  background-color: #ddd;
}

/* Notes and Attachments Placeholder */
.placeholder-text {
  color: #999;
  text-align: center;
  font-style: italic;
  padding: 20px;
}

/* Responsive Designs */
@media (max-width: 1200px) {
  .profile-content {
    flex-wrap: wrap;
  }
  
  .left-column, .right-column {
    width: 100%;
  }
  
  .center-column {
    order: -1;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .header-actions {
    align-self: flex-end;
  }
  
  .insurance-tabs {
    flex-wrap: wrap;
  }
}
</style>