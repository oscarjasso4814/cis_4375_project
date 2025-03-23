<script setup>
import { ref, reactive } from 'vue'

const customer = reactive({
  type: '',
  fullName: '',
  name: '',
  name2: '',
  suffix: '',
  title: '',
  salutation: '',
  activeStatus: 'Active',
  country: 'United States',
  isUsaCitizen: false,
  address: '',
  zip: '',
  city: '',
  state: '',
  addressVerified: false,
  sameAddress: false,
  mailingCountry: 'United States',
  mailingAddress: '',
  mailingZip: '',
  mailingCity: '',
  mailingState: '',
  cell: '',
  phone2: '',
  phone3: '',
  phone4: '',
  driversLicense: '',
  dlState: '',
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

const hideCustomer = () => {
  // Implement hide customer logic
}

const verifyMailingAddress = () => {
  // Implement mailing address verification logic
}

const saveCustomer = () => {
  // Implement save customer logic
}

const cancelEdit = () => {
  // Implement cancel edit logic
}
</script>

<template>
    <div class="customer-edit-container">
      <h2>Add Customer</h2>
      <input type="checkbox" class="hide-button" @click="hideCustomer">Hide This Customer</input>
      
      <div class="form-row">
        <div class="form-group">
          <label for="customer-type">Customer Type</label>
          <select id="customer-type" v-model="customer.type">
            <option value="Personal Lines">Personal Lines</option>
            <option value="Commercial">Commercial</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="first-middle-last">First Middle Last</label>
          <input type="text" id="first-middle-last" v-model="customer.fullName">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="name">Name</label>
          <input type="text" id="name" v-model="customer.name">
        </div>
        
        <div class="form-group">
          <label for="name2">Name 2</label>
          <input type="text" id="name2" v-model="customer.name2">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="suffix">Suffix</label>
          <input type="text" id="suffix" v-model="customer.suffix">
        </div>
        
        <div class="form-group">
          <label for="title">Title</label>
          <input type="text" id="title" v-model="customer.title">
        </div>
        
        <div class="form-group">
          <label for="salutation">Salutation</label>
          <input type="text" id="salutation" v-model="customer.salutation">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="active-status">Active Status</label>
          <select id="active-status" v-model="customer.activeStatus">
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="country">Country</label>
          <select id="country" v-model="customer.country">
            <option value="United States">United States</option>
            <option value="Canada">Canada</option>
            <option value="Other">Other</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="is-usa-citizen">Is USA Citizen?</label>
          <div class="checkbox-group">
            <input type="checkbox" id="is-usa-citizen" v-model="customer.isUsaCitizen">
            <span>Yes</span>
          </div>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="address">Address</label>
          <input type="text" id="address" v-model="customer.address">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="zip">Zip:</label>
          <input type="text" id="zip" v-model="customer.zip">
        </div>
        
        <div class="form-group">
          <label for="city">City:</label>
          <input type="text" id="city" v-model="customer.city">
        </div>
        
        <div class="form-group">
          <label for="state">State:</label>
          <select id="state" v-model="customer.state">
            <option value="TX">TX</option>
            <option value="AL">AL</option>
            <option value="AK">AK</option>
            <!-- Add other states as needed -->
          </select>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <div class="checkbox-group">
            <input type="checkbox" id="address-verified" v-model="customer.addressVerified">
            <label for="address-verified">Address Verified</label>
          </div>
        </div>
        
        <div class="form-group">
          <div class="checkbox-group">
            <input type="checkbox" id="same-address" v-model="customer.sameAddress">
            <label for="same-address">Same Address</label>
          </div>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="mailing-country">Mailing Country</label>
          <select id="mailing-country" v-model="customer.mailingCountry">
            <option value="United States">United States</option>
            <option value="Canada">Canada</option>
            <option value="Other">Other</option>
          </select>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="mailing-address">Mailing Address</label>
          <input type="text" id="mailing-address" v-model="customer.mailingAddress">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="mailing-zip">Mailing Zip</label>
          <input type="text" id="mailing-zip" v-model="customer.mailingZip">
        </div>
        
        <div class="form-group">
          <label for="mailing-city">Mailing City</label>
          <input type="text" id="mailing-city" v-model="customer.mailingCity">
        </div>
        
        <div class="form-group">
          <label for="mailing-state">Mailing State</label>
          <select id="mailing-state" v-model="customer.mailingState">
            <option value="" disabled>-- SELECT STATE --</option>
            <option value="TX">TX</option>
            <option value="AL">AL</option>
            <option value="AK">AK</option>
            <!-- Add other states as needed -->
          </select>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <a href="#" class="verify-link" @click.prevent="verifyMailingAddress">Click here to verify the new mailing address</a>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="cell">Cell</label>
          <input type="tel" id="cell" v-model="customer.cell">
        </div>
        
        <div class="form-group">
          <label for="phone2">Phone 2</label>
          <input type="tel" id="phone2" v-model="customer.phone2">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="phone3">Phone 3</label>
          <input type="tel" id="phone3" v-model="customer.phone3">
        </div>
        
        <div class="form-group">
          <label for="phone4">Phone 4</label>
          <input type="tel" id="phone4" v-model="customer.phone4">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="drivers-license">Drivers License</label>
          <input type="text" id="drivers-license" v-model="customer.driversLicense">
        </div>
        
        <div class="form-group">
          <label for="dl-state">DL State</label>
          <select id="dl-state" v-model="customer.dlState">
            <option value="" disabled>Select a State</option>
            <option value="TX">TX</option>
            <option value="AL">AL</option>
            <option value="AK">AK</option>
            <!-- Add other states as needed -->
          </select>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="date-licensed">Date Licensed MM/DD/YYYY</label>
          <input type="text" id="date-licensed" v-model="customer.dateLicensed" placeholder="MM/DD/YYYY">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="dob">Date of Birth MM/DD/YYYY</label>
          <input type="text" id="dob" v-model="customer.dateOfBirth" placeholder="MM/DD/YYYY">
        </div>
        
        <div class="form-group">
          <label for="ssn">SSN/Tax ID</label>
          <input type="text" id="ssn" v-model="customer.ssn" placeholder="000000000">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="gender">Gender</label>
          <select id="gender" v-model="customer.gender">
            <option value=""></option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="marital-status">Marital Status</label>
          <select id="marital-status" v-model="customer.maritalStatus">
            <option value=""></option>
            <option value="Single">Single</option>
            <option value="Married">Married</option>
            <option value="Divorced">Divorced</option>
            <option value="Widowed">Widowed</option>
          </select>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="household-size">Household Size</label>
          <input type="text" id="household-size" v-model="customer.householdSize">
        </div>
        
        <div class="form-group">
          <label for="people-applying">How many people applying</label>
          <input type="text" id="people-applying" v-model="customer.peopleApplying">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="household-income">Household Income (Total)</label>
          <input type="text" id="household-income" v-model="customer.householdIncome">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="customer.email">
        </div>
        
        <div class="form-group">
          <label for="email2">Email 2</label>
          <input type="email" id="email2" v-model="customer.email2">
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="website">Website</label>
          <input type="url" id="website" v-model="customer.website" placeholder="https://">
        </div>
        
        <div class="form-group">
          <label for="preferred-contact">Preferred Contact</label>
          <select id="preferred-contact" v-model="customer.preferredContact">
            <option value="None">None</option>
            <option value="Email">Email</option>
            <option value="Phone">Phone</option>
            <option value="Text">Text</option>
            <option value="Mail">Mail</option>
          </select>
        </div>
      </div>
      
      <div class="form-row">
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
      </div>
      
      <div class="form-row">
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
      </div>
      
      <div class="form-row">
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
      </div>
      
      <div class="form-row">
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
      </div>
      
      <div class="form-row">
      <div class="form-group checkbox-group">
        <input type="checkbox" id="undeliverable-email-2" v-model="customer.undeliverableEmail2">
        <label for="undeliverable-email-2">Undeliverable Email 2</label>
      </div>
    </div>

    <div class="form-actions">
      <button @click="saveCustomer" class="save-button">Save Changes</button>
      <button @click="cancelEdit" class="cancel-button">Cancel</button>
    </div>
  </div>
</template>


<style scoped>
.customer-edit-container {
  width: 100%;
  max-width: 800px;
  margin: 40px; /* Centers the container horizontally */
  padding: 20px;
  /* Remove any alignment that might be pushing it to the right */
  float: none;
  position: static;
}

/* This targets the parent container if there's one wrapping your form */
body, main, #app, .content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center; /* Centers child elements horizontally */
  width: 100%;
}

/* Make sure any parent containers don't have padding that's offsetting the centering */
body, #app, main, .content-wrapper {
  padding-left: 0;
  padding-right: 0;
}

/* Ensure all form rows are centered */
.form-row {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 15px;
  width: 100%;
  justify-content: center; /* Center the form rows */
}

/* Make form elements consistent width */
.form-group {
  flex: 1;
  margin-right: 15px;
  max-width: 100%; /* Prevent overflow */
}

.form-group:last-child {
  margin-right: 0;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="tel"],
input[type="email"],
input[type="url"],
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.checkbox-group {
  display: flex;
  align-items: center;
}

.checkbox-group input[type="checkbox"] {
  margin-right: 5px;
}

.form-actions {
  margin-top: 20px;
  text-align: right;
}

.save-button,
.cancel-button {
  padding: 10px 20px;
  margin-left: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-button {
  background-color: #4CAF50;
  color: white;
}

.cancel-button {
  background-color: #f44336;
  color: white;
}

.hide-button {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
}

.verify-link {
  color: #2196F3;
  text-decoration: none;
}

.verify-link:hover {
  text-decoration: underline;
}
</style>