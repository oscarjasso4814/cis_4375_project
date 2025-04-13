<template>
    <div class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-content">
        <h3>Add Policy for {{ customerName }}</h3>
  
        <!----<div class="customer-info">
          <p><strong>Customer ID:</strong> {{ customerId }}</p>
        </div> ---->
  
        <!-- Loading indicator -->
        <div v-if="isLoading" class="loading-container">
          <div class="spinner"></div>
          <p>Loading data...</p>
        </div>
  
        <form v-else @submit.prevent="submitPolicy">
          <!-- Policy Category -->
          <div class="form-group">
            <label>Policy Category:</label>
            <select v-model="policy.categoryId" required @change="loadSubcategories">
              <option disabled value="">-- Select Category --</option>
              <option v-for="category in categories" :key="category.CategoryID" :value="category.CategoryID">
                {{ category.CategoryName }}
              </option>
            </select>
          </div>
  
          <!-- Policy Subcategory -->
          <div class="form-group">
            <label>Policy Subcategory:</label>
            <select v-model="policy.subcategoryId" :disabled="!policy.categoryId">
              <option disabled value="">-- Select Subcategory --</option>
              <option v-for="subcategory in subcategories" :key="subcategory.SubcategoryID" :value="subcategory.SubcategoryID">
                {{ subcategory.SubcategoryName }}
              </option>
            </select>
          </div>
  
          <!-- Insurance Company -->
          <div class="form-group">
            <label>Insurance Company:</label>
            <select v-model="policy.companyId" required>
              <option disabled value="">-- Select Company --</option>
              <option v-for="company in companies" :key="company.CompanyID" :value="company.CompanyID">
                {{ company.CompanyName }}
              </option>
            </select>
          </div>
  
          <!-- Policy Number -->
          <div class="form-group">
            <label>Policy Number:</label>
            <input v-model="policy.policyNumber" required placeholder="Enter policy number" />
          </div>
  
          <!-- Issuer (if different from company) -->
          <div class="form-group">
            <label>Issuer/Underwriter (if different):</label>
            <input v-model="policy.issuer" placeholder="Enter issuer if different from company" />
          </div>
  
          <!-- Effective Date -->
          <div class="form-group">
            <label>Effective Date:</label>
            <input type="date" v-model="policy.effectiveDate" required />
          </div>
  
          <!-- Expiration Date -->
          <div class="form-group">
            <label>Expiration Date:</label>
            <input type="date" v-model="policy.expirationDate" />
          </div>
          
          <!-- Premium Amount -->
            <div class="form-group">
                <label>Premium Amount:</label>
                <input 
                    type="number" 
                    v-model="policy.premium" 
                    placeholder="Enter premium amount" 
                    step="0.01" 
                    min="0"
                    @input="validatePremiumInput" 
                />
                <small v-if="premiumHelpText" class="helper-text">{{premiumHelpText}}</small>
            </div>
          

          <!-- Agent of Record -->
          <div class="form-group">
            <label>Agent of Record:</label>
            <select v-model="policy.agentRecordId">
              <option disabled value="">-- Select Agent --</option>
              <option v-for="agent in agents" :key="agent.AgentRecordID" :value="agent.AgentRecordID">
                {{ agent.AgentName }}
              </option>
            </select>
          </div>
  
          <!-- Representative -->
          <div class="form-group">
            <label>Representative:</label>
            <select v-model="policy.representativeId">
              <option disabled value="">-- Select Representative --</option>
              <option v-for="rep in representatives" :key="rep.RepresentativeID" :value="rep.RepresentativeID">
                {{ rep.FirstName }} {{ rep.LastName }}
              </option>
            </select>
          </div>
  
          <!-- Additional Info -->
          <div class="form-group">
            <label>Additional Information:</label>
            <textarea v-model="policy.additionalInfo" rows="3" placeholder="Enter additional information about this policy"></textarea>
          </div>
  
          <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>
  
          <div class="actions">
            <button type="submit" class="btn-primary">Add Policy</button>
            <button type="button" class="btn-secondary" @click="$emit('close')">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue';
  import axios from 'axios';
  import { url } from "../api/apiurl";
  
  const props = defineProps({
    customerId: {
      type: Number,
      required: true
    },
    customerName: {
      type: String,
      required: true
    }
  });
  
  const emit = defineEmits(['close', 'policy-added']);
  
  // State management
  const isLoading = ref(true);
  const errorMessage = ref('');
  
  // Data lists
  const categories = ref([]);
  const subcategories = ref([]);
  const companies = ref([]);
  const agents = ref([]);
  const representatives = ref([]);
  
  // Policy data
  const policy = reactive({
    customerId: props.customerId,
    categoryId: '',
    subcategoryId: '',
    companyId: '',
    policyNumber: '',
    issuer: '',
    effectiveDate: '',
    expirationDate: '',
    agentRecordId: '',
    representativeId: '',
    additionalInfo: ''
  });
  
  // Load initial data
  async function loadData() {
    isLoading.value = true;
    errorMessage.value = '';
    
    try {
      // Try to fetch categories
      try {
        const categoriesRes = await axios.get(`${url}/api/categories`);
        categories.value = categoriesRes.data;
        console.log("Categories loaded:", categories.value);
      } catch (error) {
        console.error("Error loading categories:", error);
        // Use placeholder data for development
        categories.value = [
          { CategoryID: 1, CategoryName: "Auto" },
          { CategoryID: 2, CategoryName: "Home" },
          { CategoryID: 3, CategoryName: "Life" },
          { CategoryID: 4, CategoryName: "Health" }
        ];
      }
      
      // Try to fetch companies
      try {
        const companiesRes = await axios.get(`${url}/api/companies`);
        companies.value = companiesRes.data;
        console.log("Companies loaded:", companies.value);
      } catch (error) {
        console.error("Error loading companies:", error);
        // Use placeholder data for development
        companies.value = [
          { CompanyID: 1, CompanyName: "State Farm" },
          { CompanyID: 2, CompanyName: "Allstate" },
          { CompanyID: 3, CompanyName: "Progressive" }
        ];
      }
      
      // Try to fetch agents
      try {
        const agentsRes = await axios.get(`${url}/api/agents`);
        agents.value = agentsRes.data;
        console.log("Agents loaded:", agents.value);
      } catch (error) {
        console.error("Error loading agents:", error);
        // Use placeholder data for development
        agents.value = [
          { AgentRecordID: 1, AgentName: "John Agent" },
          { AgentRecordID: 2, AgentName: "Mary Agent" }
        ];
      }
      
      // Try to fetch representatives
      try {
        const repsRes = await axios.get(`${url}/api/Representative`);
        representatives.value = repsRes.data;
        console.log("Representatives loaded:", representatives.value);
      } catch (error) {
        console.error("Error loading representatives:", error);
        // Use placeholder data
        representatives.value = [
          { RepresentativeID: 1, FirstName: "John", LastName: "Doe" },
          { RepresentativeID: 2, FirstName: "Jane", LastName: "Smith" }
        ];
      }
      
      // Set current user as representative if available
      const currentRepId = localStorage.getItem('reps_id');
      if (currentRepId) {
        policy.representativeId = parseInt(currentRepId);
      }
      
    } catch (error) {
      console.error('Error loading form data:', error);
      errorMessage.value = 'Failed to load form data completely. Some options may be unavailable.';
    } finally {
      isLoading.value = false;
    }
  }
  
  // Load subcategories when category changes
  async function loadSubcategories() {
  if (!policy.categoryId) return;
  
  try {
    isLoading.value = true;
    console.log(`Loading subcategories for category ID: ${policy.categoryId}`);
    
    const res = await axios.get(`${url}/api/categories/${policy.categoryId}/subcategories`);
    
    // Check if the response has data and it's an array
    if (res.data && Array.isArray(res.data)) {
      subcategories.value = res.data;
      console.log("Subcategories loaded:", subcategories.value);
    } else {
      console.warn("Received empty or invalid subcategories data");
      subcategories.value = [];
    }
  } catch (error) {
    console.error('Error loading subcategories:', error);
    
    // Set default subcategories based on selected category
    if (policy.categoryId === 1) { // Auto
      subcategories.value = [
        { SubcategoryID: 1, SubcategoryName: "Auto Liability" },
        { SubcategoryID: 2, SubcategoryName: "Comprehensive" },
        { SubcategoryID: 3, SubcategoryName: "Collision" }
      ];
    } else if (policy.categoryId === 2) { // Home
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
  } finally {
    isLoading.value = false;
  }
}
  
  // Validate premium input to ensure it has no more than 2 decimal places
  const premiumHelpText = ref('');
  function validatePremiumInput() {
    const value = policy.premium.toString();
    const decimalParts = value.split('.');
    
    if (decimalParts.length > 1 && decimalParts[1].length > 2) {
      premiumHelpText.value = 'Premium must be a whole number or have up to 2 decimal places (e.g., 90 or 90.90)';
    } else {
      premiumHelpText.value = '';
    }
  }
  
// Update the validateForm function to include premium validation
function validateForm() {
  // Reset error message
  errorMessage.value = '';
  
  // Basic validation
  if (!policy.categoryId) {
    errorMessage.value = 'Please select a policy category';
    return false;
  }
  
  if (!policy.companyId) {
    errorMessage.value = 'Please select an insurance company';
    return false;
  }
  
  if (!policy.policyNumber) {
    errorMessage.value = 'Please enter a policy number';
    return false;
  }
  
  if (!policy.effectiveDate) {
    errorMessage.value = 'Please enter an effective date';
    return false;
  }
  
  // Premium validation - check if it has more than 2 decimal places
  if (policy.premium) {
    const premiumStr = policy.premium.toString();
    const decimalParts = premiumStr.split('.');
    
    if (decimalParts.length > 1 && decimalParts[1].length > 2) {
      errorMessage.value = 'Premium must be a whole number or have up to 2 decimal places (e.g., 90 or 90.90)';
      return false;
    }
  }
  
  // Validate expiration date is after effective date
  if (policy.effectiveDate && policy.expirationDate) {
    const effectiveDate = new Date(policy.effectiveDate);
    const expirationDate = new Date(policy.expirationDate);
    
    if (expirationDate < effectiveDate) {
      errorMessage.value = 'Expiration date must be after effective date';
      return false;
    }
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
      CustomerID: props.customerId,
      CategoryID: policy.categoryId,
      SubcategoryID: policy.subcategoryId || null,
      CompanyID: policy.companyId,
      PolicyNumber: policy.policyNumber,
      Issuer: policy.issuer || null,
      EffectiveDate: policy.effectiveDate,
      ExpirationDate: policy.expirationDate || null,
      Premium: policy.premium || 0,
      AgentRecordID: policy.agentRecordId || null,
      RepresentativeID: policy.representativeId || null,
      AdditionalInfo: policy.additionalInfo || null
    };
    
    console.log("Submitting policy data:", policyData);
    
    const response = await axios.post(`${url}/api/policy`, policyData);
    console.log("Policy created successfully:", response.data);
    
    // Emit event to refresh policy list
    emit('policy-added', response.data);
    
    // Close modal
    emit('close');
    
  } catch (error) {
    console.error('Error adding policy:', error);
    
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
    width: 500px;
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
    color: #000;
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
  
  .retry-btn {
    margin-top: 15px;
    width: auto;
    padding: 6px 15px;
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
  </style>