<template>
    <div class="modal-overlay" v-if="show" @click.self="$emit('close')">
      <div class="modal-content">
        <h3>{{ modalTitle }}</h3>
    
        <div class="customer-info">
          <p><strong>Customer:</strong> {{ customerName }}</p>
          <p><strong>Policy Number:</strong> {{ policy.policyNumber }}</p>
        </div>
    
        <!-- Loading indicator -->
        <div v-if="isLoading" class="loading-container">
          <div class="spinner"></div>
          <p>Loading data...</p>
        </div>
    
        <form v-else @submit.prevent="submitPolicy">
          <!-- Policy Category -->
          <div class="form-group">
            <label>Policy Category:</label>
            <select v-model="updatedPolicy.categoryId" required @change="loadSubcategories">
              <option disabled value="">-- Select Category --</option>
              <option v-for="category in categories" :key="category.CategoryID" :value="category.CategoryID">
                {{ category.CategoryName }}
              </option>
            </select>
          </div>
    
          <!-- Policy Subcategory -->
          <div class="form-group">
            <label>Policy Subcategory:</label>
            <select v-model="updatedPolicy.subcategoryId" :disabled="!updatedPolicy.categoryId">
              <option disabled value="">-- Select Subcategory --</option>
              <option v-for="subcategory in subcategories" :key="subcategory.SubcategoryID" :value="subcategory.SubcategoryID">
                {{ subcategory.SubcategoryName }}
              </option>
            </select>
          </div>
    
          <!-- Insurance Company -->
          <div class="form-group">
            <label>Insurance Company:</label>
            <select v-model="updatedPolicy.companyId" required>
              <option disabled value="">-- Select Company --</option>
              <option v-for="company in companies" :key="company.CompanyID" :value="company.CompanyID">
                {{ company.CompanyName }}
              </option>
            </select>
          </div>
    
          <!-- Policy Number -->
          <div class="form-group">
            <label>Policy Number:</label>
            <input v-model="updatedPolicy.policyNumber" required placeholder="Enter policy number" />
          </div>
    
          <!-- Issuer (if different from company) -->
          <div class="form-group">
            <label>Issuer/Underwriter (if different):</label>
            <input v-model="updatedPolicy.issuer" placeholder="Enter issuer if different from company" />
          </div>
    
          <!-- Effective Date -->
          <div class="form-group">
            <label>Effective Date:</label>
            <input type="date" v-model="updatedPolicy.effectiveDate" required :readonly="mode === 'renew'" />
          </div>
    
          <!-- Expiration Date -->
          <div class="form-group">
            <label>Expiration Date:</label>
            <input type="date" v-model="updatedPolicy.expirationDate" />
          </div>
          
          <!-- Premium Amount -->
          <div class="form-group">
            <label>Premium Amount:</label>
            <input 
              type="number" 
              v-model="updatedPolicy.premium" 
              placeholder="Enter premium amount" 
              step="0.01" 
              min="0"
            />
            <small v-if="premiumHelpText" class="helper-text">{{premiumHelpText}}</small>
          </div>
          
          <!-- Status Field -->
          <div class="form-group" v-if="mode === 'cancel'">
            <label>Cancel Reason:</label>
            <textarea 
              v-model="updatedPolicy.cancelReason" 
              placeholder="Enter reason for cancellation" 
              rows="3"
              required
            ></textarea>
          </div>
    
          <!-- Agent of Record -->
          <div class="form-group">
            <label>Agent of Record:</label>
            <select v-model="updatedPolicy.agentRecordId">
              <option disabled value="">-- Select Agent --</option>
              <option v-for="agent in agents" :key="agent.AgentRecordID" :value="agent.AgentRecordID">
                {{ agent.FullName }}
              </option>
            </select>
          </div>
    
          <!-- Representative -->
          <div class="form-group">
            <label>Representative:</label>
            <select v-model="updatedPolicy.representativeId">
              <option disabled value="">-- Select Representative --</option>
              <option v-for="rep in representatives" :key="rep.RepresentativeID" :value="rep.RepresentativeID">
                {{ rep.FirstName }} {{ rep.LastName }}
              </option>
            </select>
          </div>
    
          <!-- Additional Info -->
          <div class="form-group">
            <label>Additional Information:</label>
            <textarea v-model="updatedPolicy.additionalInfo" rows="3" placeholder="Enter additional information about this policy"></textarea>
          </div>
    
          <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>
    
          <div class="actions">
            <button type="submit" class="btn-primary">{{ submitButtonText }}</button>
            <button type="button" class="btn-secondary" @click="$emit('close')">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted, computed, watch } from 'vue';
  import axios from 'axios';
  import { url } from "../api/apiurl";
  
  const props = defineProps({
    show: {
      type: Boolean,
      required: true
    },
    policy: {
      type: Object,
      required: true
    },
    customerName: {
      type: String,
      required: true
    },
    customerId: {
      type: Number,
      required: true
    },
    mode: {
      type: String,
      required: true,
      validator: (value) => ['rewrite', 'renew', 'cancel'].includes(value)
    }
  });
  
  const emit = defineEmits(['close', 'policy-updated']);
  
  // State management
  const isLoading = ref(true);
  const errorMessage = ref('');
  const premiumHelpText = ref('');
  
  // Data lists
  const categories = ref([]);
  const subcategories = ref([]);
  const companies = ref([]);
  const agents = ref([]);
  const representatives = ref([]);
  
  // Updated policy data
  const updatedPolicy = reactive({
    id: props.policy?.id || null,
    categoryId: '',
    subcategoryId: '',
    companyId: '',
    policyNumber: '',
    issuer: '',
    effectiveDate: '',
    expirationDate: '',
    premium: '',
    agentRecordId: '',
    representativeId: '',
    additionalInfo: '',
    cancelReason: '',
    status: 'Active'
  });
  
  // Computed properties
  const modalTitle = computed(() => {
    if (props.mode === 'rewrite') return 'Rewrite Policy';
    if (props.mode === 'renew') return 'Renew Policy';
    if (props.mode === 'cancel') return 'Cancel Policy';
    return 'Edit Policy';
  });
  
  const submitButtonText = computed(() => {
    if (props.mode === 'rewrite') return 'Rewrite Policy';
    if (props.mode === 'renew') return 'Renew Policy';
    if (props.mode === 'cancel') return 'Cancel Policy';
    return 'Save Changes';
  });
  
  // Watch for policy changes
  watch(() => props.policy, (newPolicy) => {
    if (newPolicy) {
      populateForm(newPolicy);
    }
  }, { immediate: true });
  
  // Fill form with existing policy data
  function populateForm(policy) {
    if (!policy) return;
    
    updatedPolicy.id = policy.id;
    updatedPolicy.categoryId = policy.categoryId || '';
    updatedPolicy.subcategoryId = policy.subcategoryId || '';
    updatedPolicy.companyId = policy.companyId || '';
    updatedPolicy.policyNumber = policy.number || '';
    updatedPolicy.issuer = policy.issuer || '';
    updatedPolicy.effectiveDate = policy.startDate || '';
    updatedPolicy.expirationDate = policy.endDate || '';
    updatedPolicy.premium = policy.premium || '';
    updatedPolicy.agentRecordId = policy.agentRecordId || '';
    updatedPolicy.representativeId = policy.representativeId || '';
    updatedPolicy.additionalInfo = policy.coverage || '';
    
    // If we're renewing, set the effective date to the first day of next month
    if (props.mode === 'renew') {
      const today = new Date();
      const nextMonth = new Date(today.getFullYear(), today.getMonth() + 1, 1);
      const year = nextMonth.getFullYear();
      const month = String(nextMonth.getMonth() + 1).padStart(2, '0');
      const day = String(nextMonth.getDate()).padStart(2, '0');
      updatedPolicy.effectiveDate = `${year}-${month}-${day}`;
      updatedPolicy.expirationDate = ''; // Clear the expiration date for renewal
      updatedPolicy.policyNumber = `${policy.number}-R`; // Append -R to indicate renewal
    }
    
    // Update status based on mode
    if (props.mode === 'rewrite') {
      updatedPolicy.status = 'Rewritten';
    } else if (props.mode === 'renew') {
      updatedPolicy.status = 'Renewed';
    } else if (props.mode === 'cancel') {
      updatedPolicy.status = 'Canceled';
    }
  
    // Load subcategories for the selected category if available
    if (updatedPolicy.categoryId) {
      loadSubcategories();
    }
  }
  
  // Load initial data
  async function loadData() {
    isLoading.value = true;
    errorMessage.value = '';
    
    try {
      // Try to fetch categories
      try {
        axios.get(`${url}/api/categories`).then((response) => {
          categories.value = response.data;
        })
      } catch (error) {
        console.error("Error loading categories:", error);
        categories.value = [
          { CategoryID: 1, CategoryName: "Auto" },
          { CategoryID: 2, CategoryName: "Home" },
          { CategoryID: 3, CategoryName: "Life" },
          { CategoryID: 4, CategoryName: "Health" }
        ];
      }
      
      setTimeout(() => {
        // Try to fetch companies
        try {
          axios.get(`${url}/api/companies`).then((response) => {
            companies.value = response.data;
          })
        } catch (error) {
          console.error("Error loading companies:", error);
          companies.value = [
            { CompanyID: 1, CompanyName: "State Farm" },
            { CompanyID: 2, CompanyName: "Allstate" },
            { CompanyID: 3, CompanyName: "Progressive" }
          ];
        }
      }, 1000)

      setTimeout(() => {
        // Try to fetch agents
        try {
          axios.get(`${url}/api/agents`).then((response) => {
            agents.value = response.data;
          })
        } catch (error) {
          console.error("Error loading agents:", error);
          agents.value = [
            { AgentRecordID: 1, FullName: "John Agent" },
            { AgentRecordID: 2, FullName: "Mary Agent" }
          ];
        }
      }, 2000)
      
      setTimeout(() => {
        // Try to fetch representatives
        try {
          await axios.get(`${url}/api/Representative`).then((response) => {
            representatives.value = response.data;
          })
        } catch (error) {
          console.error("Error loading representatives:", error);
          representatives.value = [
            { RepresentativeID: 1, FirstName: "John", LastName: "Doe" },
            { RepresentativeID: 2, FirstName: "Jane", LastName: "Smith" }
          ];
        }
        
        // Set current user as representative if available
        const currentRepId = localStorage.getItem('reps_id');
        if (currentRepId) {
          updatedPolicy.representativeId = parseInt(currentRepId);
        }
      }, 3000)
      
    } catch (error) {
      console.error('Error loading form data:', error);
      errorMessage.value = 'Failed to load form data completely. Some options may be unavailable.';
    } finally {
      isLoading.value = false;
    }
  }
  
  // Load subcategories when category changes
  async function loadSubcategories() {
  if (!updatedPolicy.categoryId) return;
  
  try {
    console.log(`Loading subcategories for category ID: ${updatedPolicy.categoryId}`);
    
    await axios.get(`${url}/api/categories/${updatedPolicy.categoryId}/subcategories`).then((response) => {
      // Check if the response has data and it's an array
      if (response.data && Array.isArray(response.data)) {
        subcategories.value = response.data;
        console.log("Subcategories loaded:", subcategories.value);
      } else {
        console.warn("Received empty or invalid subcategories data");
        subcategories.value = [];
      }
    })
  } catch (error) {
    console.error('Error loading subcategories:', error);
    
    // Set default subcategories based on selected category
    if (updatedPolicy.categoryId === 1) { // Auto
      subcategories.value = [
        { SubcategoryID: 1, SubcategoryName: "Auto Liability" },
        { SubcategoryID: 2, SubcategoryName: "Comprehensive" },
        { SubcategoryID: 3, SubcategoryName: "Collision" }
      ];
    } else if (updatedPolicy.categoryId === 2) { // Home
      subcategories.value = [
        { SubcategoryID: 4, SubcategoryName: "Homeowners" },
        { SubcategoryID: 5, SubcategoryName: "Flood" },
        { SubcategoryID: 6, SubcategoryName: "Earthquake" }
      ];
    } else {
      subcategories.value = [
        { SubcategoryID: 7, SubcategoryName: "Basic" },
        { SubcategoryID: 8, SubcategoryName: "Premium" }
      ];
    }
  }
}
  
  // Validate form before submission
  function validateForm() {
    // Reset error message
    errorMessage.value = '';
    
    // Basic validation
    if (!updatedPolicy.categoryId) {
      errorMessage.value = 'Please select a policy category';
      return false;
    }
    
    if (!updatedPolicy.companyId) {
      errorMessage.value = 'Please select an insurance company';
      return false;
    }
    
    if (!updatedPolicy.policyNumber) {
      errorMessage.value = 'Please enter a policy number';
      return false;
    }
    
    if (!updatedPolicy.effectiveDate) {
      errorMessage.value = 'Please enter an effective date';
      return false;
    }
    
    // Premium validation - check if it has more than 2 decimal places
    if (updatedPolicy.premium) {
      const premiumStr = updatedPolicy.premium.toString();
      const decimalParts = premiumStr.split('.');
      
      if (decimalParts.length > 1 && decimalParts[1].length > 2) {
        errorMessage.value = 'Premium must be a whole number or have up to 2 decimal places (e.g., 90 or 90.90)';
        return false;
      }
    }
    
    // Validate expiration date is after effective date
    if (updatedPolicy.effectiveDate && updatedPolicy.expirationDate) {
      const effectiveDate = new Date(updatedPolicy.effectiveDate);
      const expirationDate = new Date(updatedPolicy.expirationDate);
      
      if (expirationDate < effectiveDate) {
        errorMessage.value = 'Expiration date must be after effective date';
        return false;
      }
    }
    
    // Cancel reason validation
    if (props.mode === 'cancel' && !updatedPolicy.cancelReason) {
      errorMessage.value = 'Please provide a reason for cancellation';
      return false;
    }
    
    return true;
  }
  
  // Submit the policy
