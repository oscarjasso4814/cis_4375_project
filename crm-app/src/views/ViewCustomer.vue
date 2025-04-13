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
            
            <!-- Start of Household Members Section -->
            <div class="info-row household-members-section">
              <div class="info-value">
                <div class="household-subheader">
                  <h3>Household Members</h3>
                  <button class="add-member-btn" @click="isAddingHouseholdMember = !isAddingHouseholdMember">
                    Add Member
                  </button>
                </div>
                
                <!-- Add Household Member Form -->
                <div v-if="isAddingHouseholdMember" class="add-form household-form">
                  <h4>Add Household Member</h4>
                  <div class="form-grid">
                    <input v-model="newHouseholdMember.FirstName" placeholder="First Name" />
                    <input v-model="newHouseholdMember.LastName" placeholder="Last Name" />
                    <input v-model="newHouseholdMember.DateOfBirth" type="date" placeholder="DOB" />
                    <select v-model="newHouseholdMember.Gender">
                      <option disabled value="">Gender</option>
                      <option v-for="g in genderOptions" :key="g" :value="g">{{ g }}</option>
                    </select>
                    <select v-model="newHouseholdMember.MaritalStatus">
                      <option disabled value="">Marital Status</option>
                      <option v-for="m in maritalStatusOptions" :key="m" :value="m">{{ m }}</option>
                    </select>
                    <input v-model="newHouseholdMember.SSN" placeholder="SSN / Tax ID" />
                    <select v-model="newHouseholdMember.Relationship">
                      <option disabled value="">Relationship</option>
                      <option v-for="r in relationshipOptions" :key="r" :value="r">{{ r }}</option>
                    </select>
                  </div>
                  <div class="btn-row">
                    <button class="primary-btn" @click="submitNewHouseholdMember">Save</button>
                    <button class="secondary-btn" @click="isAddingHouseholdMember = false">Cancel</button>
                  </div>
                </div>

                <!-- Edit Household Member Form -->
                <div v-if="isEditingHouseholdMember" class="add-form household-form">
                  <h4>Edit Household Member</h4>
                  <div class="form-grid">
                    <input v-model="editingMember.FirstName" placeholder="First Name" />
                    <input v-model="editingMember.LastName" placeholder="Last Name" />
                    <input v-model="editingMember.DateOfBirth" type="date" placeholder="DOB" />
                    <select v-model="editingMember.Gender">
                      <option disabled value="">Gender</option>
                      <option v-for="g in genderOptions" :key="g" :value="g">{{ g }}</option>
                    </select>
                    <select v-model="editingMember.MaritalStatus">
                      <option disabled value="">Marital Status</option>
                      <option v-for="m in maritalStatusOptions" :key="m" :value="m">{{ m }}</option>
                    </select>
                    <input v-model="editingMember.SSN" placeholder="SSN / Tax ID" />
                    <select v-model="editingMember.Relationship">
                      <option disabled value="">Relationship</option>
                      <option v-for="r in relationshipOptions" :key="r" :value="r">{{ r }}</option>
                    </select>
                  </div>
                  <div class="btn-row">
                    <button class="primary-btn" @click="submitEditHouseholdMember">Save Changes</button>
                    <button class="secondary-btn" @click="isEditingHouseholdMember = false">Cancel</button>
                  </div>
                </div>
                
                <!-- Household Members List -->
                <div v-if="householdMembers.length === 0" class="empty-text">No household members found.</div>
                
                <div class="members-list">
                  <div v-for="member in householdMembers" :key="member.HouseholdMemberID" class="member-card">
                    <div class="member-card-header" @click="expandedMemberRows[member.HouseholdMemberID] = !expandedMemberRows[member.HouseholdMemberID]">
                      {{ member.FirstName }} {{ member.LastName }} - Age: {{ calculateAge(member.DateOfBirth) }}
                      <span class="arrow-icon">
                        <i :class="expandedMemberRows[member.HouseholdMemberID] ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
                      </span>
                    </div>
                    
                    <div v-if="expandedMemberRows[member.HouseholdMemberID]" class="member-card-details">
                      <div class="member-details-grid">
                        <div class="member-detail-item">
                          <span class="detail-label">DOB:</span> <span class="detail-value">{{ formatDate(member.DateOfBirth) }}</span>
                        </div>
                        <div class="member-detail-item">
                          <span class="detail-label">Gender:</span> <span class="detail-value">{{ member.Gender }}</span>
                        </div>
                        <div class="member-detail-item">
                          <span class="detail-label">Marital Status:</span> <span class="detail-value">{{ member.MaritalStatus }}</span>
                        </div>
                        <div class="member-detail-item">
                          <span class="detail-label">SSN:</span> <span class="detail-value">{{ member.SSN }}</span>
                        </div>
                        <div class="member-detail-item">
                          <span class="detail-label">Relationship:</span> <span class="detail-value">{{ member.Relationship }}</span>
                        </div>
                      </div>
                      <div class="member-actions">
                        <button class="edit-btn" @click="editHouseholdMember(member)">
                          <i class="fas fa-edit"></i> Edit
                        </button>
                        <button class="danger-btn" @click="deactivateHouseholdMember(member.HouseholdMemberID)">
                          <i class="fas fa-trash"></i> Delete
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- End of Household Members Section -->
            
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
              
            </div>
            
            <!-- Line item view for policies -->
            <div class="policies-list">
              <div v-if="getPolicies(activeInsuranceType).length > 0">
                <table class="policies-table">
                  <thead>
                    <tr>
                      <th>Status</th>
                      <th>Company</th>
                      <th>Category</th>
                      <th>Policy #</th>
                      <th>Coverage</th>
                      <th>Premium</th>
                      <th>Start Date</th>
                      <th>End Date</th>
                      <th>Agent</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="text-color" v-for="policy in getPolicies(activeInsuranceType)" :key="policy.id" :class="{'canceled': policy.status === 'Canceled', 'renewed': policy.status === 'Renewed', 'rewritten': policy.status === 'Rewritten'}">
                      <td>
                        <span class="status-pill" :class="getStatusClass(policy.status)">
                          {{ policy.status || 'Active' }}
                        </span>
                      </td>
                      <td>{{ policy.companyName }}</td>
                      <td>{{ policy.categoryName }}</td>
                      <td>{{ policy.number }}</td>
                      <td>{{ policy.coverage }}</td>
                      <td>${{ parseFloat(policy.premium).toFixed(2) }}</td>
                      <td>{{ formatDate(policy.startDate) }}</td>
                      <td>{{ formatDate(policy.endDate) }}</td>
                      <td>{{ policy.agentName }}</td>
                      <td>
                        <div class="dropdown" v-if="canModifyPolicy(policy)">
                          <button class="dropdown-btn">
                            Action <i class="fas fa-caret-down"></i>
                          </button>
                          <div class="dropdown-content">
                            <a href="#" @click.prevent="rewritePolicy(policy)">Re-write</a>
                            <a href="#" @click.prevent="renewPolicy(policy)">Re-new</a>
                            <a href="#" @click.prevent="cancelPolicy(policy)">Cancel</a>
                          </div>
                        </div>
                        <span v-else class="disabled-actions">{{ getStatusMessage(policy.status) }}</span>
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
  <!-- Modal for Add Policy -->
    <AddPolicyModal
      v-if="showPolicyModal"
      :customer-id="customer.id"
      :customer-name="customer.name"
      @close="showPolicyModal = false"
      @policy-added="handlePolicyAdded"
    />
    
    <!-- Modal for Edit/Rewrite/Renew/Cancel Policy -->
    <EditPolicyModal
      v-if="showEditPolicyModal"
      :show="showEditPolicyModal"
      :policy="selectedPolicy"
      :customer-name="customer.name"
      :customer-id="customer.id"
      :mode="policyEditMode"
      @close="showEditPolicyModal = false"
      @policy-updated="handlePolicyUpdated"
    />
