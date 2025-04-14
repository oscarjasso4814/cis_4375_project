<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { url } from "../api/apiurl"

const router = useRouter()
const route = useRoute()
const isLoading = ref(false)
const errors = ref({})
const saveError = ref('')
const customerId = ref(null)
const sameAsPhysicalAddress = ref(false)

// Simplified customer object with only essential fields
const customer = reactive({
  firstName: '',
  lastName: '',
  cell: '',
  phone2: '',
  email: '',
  address: '',
  city: '',
  state: '',
  zip: '',
  mailingAddress: '',
  mailingCity: '',
  mailingState: '',
  mailingZip: '',
  dateOfBirth: '',
  gender: '',
  maritalStatus: '',
  ssn: ''
})

// Function to copy physical address to mailing address
const copyPhysicalAddress = () => {
  if (sameAsPhysicalAddress.value) {
    customer.mailingAddress = customer.address
    customer.mailingCity = customer.city
    customer.mailingState = customer.state
    customer.mailingZip = customer.zip
  } else {
    customer.mailingAddress = ''
    customer.mailingCity = ''
    customer.mailingState = ''
    customer.mailingZip = ''
  }
}

// Function to format date from backend to YYYY-MM-DD for input fields
const formatDateForInput = (dateString) => {
  if (!dateString) return ''
  
  try {
    console.log('Formatting date:', dateString)
    // Handle different date formats
    let date
    if (typeof dateString === 'string' && dateString.includes('T')) {
      // ISO format
      date = new Date(dateString)
    } else if (typeof dateString === 'string' && dateString.includes('/')) {
      // MM/DD/YYYY format
      const parts = dateString.split('/')
      date = new Date(parts[2], parts[0] - 1, parts[1])
    } else {
      date = new Date(dateString)
    }
    
    if (isNaN(date.getTime())) {
      console.error('Invalid date:', dateString)
      return ''
    }
    
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const formattedDate = `${year}-${month}-${day}`
    
    return formattedDate
  } catch (e) {
    console.error('Error formatting date:', e, dateString)
    return ''
  }
}

// Format date for display
const formatDateForDisplay = (dateString) => {
  if (!dateString) return ''
  
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return ''
    
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const year = date.getFullYear()
    
    return `${month}/${day}/${year}`
  } catch (error) {
    console.error('Error formatting date for display:', error)
    return dateString
  }
}

// Function to fetch customer data - converted to use .then() and setTimeout
const fetchCustomerData = (id) => {
  isLoading.value = true
  saveError.value = ''
  errors.value = {}
  
  // Using setTimeout to delay the API call to prevent crashes
  setTimeout(() => {
    console.log('Fetching customer data for ID:', id)
    axios.get(`${url}/api/customer/${id}`)
      .then(response => {
        if (response.data && response.data.length > 0) {
          const customerData = response.data[0]
          console.log('Customer data from API:', customerData)
          
          // Map only the fields we need
          customer.firstName = customerData.FirstName ?? ''
          customer.lastName = customerData.LastName ?? ''
          customer.cell = customerData.Phone1 ?? ''
          customer.phone2 = customerData.Phone2 ?? ''
          customer.email = customerData.Email1 ?? ''
          customer.address = customerData.Address ?? ''
          customer.city = customerData.City ?? ''
          customer.state = customerData.State ?? 'TX'
          customer.zip = customerData.Zip ?? ''
          customer.mailingAddress = customerData.MailingAddress ?? ''
          customer.mailingCity = customerData.MailingCity ?? ''
          customer.mailingState = customerData.MailingState ?? ''
          customer.mailingZip = customerData.MailingZip ?? ''
          customer.dateOfBirth = customerData.DateOfBirth ? formatDateForInput(customerData.DateOfBirth) : ''
          customer.gender = customerData.Gender ?? ''
          customer.maritalStatus = customerData.MaritalStatus ?? ''
          customer.ssn = customerData.SocialSecurityNum ?? ''
  
          console.log('Customer object after mapping:', { ...customer })
        } else {
          console.error('No customer data found in response')
          saveError.value = 'Customer data not found'
        }
      })
      .catch(error => {
        console.error('Error fetching customer data:', error)
        saveError.value = `Error loading customer data: ${error.response?.data?.message || error.message || 'Unknown error'}`
      })
      .finally(() => {
        isLoading.value = false
      })
  }, 2000) // 2 second delay
}

