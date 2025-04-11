<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from "axios";
import { url } from "../api/apiurl";

const customer = reactive({
  name: 'John Doe',
  cell: '(555) 123-4567',
  phone2: '(555) 987-6543',
  email: 'john.doe@example.com',
  email2: 'johndoe@workmail.com',
  address: {
    street: '123 Main St',
    city: 'Springfield',
    state: 'IL',
    zip: '62701',
  },
  mailingAddress: 'PO Box 456, Springfield, IL 62702',
});

const householdMembers = reactive([
  { name: 'Main Member', dob: '01/01/1980', ssn: '***-**-1234', gender: 'Male', relationship: 'Self', expanded: false },
  { name: '2nd Member', dob: '02/02/1990', ssn: '***-**-5678', gender: 'Female', relationship: 'Spouse', expanded: false },
  { name: '3rd Member', dob: '03/03/2010', ssn: '0987-11-9012', gender: 'Male', relationship: 'Child', expanded: false },
]);

const insuranceTypes = [
  { label: 'Life', value: 'LIFE' },
  { label: 'Health', value: 'HEALTH' },
  { label: 'Medicare', value: 'MEDICARE' },
  { label: 'Home', value: 'HOME' },
  { label: 'Auto', value: 'AUTO' },
  { label: 'Others', value: 'OTHERS' },
];

const activeInsuranceType = ref('LIFE');

const policies = reactive([
  {
    id: 1,
    companyName: 'ABC Insurance',
    type: 'Life',
    planName: 'Term Life Plan',
    memberId: '12345',
    dateAdded: '2023-01-01',
    effectiveDate: '2023-02-01',
    expirationDate: '2024-01-31',
    premium: '$100/month',
    agent: 'John Agent',
    csr: 'Jane CSR',
  },
]);

const attachments = reactive([
  { id: 1, name: 'Policy Document', link: '#', description: 'Life Insurance Policy Document' },
]);

const getPolicies = (type) => {
  return policies.filter((policy) => policy.type.toUpperCase() === type);
};

const toggleMemberDetails = (index) => {
  householdMembers[index].expanded = !householdMembers[index].expanded;
};

let isResizing = false;
let startY = 0;
let startHeightPolicy = 0;
let startHeightNotes = 0;

const startResizing = (event) => {
  isResizing = true;
  startY = event.clientY;
  const policyDisplay = document.querySelector('.policy-display');
  const notesAttachments = document.querySelector('.notes-attachments');
  startHeightPolicy = policyDisplay.offsetHeight;
  startHeightNotes = notesAttachments.offsetHeight;

  document.addEventListener('mousemove', resizeSections);
  document.addEventListener('mouseup', stopResizing);
};

const resizeSections = (event) => {
  if (!isResizing) return;

  const deltaY = event.clientY - startY;
  const policyDisplay = document.querySelector('.policy-display');
  const notesAttachments = document.querySelector('.notes-attachments');

  policyDisplay.style.height = `${startHeightPolicy + deltaY}px`;
  notesAttachments.style.height = `${startHeightNotes - deltaY}px`;
};

const stopResizing = () => {
  isResizing = false;
  document.removeEventListener('mousemove', resizeSections);
  document.removeEventListener('mouseup', stopResizing);
};

// Function to fetch and update customer information
// Generated using ChatGPT:
// Create a function following this initial layout (getCustomer() in ViewCustomer.vue)
// but with series of customer.key = customerData.value statements similar to customer.name using the keys from this reactive const (customer in ViewCustomer.vue)
// and this MySQL table's keys (Customer CREATE TABLE from Create_Database_and_Tables.sql)
async function getCustomer(custid) {
  axios.get(url + `/api/customer/${custid}`)
    .then((response) => {
      const customerData = response.data[0];

      if (customerData) {
        customer.name = customerData.FirstName + " " + customerData.LastName || '';
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
      }
      else {
          throw new Error ("No customer data returned");
      }
    })
    .catch((error) => {
      console.error('Error fetching customer data:', error);
    });
}