</div>

</template>

<script setup>
import AddTask from '@/components/AddTask.vue'
import { ref, reactive, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from "axios";
import { url } from "../api/apiurl";
import AddPolicyModal from '../components/AddPolicy.vue';
import EditPolicyModal from '../components/EditPolicy.vue';


function formatDate(dateString) {
  if (!dateString) return '';
  
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return 'Invalid Date';
    
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const year = date.getFullYear();
    
    return `${month}/${day}/${year}`;
  } catch (error) {
    console.error('Error formatting date:', error);
    return dateString; // Return original if parsing fails
  }
}

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

// Household members variables
const householdMembers = ref([]);
const expandedMemberRows = ref({});
const isAddingHouseholdMember = ref(false);

const genderOptions = ['Male', 'Female', 'Other'];
const maritalStatusOptions = ['Single', 'Married', 'Divorced', 'Widowed'];
const relationshipOptions = ['Spouse', 'Child', 'Parent', 'Sibling', 'Other'];

const newHouseholdMember = ref({
  FirstName: '',
  LastName: '',
  DateOfBirth: '',
  Gender: '',
  MaritalStatus: '',
  SSN: '',
  Relationship: ''
});

// Active tab
const activeTab = ref('notes');
const contentSectionHeight = ref(300); // Default height