// Function to validate form
const validateForm = () => {
  const newErrors = {}
  
  // Required fields validation
  if (!customer.firstName.trim()) newErrors.firstName = 'First name is required'
  if (!customer.lastName.trim()) newErrors.lastName = 'Last name is required'
  if (!customer.address.trim()) newErrors.address = 'Address is required'
  if (!customer.city.trim()) newErrors.city = 'City is required'
  if (!customer.zip.trim()) newErrors.zip = 'ZIP code is required'
  
  // Email validation if provided
  if (customer.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(customer.email)) {
    newErrors.email = 'Please enter a valid email address'
  }
  
  // Phone validation if provided
  if (customer.cell && !/^\d{10}$/.test(customer.cell.replace(/\D/g, ''))) {
    newErrors.cell = 'Please enter a valid 10-digit phone number'
  }
  
  // Date validation if provided
  const dateRegex = /^\d{4}-\d{2}-\d{2}$/ // YYYY-MM-DD format for input type="date"
  
  if (customer.dateOfBirth && !dateRegex.test(customer.dateOfBirth)) {
    newErrors.dateOfBirth = 'Please enter a valid date (YYYY-MM-DD)'
  }
  
  // Set errors and return validation result
  errors.value = newErrors
  return Object.keys(newErrors).length === 0
}

