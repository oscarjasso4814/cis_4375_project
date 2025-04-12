<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { url } from "../api/apiurl"

const router = useRouter()
const isLoading = ref(false)
const errors = ref({})

// Initialize the customer object with all required fields
const customer = reactive({
  type: 'Personal Lines',
  firstName: '',
  middleName: '',
  lastName: '',
  suffix: '',
  title: '',
  salutation: '',
  activeStatus: 'Active',
  country: 'United States',
  isUsaCitizen: false,
  address: '',
  zip: '',
  city: '',
  state: 'TX',
  addressVerified: false,
  sameAddress: false,
  mailingCountry: 'United States',
  mailingAddress: '',
  mailingZip: '',
  mailingCity: '',
  mailingState: 'TX',
  cell: '',
  phone2: '',
  phone3: '',
  phone4: '',
  driversLicense: '',
  dlState: 'TX',
  dateLicensed: '',
  dateOfBirth: '',
  ssn: '',
  gender: '',
  maritalStatus: '',
  householdSize: '',
  peopleApplying: '',
  householdIncome: '',
  email: '',
  email2: '',
  website: '',
  preferredContact: 'None',
  doNotEmail: false,
  doNotText: false,
  doNotCall: false,
  doNotMail: false,
  doNotMarket: false,
  doNotCaptureEmail: false,
  undeliverableMail: false,
  badCell: false,
  badPhone2: false,
  badPhone3: false,
  badPhone4: false,
  undeliverableEmail1: false,
  undeliverableEmail2: false
})

// When "Same Address" is checked, copy physical address to mailing address
const handleSameAddressChange = () => {
  if (customer.sameAddress) {
    customer.mailingAddress = customer.address
    customer.mailingZip = customer.zip
    customer.mailingCity = customer.city
    customer.mailingState = customer.state
    customer.mailingCountry = customer.country
  } else {
    // Clear mailing address fields if unchecked
    customer.mailingAddress = ''
    customer.mailingZip = ''
    customer.mailingCity = ''
    customer.mailingState = ''
  }
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
  
  if (customer.dateLicensed && !dateRegex.test(customer.dateLicensed)) {
    newErrors.dateLicensed = 'Please enter a valid date (YYYY-MM-DD)'
  }
  
  // Set errors and return validation result
  errors.value = newErrors
  return Object.keys(newErrors).length === 0
}

// Format the customer data for the API
const formatCustomerData = () => {
  // Get the full name
  const fullName = [
    customer.firstName, 
    customer.middleName, 
    customer.lastName
  ].filter(Boolean).join(' ')
  
  return {
    Type: customer.type,
    FirstName: customer.firstName,
    MiddleName: customer.middleName || null,
    LastName: customer.lastName,
    Suffix: customer.suffix || null,
    Title: customer.title || null,
    Salutation: customer.salutation || null,
    ActiveStatus: customer.activeStatus === 'Active' ? 1 : 0,
    Country: customer.country,
    IsUSACitizen: customer.isUsaCitizen ? 1 : 0,
    Address: customer.address,
    Zip: customer.zip,
    City: customer.city,
    State: customer.state,
    AddressVerified: customer.addressVerified ? 1 : 0,
    MailingCountry: customer.sameAddress ? customer.country : customer.mailingCountry,
    MailingAddress: customer.sameAddress ? customer.address : customer.mailingAddress,
    MailingZip: customer.sameAddress ? customer.zip : customer.mailingZip,
    MailingCity: customer.sameAddress ? customer.city : customer.mailingCity,
    MailingState: customer.sameAddress ? customer.state : customer.mailingState,
    Phone1: customer.cell,
    Phone2: customer.phone2 || null,
    Phone3: customer.phone3 || null,
    Phone4: customer.phone4 || null,
    DriversLicenseNum: customer.driversLicense || null,
    DriversLicenseState: customer.dlState || null,
    DateLicensed: customer.dateLicensed || null,
    DateOfBirth: customer.dateOfBirth || null,
    SocialSecurityNum: customer.ssn || null,
    Gender: customer.gender || null,
    MaritalStatus: customer.maritalStatus || null,
    HouseholdSize: customer.householdSize || null,
    PeopleApplying: customer.peopleApplying || null,
    HouseholdIncome: customer.householdIncome || null,
    Email1: customer.email || null,
    Email2: customer.email2 || null,
    Website: customer.website || null,
    PreferredContact: customer.preferredContact,
    DoNotEmail: customer.doNotEmail ? 1 : 0,
    DoNotText: customer.doNotText ? 1 : 0,
    DoNotCall: customer.doNotCall ? 1 : 0,
    DoNotMail: customer.doNotMail ? 1 : 0,
    DoNotMarket: customer.doNotMarket ? 1 : 0,
    DoNotCaptureEmail: customer.doNotCaptureEmail ? 1 : 0,
    UndeliverableMail: customer.undeliverableMail ? 1 : 0,
    BadCell: customer.badCell ? 1 : 0,
    BadPhone2: customer.badPhone2 ? 1 : 0,
    BadPhone3: customer.badPhone3 ? 1 : 0,
    BadPhone4: customer.badPhone4 ? 1 : 0,
    UndeliverableEmail1: customer.undeliverableEmail1 ? 1 : 0,
    UndeliverableEmail2: customer.undeliverableEmail2 ? 1 : 0,
    DateAdded: new Date().toISOString().split('T')[0]
  }
}