// Lifecycle hook
onMounted(async () => {
  console.log('Updated customer profile component mounted');
  // TODO: Update input to a passed prop when page is loaded
  // getCustomer(2) returns the default values
  getCustomer(1);
  // getCustomer(3) tests if error catch works (check console)
  //getCustomer(3);
  // DO NOT run both at the same time; will crash flask
});
</script>

<template>
  <div class="view-customer-container">
    <!-- Left Panel -->
    <aside class="left-panel">
      <header class="panel-header">
        <h3>Contact</h3>
        <button class="edit-btn">Edit</button>
      </header>
      <div class="contact-info">
        <p><strong>Name:</strong> {{ customer.name }}</p>
        <span class="customer-id">ID: {{ customer.id }}</span>
        <p><strong>Phone 1:</strong> {{ customer.cell }}</p>
        <p><strong>Phone 2:</strong> {{ customer.phone2 }}</p>
        <p><strong>Email 1:</strong> {{ customer.email }}</p>
        <p><strong>Email 2:</strong> {{ customer.email2 }}</p>
        <p><strong>Physical Address:</strong> {{ customer.address.street }}, {{ customer.address.city }}, {{ customer.address.state }} {{ customer.address.zip }}</p>
        <p><strong>Mailing Address:</strong> {{ customer.mailingAddress }}</p>
      </div>
      <div class="household-members">
        <h4>Household Members</h4>
        <ul>
          <li v-for="(member, index) in householdMembers" :key="index">
            <button @click="toggleMemberDetails(index)">
              {{ member.name }}
              <span v-if="member.expanded">▲</span>
              <span v-else>▼</span>
            </button>
            <div v-if="member.expanded" class="member-details">
              <p><strong>DOB:</strong> {{ member.dob }}</p>
              <p><strong>SSN:</strong> {{ member.ssn }}</p>
              <p><strong>Gender:</strong> {{ member.gender }}</p>
              <p><strong>Relationship:</strong> {{ member.relationship }}</p>
            </div>
          </li>
        </ul>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <!-- LOB Buttons -->
      <div class="lob-tabs">
        <button
          v-for="type in insuranceTypes"
          :key="type.value"
          class="tab-btn"
          :class="{ active: activeInsuranceType === type.value }"
          @click="activeInsuranceType = type.value"
        >
          {{ type.label }}
        </button>
      </div>

      <!-- Resizable Sections -->
      <div class="resizable-container">
        <!-- Policy Display Area -->
        <div class="policy-display resizable-section">
          <div class="policy-content">
            <h3>{{ activeInsuranceType }} Policies</h3>
            <table class="policy-table">
              <thead>
                <tr>
                  <th>Company Name</th>
                  <th>Type</th>
                  <th>Plan Name</th>
                  <th>Member ID</th>
                  <th>Date Added</th>
                  <th>Effective Date</th>
                  <th>Expiration Date</th>
                  <th>Premium</th>
                  <th>Agent</th>
                  <th>CSR</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="policy in getPolicies(activeInsuranceType)" :key="policy.id">
                  <td>{{ policy.companyName }}</td>
                  <td>{{ policy.type }}</td>
                  <td>{{ policy.planName }}</td>
                  <td>{{ policy.memberId }}</td>
                  <td>{{ policy.dateAdded }}</td>
                  <td>{{ policy.effectiveDate }}</td>
                  <td>{{ policy.expirationDate }}</td>
                  <td>{{ policy.premium }}</td>
                  <td>{{ policy.agent }}</td>
                  <td>{{ policy.csr }}</td>
                  <td>
                    <button class="action-btn">Rewrite</button>
                    <button class="action-btn">Renew</button>
                    <button class="action-btn">Cancel</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="resizer" @mousedown="startResizing"></div>
        <!-- Notes & Attachments Section -->
        <div class="notes-attachments resizable-section">
          <h3>Notes & Attachments</h3>
          <textarea placeholder="Add a note..."></textarea>
          <button class="add-note-btn">Add Note</button>
          <div class="attachments">
            <h4>Attachments</h4>
            <ul>
              <li v-for="attachment in attachments" :key="attachment.id">
                <a :href="attachment.link" target="_blank">{{ attachment.name }}</a>
                <p>{{ attachment.description }}</p>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </main>

    <!-- Right Sidebar -->
    <aside class="right-sidebar">
      <h3>Actions</h3>
      <button class="action-btn">Add Policy</button>
      <button class="action-btn">Add Task</button>
      <button class="action-btn">Custom Form 1</button>
      <button class="action-btn">Custom Form 2</button>
      <p class="note">Will add policies into the LOB showing</p>
    </aside>
  </div>