// Updated function to fetch policies from the backend
async function getPoliciesFromDB(custid) {
  try {
    const response = await axios.get(`${url}/api/customers/${custid}/policies`);
    policies.value = response.data.map(policy => ({
      id: policy.PolicyID,
      type: policy.CategoryName?.toUpperCase() || 'OTHER',
      name: policy.CompanyName || policy.Issuer || 'Unknown',
      number: policy.PolicyNumber,
      coverage: policy.AdditionalInfo || 'N/A',
      premium: policy.Premium,
      startDate: policy.EffectiveDate || 'N/A',
      endDate: policy.ExpirationDate || 'N/A',
      status: policy.PolicyStatus || 'Active', // Ensure policy status is correctly set
      cancelReason: policy.CancelReason || null,
      cancelDate: policy.CancelDate || null,
      // Additional fields needed for edit modal
      categoryId: policy.CategoryID,
      subcategoryId: policy.SubcategoryID,
      companyId: policy.CompanyID,
      issuer: policy.Issuer,
      agentRecordId: policy.AgentRecordID,
      representativeId: policy.RepresentativeID,
      // Include the new fields for display
      categoryName: policy.CategoryName || 'N/A',
      companyName: policy.CompanyName || 'N/A',
      agentName: policy.AgentName || 'N/A',
      representativeName: policy.RepresentativeName || 'N/A'
    }));
    
    console.log("Fetched policies:", policies.value);
  } catch (err) {
    console.error("Error loading policies:", err);
  }
}


// Household member functions
function calculateAge(dob) {
  if (!dob) return '';
  const birth = new Date(dob);
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--;
  return age;
}

async function fetchHouseholdMembers() {
  try {
    const res = await axios.get(`/api/customer/${customer.id}/household-members`);
    householdMembers.value = res.data;
  } catch (error) {
    console.error('Error fetching household members:', error);
  }
}

async function submitNewHouseholdMember() {
  try {
    await axios.post(`/api/customer/${customer.id}/household-members`, newHouseholdMember.value);
    isAddingHouseholdMember.value = false;
    resetHouseholdMemberForm();
    await fetchHouseholdMembers();
  } catch (error) {
    console.error('Error adding household member:', error);
  }
}

function resetHouseholdMemberForm() {
  newHouseholdMember.value = {
    FirstName: '',
    LastName: '',
    DateOfBirth: '',
    Gender: '',
    MaritalStatus: '',
    SSN: '',
    Relationship: ''
  };
}

async function deactivateHouseholdMember(memberId) {
  try {
    await axios.delete(`/api/household-members/${memberId}`);
    await fetchHouseholdMembers();
  } catch (error) {
    console.error('Error deactivating household member:', error);
  }
}

// Used by UI to filter by tab type and sort by expiration date
const getPolicies = (type) => {
  return policies.value
    .filter(policy => policy.type === type)
    .sort((a, b) => {
      // Sort by expiration date in descending order (most recent first)
      const dateA = a.endDate ? new Date(a.endDate) : new Date(0);
      const dateB = b.endDate ? new Date(b.endDate) : new Date(0);
      return dateB - dateA;
    });
};

// Check if a policy can be modified (can't modify already canceled/renewed/rewritten policies)
function canModifyPolicy(policy) {
  // Only allow actions on 'Active' policies
  return policy.status === 'Active' || policy.status === null || policy.status === undefined;
}