// Function to save the customer - converted to use .then() and setTimeout
const saveCustomer = () => {
  // Reset error messages
  saveError.value = ''
  
  // Validate the form first
  if (!validateForm()) {
    // Scroll to the first error
    const firstErrorEl = document.querySelector('.error-message')
    if (firstErrorEl) {
      firstErrorEl.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
    return
  }
  
  // Ask for confirmation before saving
  if (!confirm('Are you sure you want to save these changes?')) {
    return
  }
  
  isLoading.value = true
  
  // Only include the visible fields that we want to update
  // This avoids issues with columns that might not exist in the database
  const customerData = {
    // Only include the fields that are visible in the form
    FirstName: customer.firstName,
    LastName: customer.lastName,
    Phone1: customer.cell,
    Phone2: customer.phone2 || null,
    Email1: customer.email,
    Address: customer.address,
    City: customer.city,
    State: customer.state,
    Zip: customer.zip,
    MailingAddress: customer.mailingAddress,
    MailingCity: customer.mailingCity,
    MailingState: customer.mailingState,
    MailingZip: customer.mailingZip,
    DateOfBirth: customer.dateOfBirth,
    Gender: customer.gender,
    MaritalStatus: customer.maritalStatus,
    SocialSecurityNum: customer.ssn
  }
  
  console.log('Sending updated customer data:', customerData)
  
  // Using setTimeout to delay the API call
  setTimeout(() => {
    // Make the API call
    axios.put(`${url}/api/Customer/${customerId.value}`, customerData)
      .then(response => {
        // Success!
        alert('Customer updated successfully!')
        
        // Redirect back to the customer profile
        router.push(`/customer/${customerId.value}`)
      })
      .catch(error => {
        console.error('Error updating customer:', error)
        let errorMessage = 'Failed to update customer.'
        
        // Extract detailed error message if available
        if (error.response) {
          if (error.response.data && error.response.data.details) {
            errorMessage += ` Error: ${error.response.data.details}`
          } else if (error.response.data && error.response.data.error) {
            errorMessage += ` Error: ${error.response.data.error}`
          } else {
            errorMessage += ` Status: ${error.response.status} - ${error.response.statusText}`
          }
        } else if (error.request) {
          errorMessage += ' Network error, please check your connection.'
        } else {
          errorMessage += ` ${error.message}`
        }
        
        saveError.value = errorMessage
        
        // Scroll to the error message
        setTimeout(() => {
          const errorEl = document.querySelector('.save-error')
          if (errorEl) {
            errorEl.scrollIntoView({ behavior: 'smooth', block: 'center' })
          }
        }, 100)
      })
      .finally(() => {
        isLoading.value = false
      })
  }, 1000) // 1 second delay
}

// Function to cancel and return to previous page
const cancelEdit = () => {
  if (confirm('Are you sure you want to cancel? Any unsaved changes will be lost.')) {
    router.push(`/customer/${customerId.value}`)
  }
}

// Load customer data when component mounts - converted to use .then()
onMounted(() => {
  console.log('EditCustomer component mounted')
  
  // Get customer ID from route params
  customerId.value = route.params.id
  console.log('Route params ID:', customerId.value)
  
  setTimeout(() => {
    if (customerId.value) {
      fetchCustomerData(customerId.value)
    } else {
      saveError.value = 'No customer ID provided'
      console.error('No customer ID in route params')
    }
  }, 1000) // 1 second delay
})
</script>

<template>
  <div class="edit-customer-container">
    <div class="page-header">
      <h1 class="page-title">Edit Customer</h1>
      <div class="actions">
        <button @click="cancelEdit" class="secondary-btn">
          <i class="fas fa-arrow-left"></i> Cancel
        </button>
      </div>
    </div>

    <div class="form-container">
      <!-- Loading overlay -->
      <div v-if="isLoading" class="loading-overlay">
        <div class="spinner"></div>
        <p>Loading...</p>
      </div>

      <!-- Main error message -->
      <div v-if="saveError" class="save-error">
        <div class="error-box">
          <i class="fas fa-exclamation-triangle"></i>
          <span>{{ saveError }}</span>
        </div>
      </div>

      <form @submit.prevent="saveCustomer" class="customer-form">
        <!-- Basic Information Section -->
        <div class="form-section">
          <h2 class="section-title">Basic Information</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="first-name">First Name <span class="required">*</span></label>
              <input 
                type="text" 
                id="first-name" 
                v-model="customer.firstName" 
                class="input-field" 
                :class="{ 'error-input': errors.firstName }"
                required
              >
              <span v-if="errors.firstName" class="error-message">{{ errors.firstName }}</span>
            </div>
            
            <div class="form-group">
              <label for="last-name">Last Name <span class="required">*</span></label>
              <input 
                type="text" 
                id="last-name" 
                v-model="customer.lastName" 
                class="input-field"
                :class="{ 'error-input': errors.lastName }"
                required
              >
              <span v-if="errors.lastName" class="error-message">{{ errors.lastName }}</span>
            </div>
          </div>
        </div>
        
        <!-- Contact Information Section -->
        <div class="form-section">
          <h2 class="section-title">Contact Information</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="cell">Cell Phone <span class="required">*</span></label>
              <input 
                type="tel" 
                id="cell" 
                v-model="customer.cell" 
                class="input-field"
                :class="{ 'error-input': errors.cell }"
                placeholder="(XXX) XXX-XXXX"
                required
              >
              <span v-if="errors.cell" class="error-message">{{ errors.cell }}</span>
            </div>
            
            <div class="form-group">
              <label for="phone2">Alternate Phone</label>
              <input type="tel" id="phone2" v-model="customer.phone2" class="input-field" placeholder="(XXX) XXX-XXXX">
            </div>
            
            <div class="form-group">
              <label for="email">Email <span class="required">*</span></label>
              <input 
                type="email" 
                id="email" 
                v-model="customer.email" 
                class="input-field"
                :class="{ 'error-input': errors.email }"
                required
              >
              <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
            </div>
          </div>
        </div>
        
        <!-- Physical Address Section -->
        <div class="form-section">
          <h2 class="section-title">Physical Address</h2>
          <div class="form-grid">
            <div class="form-group full-width">
              <label for="address">Street Address <span class="required">*</span></label>
              <input 
                type="text" 
                id="address" 
                v-model="customer.address" 
                class="input-field"
                :class="{ 'error-input': errors.address }"
                required
              >
              <span v-if="errors.address" class="error-message">{{ errors.address }}</span>
            </div>
            
            <div class="form-group">
              <label for="city">City <span class="required">*</span></label>
              <input 
                type="text" 
                id="city" 
                v-model="customer.city" 
                class="input-field"
                :class="{ 'error-input': errors.city }"
                required
              >
              <span v-if="errors.city" class="error-message">{{ errors.city }}</span>
            </div>
            
            <div class="form-group">
              <label for="state">State <span class="required">*</span></label>
              <select 
                id="state" 
                v-model="customer.state" 
                class="input-field"
                required
              >
                <option value="AL">AL - Alabama</option>
                <option value="AK">AK - Alaska</option>
                <option value="AZ">AZ - Arizona</option>
                <option value="AR">AR - Arkansas</option>
                <option value="CA">CA - California</option>
                <option value="CO">CO - Colorado</option>
                <option value="CT">CT - Connecticut</option>
                <option value="DE">DE - Delaware</option>
                <option value="FL">FL - Florida</option>
                <option value="GA">GA - Georgia</option>
                <option value="HI">HI - Hawaii</option>
                <option value="ID">ID - Idaho</option>
                <option value="IL">IL - Illinois</option>
                <option value="IN">IN - Indiana</option>
                <option value="IA">IA - Iowa</option>
                <option value="KS">KS - Kansas</option>
                <option value="KY">KY - Kentucky</option>
                <option value="LA">LA - Louisiana</option>
                <option value="ME">ME - Maine</option>
                <option value="MD">MD - Maryland</option>
                <option value="MA">MA - Massachusetts</option>
                <option value="MI">MI - Michigan</option>
                <option value="MN">MN - Minnesota</option>
                <option value="MS">MS - Mississippi</option>
                <option value="MO">MO - Missouri</option>
                <option value="MT">MT - Montana</option>
                <option value="NE">NE - Nebraska</option>
                <option value="NV">NV - Nevada</option>
                <option value="NH">NH - New Hampshire</option>
                <option value="NJ">NJ - New Jersey</option>
                <option value="NM">NM - New Mexico</option>
                <option value="NY">NY - New York</option>
                <option value="NC">NC - North Carolina</option>
                <option value="ND">ND - North Dakota</option>
                <option value="OH">OH - Ohio</option>
                <option value="OK">OK - Oklahoma</option>
                <option value="OR">OR - Oregon</option>
                <option value="PA">PA - Pennsylvania</option>
                <option value="RI">RI - Rhode Island</option>
                <option value="SC">SC - South Carolina</option>
                <option value="SD">SD - South Dakota</option>
                <option value="TN">TN - Tennessee</option>
                <option value="TX">TX - Texas</option>
                <option value="UT">UT - Utah</option>
                <option value="VT">VT - Vermont</option>
                <option value="VA">VA - Virginia</option>
                <option value="WA">WA - Washington</option>
                <option value="WV">WV - West Virginia</option>
                <option value="WI">WI - Wisconsin</option>
                <option value="WY">WY - Wyoming</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="zip">ZIP Code <span class="required">*</span></label>
              <input 
                type="text" 
                id="zip" 
                v-model="customer.zip" 
                class="input-field"
                :class="{ 'error-input': errors.zip }"
                required
              >
              <span v-if="errors.zip" class="error-message">{{ errors.zip }}</span>
            </div>
          </div>
        </div>
        
        <!-- Mailing Address Section -->
        <div class="form-section">
          <h2 class="section-title">Mailing Address</h2>
          <div class="form-grid">
            <!-- Checkbox for "Same as Physical Address" -->
            <div class="form-group full-width">
              <label>
                <input 
                  type="checkbox" 
                  v-model="sameAsPhysicalAddress" 
                  @change="copyPhysicalAddress"
                >
                Same as Physical Address
              </label>
            </div>

            <div class="form-group full-width">
              <label for="mailing-address">Street Address</label>
              <input type="text" id="mailing-address" v-model="customer.mailingAddress" class="input-field">
            </div>

            <div class="form-group">
              <label for="mailing-city">City</label>
              <input type="text" id="mailing-city" v-model="customer.mailingCity" class="input-field">
            </div>

            <div class="form-group">
              <label for="mailing-state">State</label>
              <select id="mailing-state" v-model="customer.mailingState" class="input-field">
                <option value=""></option>
                <option value="AL">AL - Alabama</option>
                <option value="AK">AK - Alaska</option>
                <option value="AZ">AZ - Arizona</option>
                <option value="AR">AR - Arkansas</option>
                <option value="CA">CA - California</option>
                <option value="CO">CO - Colorado</option>
                <option value="CT">CT - Connecticut</option>
                <option value="DE">DE - Delaware</option>
                <option value="FL">FL - Florida</option>
                <option value="GA">GA - Georgia</option>
                <option value="HI">HI - Hawaii</option>
                <option value="ID">ID - Idaho</option>
                <option value="IL">IL - Illinois</option>
                <option value="IN">IN - Indiana</option>
                <option value="IA">IA - Iowa</option>
                <option value="KS">KS - Kansas</option>
                <option value="KY">KY - Kentucky</option>
                <option value="LA">LA - Louisiana</option>
                <option value="ME">ME - Maine</option>
                <option value="MD">MD - Maryland</option>
                <option value="MA">MA - Massachusetts</option>
                <option value="MI">MI - Michigan</option>
                <option value="MN">MN - Minnesota</option>
                <option value="MS">MS - Mississippi</option>
                <option value="MO">MO - Missouri</option>
                <option value="MT">MT - Montana</option>
                <option value="NE">NE - Nebraska</option>
                <option value="NV">NV - Nevada</option>
                <option value="NH">NH - New Hampshire</option>
                <option value="NJ">NJ - New Jersey</option>
                <option value="NM">NM - New Mexico</option>
                <option value="NY">NY - New York</option>
                <option value="NC">NC - North Carolina</option>
                <option value="ND">ND - North Dakota</option>
                <option value="OH">OH - Ohio</option>
                <option value="OK">OK - Oklahoma</option>
                <option value="OR">OR - Oregon</option>
                <option value="PA">PA - Pennsylvania</option>
                <option value="RI">RI - Rhode Island</option>
                <option value="SC">SC - South Carolina</option>
                <option value="SD">SD - South Dakota</option>
                <option value="TN">TN - Tennessee</option>
                <option value="TX">TX - Texas</option>
                <option value="UT">UT - Utah</option>
                <option value="VT">VT - Vermont</option>
                <option value="VA">VA - Virginia</option>
                <option value="WA">WA - Washington</option>
                <option value="WV">WV - West Virginia</option>
                <option value="WI">WI - Wisconsin</option>
                <option value="WY">WY - Wyoming</option>
              </select>
            </div>

            <div class="form-group">
              <label for="mailing-zip">ZIP Code</label>
              <input type="text" id="mailing-zip" v-model="customer.mailingZip" class="input-field">
            </div>
          </div>
        </div>
        
        <!-- Personal Details Section -->
        <div class="form-section">
          <h2 class="section-title">Personal Details</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="dob">Date of Birth</label>
              <input 
                type="date" 
                id="dob" 
                v-model="customer.dateOfBirth" 
                class="input-field"
                :class="{ 'error-input': errors.dateOfBirth }"
              >
              <span v-if="errors.dateOfBirth" class="error-message">{{ errors.dateOfBirth }}</span>
            </div>
            
            <div class="form-group">
              <label for="gender">Gender</label>
              <select id="gender" v-model="customer.gender" class="input-field">
                <option value=""></option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Non-Binary">Non-Binary</option>
                <option value="Other">Other</option>
                <option value="Prefer not to say">Prefer not to say</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="marital-status">Marital Status</label>
              <select id="marital-status" v-model="customer.maritalStatus" class="input-field">
                <option value=""></option>
                <option value="Single">Single</option>
                <option value="Married">Married</option>
                <option value="Divorced">Divorced</option>
                <option value="Widowed">Widowed</option>
                <option value="Separated">Separated</option>
                <option value="Other">Other</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="ssn">SSN/Tax ID</label>
              <input type="text" id="ssn" v-model="customer.ssn" class="input-field" placeholder="XXX-XX-XXXX">
            </div>
          </div>
        </div>
        
        <!-- Form Actions -->
        <div class="form-actions">
          <button type="submit" class="primary-btn">
            <i class="fas fa-save"></i> Save Changes
          </button>
          <button type="button" @click="cancelEdit" class="secondary-btn">
            <i class="fas fa-times"></i> Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* Main Container Styles */
.edit-customer-container {
  width: 100%;
  max-width: 1200px;
  margin: 60px auto 0;
  padding: 20px;
  background-color: #f9f9f9;
  color: #333;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ddd;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.actions {
  display: flex;
  gap: 10px;
}

/* Form Container */
.form-container {
  position: relative;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 100%;
}

/* Form Sections */
.form-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.form-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.full-width {
  grid-column: 1 / -1;
}

/* Form Groups */
.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
  font-size: 14px;
}

.required {
  color: #dc3545;
  margin-left: 3px;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  background-color: #fff;
  transition: border-color 0.2s ease;
}

.input-field:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.error-input {
  border-color: #dc3545;
}

.error-message {
  display: block;
  color: #dc3545;
  font-size: 12px;
  margin-top: 4px;
}

/* Save Error Message */
.save-error {
  margin-bottom: 20px;
}

.error-box {
  background-color: #f8d7da;
  color: #721c24;
  padding: 12px 15px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.error-box i {
  font-size: 18px;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

/* Button Styles */
.primary-btn,
.secondary-btn,
.action-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.primary-btn {
  background-color: #007bff;
  color: white;
}

.primary-btn:hover {
  background-color: #0069d9;
}

.secondary-btn {
  background-color: #6c757d;
  color: white;
}

.secondary-btn:hover {
  background-color: #5a6268;
}

/* Loading Overlay */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  border-radius: 8px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(0, 123, 255, 0.3);
  border-radius: 50%;
  border-top-color: #007bff;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive Styles */
@media (max-width: 768px) {
  .edit-customer-container {
    padding: 15px;
    margin-top: 50px;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .primary-btn, .secondary-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>