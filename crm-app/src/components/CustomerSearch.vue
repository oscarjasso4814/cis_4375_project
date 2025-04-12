<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { url } from "../api/apiurl";

const router = useRouter();
const query = ref("");
const searchResults = ref([]);
const isSearching = ref(false);
const searchError = ref("");
const showResults = ref(false);

// Search by specific criteria
const searchBy = ref("name"); // Default to name search
const searchOptions = [
  { value: "name", label: "Name" },
  { value: "id", label: "Customer ID" },
  { value: "phone", label: "Phone Number" },
  { value: "email", label: "Email" }
];

// Search function - now sending the search type to backend
const searchCustomers = async () => {
  if (!query.value.trim()) {
    searchResults.value = [];
    searchError.value = "";
    showResults.value = false;
    return;
  }

  try {
    isSearching.value = true;
    searchError.value = "";
    showResults.value = false;
    
    // Send both query and type to the backend
    const res = await axios.get(url + "/api/customers/search", {
      params: { 
        query: query.value,
        type: searchBy.value 
      },
    });
    
    searchResults.value = res.data;
    showResults.value = true;
    
    // If only one result is found, navigate directly to that customer's profile
    if (searchResults.value.length === 1) {
      navigateToCustomerProfile(searchResults.value[0].id);
    }
    
  } catch (err) {
    console.error("Error searching customers:", err);
    searchError.value = "An error occurred while searching. Please try again.";
    searchResults.value = [];
  } finally {
    isSearching.value = false;
  }
};

// Navigate to customer profile
const navigateToCustomerProfile = (customerId) => {
  router.push({
    name: "CustomerProfile", 
    params: { id: customerId }
  });
};

// Add customer function
const navigateToAddCustomer = () => {
  router.push({ name: "AddCustomer" });
};

// get rep name from localStorage
const repName = ref("");

async function getRepName(repid) {
  if (!repid) {
    repName.value = "Agent";
    return;
  }
  
  try {
    const response = await axios.get(url + '/api/rep/' + repid + '/name');
    if (response.data && response.data[0]) {
      const representative = response.data[0].FirstName + " " + response.data[0].LastName;
      repName.value = representative;
    } else {
      repName.value = "Agent";
    }
  } catch (error) {
    console.error("Error fetching representative name:", error);
    repName.value = "Agent";
  }
}

onMounted(async () => {
  const repsId = localStorage.getItem("reps_id");
  console.log("Retrieved reps_id:", repsId);
  getRepName(repsId);
});
</script>

<template>
  <div class="search-container">
    <h1 class="search-title">Welcome, {{ repName }}</h1>
    <h2 class="search-title">Customer Search</h2>
    
    <!-- Search Form -->
    <div class="search-form">
      <div class="input-group">
        <!-- Search Criteria Dropdown -->
        <select v-model="searchBy" class="search-criteria">
          <option v-for="option in searchOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
        
        <!-- Search Input -->
        <input
          v-model="query"
          type="text"
          :placeholder="`Search by ${searchOptions.find(opt => opt.value === searchBy)?.label.toLowerCase()}...`"
          class="search-input"
          @keyup.enter="searchCustomers"
        />
        
        <!-- Search Button -->
        <button @click="searchCustomers" class="search-button">
          <i class="fas fa-search"></i> Search
        </button>
      </div>
      
      <button @click="navigateToAddCustomer" class="add-customer-button">
        <i class="fas fa-plus"></i> Add Customer
      </button>
    </div>
    
    <!-- Loading Indicator -->
    <div v-if="isSearching" class="loading-indicator">
      Searching...
    </div>
    
    <!-- Error Message -->
    <div v-if="searchError" class="error-message">
      {{ searchError }}
    </div>
    
    <!-- Search Results Table -->
    <div v-if="showResults && searchResults.length > 0" class="results-container">
      <h3 class="results-title">Search Results ({{ searchResults.length }})</h3>
      
      <table class="results-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Phone</th>
            <th>Email</th>
            <th>DOB</th>
            <th>Agent of Record</th>
            <th>Date Added</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="customer in searchResults" :key="customer.id" class="result-row">
            <td>{{ customer.id }}</td>
            <td>{{ customer.name }}</td>
            <td>{{ customer.phone }}</td>
            <td>{{ customer.email }}</td>
            <td>{{ customer.dob || 'N/A' }}</td>
            <td>{{ customer.agent || 'N/A' }}</td>
            <td>{{ customer.dateAdded || 'N/A' }}</td>
            <td>
              <button 
                @click="navigateToCustomerProfile(customer.id)" 
                class="view-profile-button"
              >
                View Profile
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- No Results Message -->
    <div v-if="showResults && searchResults.length === 0" class="no-results">
      No customers found matching "{{ query }}" in {{ searchOptions.find(opt => opt.value === searchBy)?.label.toLowerCase() }}. 
      <button @click="navigateToAddCustomer" class="add-link">
        Add a new customer?
      </button>
    </div>
  </div>
</template>

<style scoped>
.search-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.search-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

.search-form {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.input-group {
  display: flex;
  flex: 1;
}

.search-criteria {
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 6px 0 0 6px;
  font-size: 16px;
  color: #333;
  background-color: #f5f5f5;
  min-width: 140px;
  cursor: pointer;
}

.search-input {
  flex: 1;
  padding: 12px 15px;
  border: 2px solid #ddd;
  border-left: none;
  font-size: 16px;
  color: #333;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #007bff;
  outline: none;
}

.search-button {
  padding: 12px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 0 6px 6px 0;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #0069d9;
}

.add-customer-button {
  padding: 12px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.3s;
}

.add-customer-button:hover {
  background-color: #218838;
}

.loading-indicator {
  text-align: center;
  padding: 15px;
  font-style: italic;
  color: #666;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 10px 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.results-container {
  margin-top: 20px;
}

.results-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.results-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.results-table th,
.results-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.results-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #333;
}

.result-row:hover {
  background-color: #f5f5f5;
}

.view-profile-button {
  padding: 6px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.view-profile-button:hover {
  background-color: #0069d9;
}

.no-results {
  text-align: center;
  padding: 30px;
  color: #666;
  background-color: #f8f9fa;
  border-radius: 6px;
  font-size: 16px;
}

.add-link {
  background: none;
  border: none;
  color: #007bff;
  text-decoration: underline;
  cursor: pointer;
  font-size: 16px;
  margin-left: 5px;
}

.add-link:hover {
  color: #0056b3;
  text-decoration: none;
}

/* Responsive Design */
@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
    align-items: stretch;
  }
  
  .input-group {
    flex-direction: column;
  }
  
  .search-criteria {
    border-radius: 6px 6px 0 0;
    width: 100%;
  }
  
  .search-input {
    border-left: 2px solid #ddd;
    border-top: none;
    border-radius: 0;
  }
  
  .search-button {
    border-radius: 0 0 6px 6px;
  }
  
  .add-customer-button {
    margin-top: 10px;
    width: 100%;
  }
  
  .results-table {
    display: block;
    overflow-x: auto;
  }
}
</style>