// Get status message for policies that can't be modified
function getStatusMessage(status) {
  if (status === 'Canceled') return 'Policy Canceled';
  if (status === 'Renewed') return 'Policy Renewed';
  if (status === 'Rewritten') return 'Policy Rewritten';
  return '';
}

// Get CSS class for policy status
function getStatusClass(status) {
  if (!status || status === 'Active') return 'status-active';
  if (status === 'Canceled') return 'status-canceled';
  if (status === 'Renewed') return 'status-renewed';
  if (status === 'Rewritten') return 'status-rewritten';
  return '';
}

// Rewrite policy
const rewritePolicy = (policy) => {
  selectedPolicy.value = policy;
  policyEditMode.value = 'rewrite';
  showEditPolicyModal.value = true;
};

// Renew policy
const renewPolicy = (policy) => {
  selectedPolicy.value = policy;
  policyEditMode.value = 'renew';
  showEditPolicyModal.value = true;
};

// Cancel policy
const cancelPolicy = (policy) => {
  selectedPolicy.value = policy;
  policyEditMode.value = 'cancel';
  showEditPolicyModal.value = true;
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


// Resize functionality for the combined section
const startResize = (e) => {
  e.preventDefault();
  document.addEventListener('mousemove', resize);
  document.addEventListener('mouseup', stopResize);
};

const resize = (e) => {
  const container = e.target.parentElement;
  const newHeight = e.clientY - container.getBoundingClientRect().top;
  if (newHeight > 100) { // Minimum height
    contentSectionHeight.value = newHeight;
  }
};

const stopResize = () => {
  document.removeEventListener('mousemove', resize);
  document.removeEventListener('mouseup', stopResize);
};

// Handle policy update (refresh policies list)
const handlePolicyUpdated = async (policyData) => {
  console.log("Policy updated successfully:", policyData);
  // Show a success message to the user based on the operation
  let message = '';
  if (policyEditMode.value === 'rewrite') {
    message = `Policy rewritten successfully! Policy ID: ${policyData.PolicyID}`;
  } else if (policyEditMode.value === 'renew') {
    message = `Policy renewed successfully! Policy ID: ${policyData.PolicyID}`;
  } else if (policyEditMode.value === 'cancel') {
    message = `Policy canceled successfully!`;
  } else {
    message = `Policy updated successfully! Policy ID: ${policyData.PolicyID}`;
  }
  
  alert(message);
  
  // Refresh policies list
  await getPoliciesFromDB(customer.id);
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

const isEditingHouseholdMember = ref(false);
const editingMember = ref({});

function editHouseholdMember(member) {
  // Create a deep copy of the member object
  editingMember.value = JSON.parse(JSON.stringify(member));
  
  // Format the date for the input field (YYYY-MM-DD format required by date inputs)
  if (editingMember.value.DateOfBirth) {
    const date = new Date(editingMember.value.DateOfBirth);
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const year = date.getFullYear();
    editingMember.value.DateOfBirth = `${year}-${month}-${day}`;
  }
  
  isEditingHouseholdMember.value = true;
}

async function submitEditHouseholdMember() {
  try {
    await axios.put(`/api/household-members/${editingMember.value.HouseholdMemberID}`, editingMember.value);
    isEditingHouseholdMember.value = false;
    await fetchHouseholdMembers();
  } catch (error) {
    console.error('Error updating household member:', error);
  }
}

// Watch for changes in the route parameter and fetch the customer data
watch(
  () => route.params.id,
  async (newId) => {
    if (newId) {
      await getCustomer(newId);
      await getPoliciesFromDB(newId);
      await fetchHouseholdMembers();
    }
  }
);

const showPolicyModal = ref(false);

const addNewPolicy = () => {
  console.log("Opening policy modal for customer ID:", customer.id);
  showPolicyModal.value = true;
};


// Function to handle policy added event
const handlePolicyAdded = async (policyData) => {
  console.log("Policy added successfully:", policyData);
  // Show a success message to the user
  alert(`Policy added successfully! Policy ID: ${policyData.PolicyID}`);
  // Refresh policies list
  await getPoliciesFromDB(customer.id);
};

const showEditPolicyModal = ref(false);
const selectedPolicy = ref(null);
const policyEditMode = ref('rewrite'); // 'rewrite', 'renew', or 'cancel'

// Lifecycle hook
onMounted( async () => {
  console.log('Customer profile component mounted');
  
  // Get the customer ID from the route params
  const customerId = route.params.id;
  
  if (customerId) {
    await getCustomer(customerId);
    await getPoliciesFromDB(customerId);
    await fetchHouseholdMembers();
  } else {
    // Use a default ID for the ex_cust route
    await getCustomer(2);
    await getPoliciesFromDB(2);
    await fetchHouseholdMembers();
  }
  
  // Fetch representatives for the AddTask component
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

/* Household Members Styles */
.household-members-section {
  margin-top: 25px;
  margin-bottom: 25px;
  flex-direction: column;
  align-items: flex-start;
}

.household-members-section .info-label {
  width: 100%;
  margin-bottom: 5px;
  font-size: 16px;
  color: #444;
}

.household-members-section .info-value {
  width: 100%;
}

.household-subheader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  border-bottom: 1px solid #e5e5e5;
  padding-bottom: 8px;
}

.household-subheader h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #444;
}

.add-member-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 6px 15px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-member-btn:hover {
  background-color: #0069d9;
}

.add-form {
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.household-form h4 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 15px;
  color: #333;
  font-weight: 600;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
  margin-bottom: 15px;
}

.form-grid input,
.form-grid select {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-grid input:focus,
.form-grid select:focus {
  outline: none;
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
}

.btn-row {
  display: flex;
  gap: 10px;
  justify-content: flex-start;
}

.secondary-btn {
  background-color: #f8f9fa;
  border: 1px solid #ccc;
  color: #333;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.secondary-btn:hover {
  background-color: #e9ecef;
}

.danger-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: background-color 0.2s;
}

.edit-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  margin-right: 10px;
  transition: background-color 0.2s;
}

.edit-btn:hover {
  background-color: #0069d9;
}

.member-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #eee;
}