// Function to save the customer
const saveCustomer = async () => {
  // Validate the form first
  if (!validateForm()) {
    // Scroll to the first error
    const firstErrorEl = document.querySelector('.error-message')
    if (firstErrorEl) {
      firstErrorEl.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
    return
  }
  
  try {
    isLoading.value = true
    
    // Format customer data for API
    const customerData = formatCustomerData()
    
    // Mock API call - replace with your actual API endpoint
    console.log('Sending customer data:', customerData)
    
    // Simulate API call
    setTimeout(() => {
      alert('Customer added successfully!')
      // Redirect to customer profile (replace with actual ID)
      router.push('/')
      isLoading.value = false
    }, 1000)
    
    // Uncomment this for actual API implementation
    // const response = await axios.post(`${url}/api/Customer`, customerData)
    // if (response.data && response.data.CustomerID) {
    //   router.push(`/customer/${response.data.CustomerID}`)
    // } else {
    //   alert('Customer added successfully!')
    //   router.push('/')
    // }
  } catch (error) {
    console.error('Error saving customer:', error)
    alert('Failed to save customer. Please try again.')
    isLoading.value = false
  }
}

// Function to handle address verification
const verifyAddress = async () => {
  // This would normally call an address verification API
  // For now, just simulate the process
  
  if (!customer.address || !customer.city || !customer.state || !customer.zip) {
    alert('Please fill in all address fields before verification.')
    return
  }
  
  isLoading.value = true
  
  // Simulate API call delay
  setTimeout(() => {
    customer.addressVerified = true
    isLoading.value = false
    alert('Address has been verified successfully!')
  }, 1000)
}

// Function to verify mailing address
const verifyMailingAddress = async () => {
  if (!customer.mailingAddress || !customer.mailingCity || !customer.mailingState || !customer.mailingZip) {
    alert('Please fill in all mailing address fields before verification.')
    return
  }
  
  isLoading.value = true
  
  // Simulate API call delay
  setTimeout(() => {
    isLoading.value = false
    alert('Mailing address has been verified successfully!')
  }, 1000)
}

// Function to cancel and return to previous page
const cancelEdit = () => {
  router.go(-1) // Go back to previous page
}

// US States for dropdown
const usStates = [
  { value: 'AL', name: 'Alabama' },
  { value: 'AK', name: 'Alaska' },
  { value: 'AZ', name: 'Arizona' },
  { value: 'AR', name: 'Arkansas' },
  { value: 'CA', name: 'California' },
  { value: 'CO', name: 'Colorado' },
  { value: 'CT', name: 'Connecticut' },
  { value: 'DE', name: 'Delaware' },
  { value: 'FL', name: 'Florida' },
  { value: 'GA', name: 'Georgia' },
  { value: 'HI', name: 'Hawaii' },
  { value: 'ID', name: 'Idaho' },
  { value: 'IL', name: 'Illinois' },
  { value: 'IN', name: 'Indiana' },
  { value: 'IA', name: 'Iowa' },
  { value: 'KS', name: 'Kansas' },
  { value: 'KY', name: 'Kentucky' },
  { value: 'LA', name: 'Louisiana' },
  { value: 'ME', name: 'Maine' },
  { value: 'MD', name: 'Maryland' },
  { value: 'MA', name: 'Massachusetts' },
  { value: 'MI', name: 'Michigan' },
  { value: 'MN', name: 'Minnesota' },
  { value: 'MS', name: 'Mississippi' },
  { value: 'MO', name: 'Missouri' },
  { value: 'MT', name: 'Montana' },
  { value: 'NE', name: 'Nebraska' },
  { value: 'NV', name: 'Nevada' },
  { value: 'NH', name: 'New Hampshire' },
  { value: 'NJ', name: 'New Jersey' },
  { value: 'NM', name: 'New Mexico' },
  { value: 'NY', name: 'New York' },
  { value: 'NC', name: 'North Carolina' },
  { value: 'ND', name: 'North Dakota' },
  { value: 'OH', name: 'Ohio' },
  { value: 'OK', name: 'Oklahoma' },
  { value: 'OR', name: 'Oregon' },
  { value: 'PA', name: 'Pennsylvania' },
  { value: 'RI', name: 'Rhode Island' },
  { value: 'SC', name: 'South Carolina' },
  { value: 'SD', name: 'South Dakota' },
  { value: 'TN', name: 'Tennessee' },
  { value: 'TX', name: 'Texas' },
  { value: 'UT', name: 'Utah' },
  { value: 'VT', name: 'Vermont' },
  { value: 'VA', name: 'Virginia' },
  { value: 'WA', name: 'Washington' },
  { value: 'WV', name: 'West Virginia' },
  { value: 'WI', name: 'Wisconsin' },
  { value: 'WY', name: 'Wyoming' }
]
</script>

<template>
  <div class="add-customer-container">
    <div class="page-header">
      <h1 class="page-title">Add New Customer</h1>
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
        <p>Processing...</p>
      </div>

      <form @submit.prevent="saveCustomer" class="customer-form">
        <!-- Basic Information Section -->
        <div class="form-section">
          <h2 class="section-title">Basic Information</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="customer-type">Customer Type <span class="required">*</span></label>
              <select id="customer-type" v-model="customer.type" class="input-field">
                <option value="Personal Lines">Personal Lines</option>
                <option value="Commercial">Commercial</option>
              </select>
            </div>
            
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
              <label for="middle-name">Middle Name</label>
              <input type="text" id="middle-name" v-model="customer.middleName" class="input-field">
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
            
            <div class="form-group">
              <label for="suffix">Suffix</label>
              <input type="text" id="suffix" v-model="customer.suffix" class="input-field">
            </div>
            
            <div class="form-group">
              <label for="title">Title</label>
              <input type="text" id="title" v-model="customer.title" class="input-field">
            </div>
            
            <div class="form-group">
              <label for="salutation">Salutation</label>
              <input type="text" id="salutation" v-model="customer.salutation" class="input-field">
            </div>
            
            <div class="form-group">
              <label for="status">Status</label>
              <select id="status" v-model="customer.activeStatus" class="input-field">
                <option value="Active">Active</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="country">Country</label>
              <select id="country" v-model="customer.country" class="input-field">
                <option value="United States">United States</option>
                <option value="Canada">Canada</option>
                <option value="Mexico">Mexico</option>
                <option value="Other">Other</option>
              </select>
            </div>
            
            <div class="form-group checkbox-group">
              <input type="checkbox" id="us-citizen" v-model="customer.isUsaCitizen">
              <label for="us-citizen">US Citizen</label>
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
                <option v-for="state in usStates" :key="state.value" :value="state.value">
                  {{ state.value }} - {{ state.name }}
                </option>
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
            
            <div class="form-group address-actions">
              <button type="button" @click="verifyAddress" class="action-btn">
                <i class="fas fa-check-circle"></i> Verify Address
              </button>
              
              <div class="checkbox-group">
                <input type="checkbox" id="address-verified" v-model="customer.addressVerified">
                <label for="address-verified">Address Verified</label>
              </div>
              
              <div class="checkbox-group">
                <input type="checkbox" id="same-address" v-model="customer.sameAddress" @change="handleSameAddressChange">
                <label for="same-address">Same as Mailing Address</label>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Mailing Address Section -->
        <div class="form-section" :class="{ 'disabled-section': customer.sameAddress }">
          <h2 class="section-title">Mailing Address</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="mailing-country">Country</label>
              <select id="mailing-country" v-model="customer.mailingCountry" class="input-field" :disabled="customer.sameAddress">
                <option value="United States">United States</option>
                <option value="Canada">Canada</option>
                <option value="Mexico">Mexico</option>
                <option value="Other">Other</option>
              </select>
            </div>
            
            <div class="form-group full-width">
              <label for="mailing-address">Street Address</label>
              <input type="text" id="mailing-address" v-model="customer.mailingAddress" class="input-field" :disabled="customer.sameAddress">
            </div>
            
            <div class="form-group">
              <label for="mailing-city">City</label>
              <input type="text" id="mailing-city" v-model="customer.mailingCity" class="input-field" :disabled="customer.sameAddress">
            </div>
            
            <div class="form-group">
              <label for="mailing-state">State</label>
              <select id="mailing-state" v-model="customer.mailingState" class="input-field" :disabled="customer.sameAddress">
                <option v-for="state in usStates" :key="state.value" :value="state.value">
                  {{ state.value }} - {{ state.name }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="mailing-zip">ZIP Code</label>
              <input type="text" id="mailing-zip" v-model="customer.mailingZip" class="input-field" :disabled="customer.sameAddress">
            </div>
            
            <div class="form-group" v-if="!customer.sameAddress">
              <button type="button" @click="verifyMailingAddress" class="action-btn">
                <i class="fas fa-check-circle"></i> Verify Mailing Address
              </button>
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
              <label for="phone3">Work Phone</label>
              <input type="tel" id="phone3" v-model="customer.phone3" class="input-field" placeholder="(XXX) XXX-XXXX">
            </div>
            
            <div class="form-group">
              <label for="phone4">Other Phone</label>
              <input type="tel" id="phone4" v-model="customer.phone4" class="input-field" placeholder="(XXX) XXX-XXXX">
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
            
            <div class="form-group">
              <label for="email2">Secondary Email</label>
              <input type="email" id="email2" v-model="customer.email2" class="input-field">
            </div>
            
            <div class="form-group">
              <label for="website">Website</label>
              <input type="url" id="website" v-model="customer.website" class="input-field" placeholder="https://">
            </div>
            
            <div class="form-group">
              <label for="preferred-contact">Preferred Contact Method</label>
              <select id="preferred-contact" v-model="customer.preferredContact" class="input-field">
                <option value="None">None</option>
                <option value="Email">Email</option>
                <option value="Phone">Phone</option>
                <option value="Text">Text</option>
                <option value="Mail">Mail</option>
              </select>
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
            
            <div class="form-group">
              <label for="drivers-license">Driver's License #</label>
              <input type="text" id="drivers-license" v-model="customer.driversLicense" class="input-field">
            </div>
            
            <div class="form-group">
              <label for="dl-state">DL State</label>
              <select id="dl-state" v-model="customer.dlState" class="input-field">
                <option v-for="state in usStates" :key="state.value" :value="state.value">
                  {{ state.value }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="date-licensed">Date Licensed</label>
              <input 
                type="date" 
                id="date-licensed" 
                v-model="customer.dateLicensed" 
                class="input-field"
                :class="{ 'error-input': errors.dateLicensed }"
              >
              <span v-if="errors.dateLicensed" class="error-message">{{ errors.dateLicensed }}</span>
            </div>
          </div>
        </div>
        
        <!-- Household Information Section -->
        <div class="form-section">
          <h2 class="section-title">Household Information</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="household-size">Household Size</label>
              <input type="number" id="household-size" v-model="customer.householdSize" class="input-field" min="1">
            </div>
            
            <div class="form-group">
              <label for="people-applying">People Applying</label>
              <input type="number" id="people-applying" v-model="customer.peopleApplying" class="input-field" min="1">
            </div>
            
            <div class="form-group">
              <label for="household-income">Household Income ($)</label>
              <input type="number" id="household-income" v-model="customer.householdIncome" class="input-field" min="0">
            </div>
          </div>
        </div>
        
        <!-- Preferences Section -->
        <div class="form-section">
          <h2 class="section-title">Contact Preferences</h2>
          <div class="form-grid preferences-grid">
            <div class="form-group checkbox-group">
              <input type="checkbox" id="do-not-email" v-model="customer.doNotEmail">
              <label for="do-not-email">Do Not Email</label>
            </div>
            
            <div class="form-group checkbox-group">
              <input type="checkbox" id="do-not-text" v-model="customer.doNotText">
              <label for="do-not-text">Do Not Text</label>
            </div>
            
            <div class="form-group checkbox-group">
              <input type="checkbox" id="do-not-call" v-model="customer.doNotCall">
              <label for="do-not-call">Do Not Call</label>
            </div>
            
            <div class="form-group checkbox-group">
              <input type="checkbox" id="do-not-mail" v-model="customer.doNotMail">
              <label for="do-not-mail">Do Not Mail</label>
            </div>
            
            <div class="form-group checkbox-group">
              <input type="checkbox" id="do-not-market" v-model="customer.doNotMarket">
              <label for="do-not-market">Do Not Market</label>
            </div>
            
            <div class="form-group checkbox-group">
              <input type="checkbox" id="do-not-capture-email" v-model="customer.doNotCaptureEmail">
              <label for="do-not-capture-email">Do Not Capture Email</label>
            </div>
            
            <div class="form-group checkbox-group">
              <input type="checkbox" id="undeliverable-mail" v-model="customer.undeliverableMail">
              <label for="undeliverable-mail">Undeliverable Mail</label>
            </div>
            
            <div class="form-group checkbox-group">
              <input type="checkbox" id="bad-cell" v-model="customer.badCell">
              <label for="bad-cell">Bad Cell</label>
            </div>
            
            <div class="form-group checkbox-group">
              <input type="checkbox" id="bad-phone-2" v-model="customer.badPhone2">
              <label for="bad-phone-2">Bad Phone 2</label>
            </div>
            
            <div class="form-group checkbox-group">
              <input type="checkbox" id="bad-phone-3" v-model="customer.badPhone3">
              <label for="bad-phone-3">Bad Phone 3</label>
            </div>
            
            <div class="form-group checkbox-group">
              <input type="checkbox" id="bad-phone-4" v-model="customer.badPhone4">
              <label for="bad-phone-4">Bad Phone 4</label>
            </div>
            
            <div class="form-group checkbox-group">
              <input type="checkbox" id="undeliverable-email-1" v-model="customer.undeliverableEmail1">
              <label for="undeliverable-email-1">Undeliverable Email 1</label>
            </div>
            
            <div class="form-group checkbox-group">
              <input type="checkbox" id="undeliverable-email-2" v-model="customer.undeliverableEmail2">
              <label for="undeliverable-email-2">Undeliverable Email 2</label>
            </div>
          </div>
        </div>
        
        <!-- Form Actions -->
        <div class="form-actions">
          <button type="submit" class="primary-btn">
            <i class="fas fa-save"></i> Save Customer
          </button>
          <button type="button" @click="cancelEdit" class="secondary-btn">
            <i class="fas fa-times"></i> Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style>
/* Main Container Styles */
.add-customer-container {
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

.preferences-grid {
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
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

.input-field:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
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

/* Checkbox Groups */
.checkbox-group {
  display: flex;
  align-items: center;
  margin-bottom: 0;
}

.checkbox-group input[type="checkbox"] {
  margin-right: 8px;
}

.checkbox-group label {
  margin-bottom: 0;
  cursor: pointer;
}

/* Address Actions */
.address-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  grid-column: 1 / -1;
}

/* Disabled Section */
.disabled-section {
  opacity: 0.7;
  position: relative;
}

.disabled-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.5);
  z-index: 1;
  pointer-events: none;
  border-radius: 8px;
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

.action-btn {
  background-color: #f8f9fa;
  color: #495057;
  border: 1px solid #ddd;
}

.action-btn:hover {
  background-color: #e9ecef;
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
  .add-customer-container {
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