</template>

<style scoped>
.view-customer-container {
  display: flex;
  flex-direction: row;
  gap: 20px;
  padding: 20px;
  background-color: #f4f6f8;
  margin: 0;
  height: calc(100vh - 60px); /* Subtract navbar height */
  margin-top: 60px; /* Push content below the navbar */
  box-sizing: border-box;
  color: #333;
}

.left-panel {
  max-width: 30%;
  flex: 1;
  background-color: #ffffff;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  color: #333;
}


.right-sidebar {
  max-width: 13%;
  flex: 1;
  background-color: #ffffff;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  color: #333;
}

.main-content {
  flex: 3;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.lob-tabs {
  display: flex;
  gap: 10px; /* Add spacing between buttons */
  margin-bottom: 0px; /* Add space below the buttons */
}

.tab-btn {
  flex: 1; /* Make buttons equally wide */
  padding: 7px; /* Adjust padding to make buttons square */
  margin: 0 10px; /* Add left and right margins */
  border: none;
  background-color: #e9ecef;
  border-radius: 0; /* Remove rounding for square buttons */
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
  text-align: center; /* Center text inside the button */
}

.tab-btn.active {
  background-color: #007bff;
  color: white;
}

.tab-btn:hover {
  background-color: #0056b3;
  color: white;
}

.resizable-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
  border: 1px solid #ddd; /* Add border around the container */
  border-radius: 10px; /* Rounded corners for the container */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  background-color: #ffffff; /* White background for the container */
}

.resizable-section {
  overflow-y: auto;
  resize: none; /* Prevent native resizing */
  padding: 15px; /* Add padding inside the sections */
}

.policy-display {
  height: 50%; /* Initial height */
  transition: height 0.2s ease; /* Smooth resizing */
  border-bottom: 1px solid #ddd; /* Divider between sections */
  position: relative; /* Ensure tabs are positioned correctly */
}

.policy-content {
  margin-top: 0; /* Remove space for tabs */
  overflow-y: auto;
  padding: 15px;
}

.notes-attachments {
  height: 50%; /* Initial height */
  transition: height 0.2s ease; /* Smooth resizing */
}

.resizer {
  height: 5px;
  background-color: #ccc;
  cursor: row-resize;
  transition: background-color 0.2s;
}

.resizer:hover {
  background-color: #999;
}

.policy-table {
  width: 100%;
  border-collapse: collapse;
  word-wrap: break-word;
}

.policy-table th,
.policy-table td {
  border: 1px solid #e0e0e0;
  padding: 10px;
  text-align: left;
  color: #333;
}

.policy-table th {
  background-color: #f8f9fa;
  font-weight: bold;
}

.household-members ul {
  max-height: 200px;
  overflow-y: auto;
}

.household-members button {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  font-size: 14px;
  transition: color 0.3s;
}

.household-members button:hover {
  color: #0056b3;
}

.action-btn {
  display: block;
  width: 100%;
  padding: 12px;
  margin-bottom: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.3s;
}

.action-btn:hover {
  background-color: #0056b3;
}

.note {
  color: red;
  font-size: 12px;
  margin-top: 10px;
}

textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  resize: none;
  font-size: 14px;
}

textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.add-note-btn {
  margin-top: 10px;
  padding: 10px 15px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-note-btn:hover {
  background-color: #218838;
}

.attachments a {
  color: #007bff;
  text-decoration: none;
  transition: color 0.3s;
}

.attachments a:hover {
  color: #0056b3;
}
</style>