.danger-btn:hover {
  background-color: #d32f2f;
}

.empty-text {
  color: #777;
  font-style: italic;
  padding: 10px 0;
  font-size: 14px;
  text-align: center;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.member-card {
  border: 1px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: box-shadow 0.2s;
}

.member-card:hover {
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.member-card-header {
  background-color: #f8f9fa;
  padding: 10px 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  font-weight: 500;
  color: #333;
  transition: background-color 0.2s;
}

.member-card-header:hover {
  background-color: #eff2f7;
}

.arrow-icon {
  display: flex;
  align-items: center;
  color: #777;
  font-size: 14px;
}

.member-card-details {
  padding: 15px;
  background-color: #fff;
  border-top: 1px solid #eee;
}

.member-details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
  margin-bottom: 15px;
}

.member-detail-item {
  display: flex;
  flex-direction: row;
  margin-bottom: 8px;
  align-items: center;
}

.detail-label {
  font-weight: 600;
  color: #555;
  font-size: 13px;
  margin-right: 5px;
}

.detail-value {
  color: #333;
  font-size: 14px;
}

.member-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #eee;
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
  max-height: 60vh;
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
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;

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
  color: #007bff;
  border-color: #007bff;
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

  .center-column .box-content {
  height: 70vh; /* 70% of the viewport height */
  overflow-y: auto; /* Add scroll if content overflows */
}
}

.center-column .box-content {
  height: 40vh; /* 70% of the viewport height */
  overflow-y: auto; /* Add scroll if content overflows */
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

/* Policy Status Styles */
.status-pill {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
  min-width: 80px;
}

.status-active {
  background-color: #28a745;
  color: white;
}

.status-canceled {
  background-color: #dc3545;
  color: white;
}

.status-renewed {
  background-color: #17a2b8;
  color: white;
}

.status-rewritten {
  background-color: #fd7e14;
  color: white;
}

tr.canceled {
  background-color: #ffe6e6 !important;
}

tr.renewed {
  background-color: #e6f7ff !important;
}

tr.rewritten {
  background-color: #fff3e6 !important;
}

.disabled-actions {
  color: #6c757d;
  font-style: italic;
  font-size: 13px;
}



</style>