async function submitPolicy() {
  if (!validateForm()) return;
  
  try {
    isLoading.value = true;
    errorMessage.value = '';
    
    // Prepare data for API
    const policyData = {
      PolicyID: props.policy.id,
      CustomerID: props.customerId,
      CategoryID: updatedPolicy.categoryId,
      SubcategoryID: updatedPolicy.subcategoryId || null,
      CompanyID: updatedPolicy.companyId,
      PolicyNumber: updatedPolicy.policyNumber,
      Issuer: updatedPolicy.issuer || null,
      EffectiveDate: updatedPolicy.effectiveDate,
      ExpirationDate: updatedPolicy.expirationDate || null,
      Premium: updatedPolicy.premium || 0,
      AgentRecordID: updatedPolicy.agentRecordId || null,
      RepresentativeID: updatedPolicy.representativeId || null,
      AdditionalInfo: updatedPolicy.additionalInfo || null,
      PolicyStatus: updatedPolicy.status
    };
    
    // Add cancel reason for canceled policies
    if (props.mode === 'cancel') {
      policyData.CancelReason = updatedPolicy.cancelReason;
      policyData.CancelDate = new Date().toISOString().split('T')[0]; // Today's date
    }
    
    console.log("Submitting policy data:", policyData);
    
    let apiUrl;
    if (props.mode === 'rewrite') {
      apiUrl = `${url}/api/policy/${props.policy.id}/rewrite`;
    } else if (props.mode === 'renew') {
      apiUrl = `${url}/api/policy/${props.policy.id}/renew`;
    } else if (props.mode === 'cancel') {
      apiUrl = `${url}/api/policy/${props.policy.id}/cancel`;
    } else {
      apiUrl = `${url}/api/policy/${props.policy.id}`;
    }
    
    await axios.post(apiUrl, policyData).then((response) => {
      console.log("Policy updated successfully:", response.data);
    
    // Emit event to refresh policy list
    emit('policy-updated', response.data);
    
    // Close modal
    emit('close');
    })
  } catch (error) {
    console.error(`Error ${props.mode === 'edit' ? 'updating' : props.mode + 'ing'} policy:`, error);
    
    // More detailed error handling
    if (error.response) {
      errorMessage.value = `Server error: ${error.response.status} - ${error.response.data.message || error.response.statusText}`;
    } else if (error.request) {
      errorMessage.value = 'Network error. Please check your connection and try again.';
    } else {
      errorMessage.value = `Error: ${error.message}`;
    }
    
  } finally {
    isLoading.value = false;
  }
}
  
  // Initialize component
  onMounted(() => {
    loadData();
  });
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background: white;
    padding: 30px;
    border-radius: 12px;
    width: 600px;
    max-width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }
  
  h3 {
    font-size: 20px;
    margin-top: 0;
    margin-bottom: 20px;
    color: #333;
    text-align: center;
  }
  
  .customer-info {
    background-color: #f8f9fa;
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 20px;
    border: 1px solid #eee;
  }
  
  .form-group {
    margin-bottom: 16px;
  }
  
  label {
    display: block;
    margin-bottom: 6px;
    font-weight: 600;
    color: #333;
  }
  
  input, select, textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 14px;
  }
  
  select {
    background-color: white;
  }
  
  textarea {
    resize: vertical;
  }
  
  .error-message {
    color: #dc3545;
    margin-bottom: 15px;
    font-size: 14px;
  }
  
  .helper-text {
    color: #6c757d;
    font-size: 12px;
    margin-top: 4px;
  }
  
  .actions {
    display: flex;
    justify-content: space-between;
    margin-top: 25px;
  }
  
  .btn-primary {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 15px;
    transition: background-color 0.2s;
  }
  
  .btn-primary:hover {
    background-color: #0069d9;
  }
  
  .btn-secondary {
    background-color: #6c757d;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 15px;
    transition: background-color 0.2s;
  }
  
  .btn-secondary:hover {
    background-color: #5a6268;
  }
  
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 0;
  }
  
  .spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border-left-color: #007bff;
    animation: spin 1s linear infinite;
    margin-bottom: 15px;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: #80bdff;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  }
  
  select:disabled {
    background-color: #e9ecef;
    cursor: not-allowed;
  }
  
  input:read-only {
    background-color: #e9ecef;
    cursor: not-allowed;
  }
  </style>