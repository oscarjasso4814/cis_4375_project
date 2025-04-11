<script setup>
import { ref } from "vue";
import axios from "axios";
import { url } from "../api/apiurl";
import { RouterLink } from "vue-router";

// Search state
const query = ref("");
const results = ref([]);
const hasSearched = ref(false);
const showDropdown = ref(false);
const selectedCustomerId = ref(null);

// Search function
const searchCustomers = async () => {
  if (!query.value.trim()) {
    results.value = [];
    hasSearched.value = false;
    showDropdown.value = false;
    return;
  }

  try {
    const res = await axios.get(url + "/api/customers/search", {
      params: { query: query.value },
    });
    results.value = res.data;
    hasSearched.value = true;
    showDropdown.value = true;
  } catch (err) {
    console.error("Error searching customers:", err);
    results.value = [];
    hasSearched.value = true;
    showDropdown.value = false;
  }
};

// Handle selection
const selectCustomer = (customer) => {
  query.value = customer.name;
  selectedCustomerId.value = customer.id;
  showDropdown.value = false;
  console.log("Selected customer ID:", customer.id);
};

// Add customer logic
const addCustomer = () => {
  console.log("Add customer button clicked");
};
</script>

<template>
  <!-- Centered Search Area -->
  <div class="search-center">
    <div class="search-box">
      <h2 class="search-heading">Search Customers</h2>
      <div class="flex flex-col md:flex-row items-center gap-4">
        <!-- Input Box -->
        <div class="relative w-full">
          <input
            v-model="query"
            @input="searchCustomers"
            @focus="showDropdown = true"
            type="text"
            placeholder="Enter a name..."
            class="search-input"
          />
          <!-- Dropdown Results -->
          <ul
            v-if="showDropdown && results.length > 0"
            class="dropdown-menu"
          >
            <li
              v-for="customer in results"
              :key="customer.id"
              @click="selectCustomer(customer)"
              class="dropdown-item"
            >
              <div class="font-semibold">{{ customer.name }}</div>
              <div class="text-sm text-gray-600">
                ID: {{ customer.id }} | {{ customer.email }} | {{ customer.phone }}
              </div>
            </li>
          </ul>
          <p v-if="results.length === 0 && hasSearched" class="no-results">
            No matching customers found.
          </p>
        </div>
        <!-- Add Customer Button -->
        <RouterLink
          to="/AddCustomer"
          class="add-customer-btn"
        >
          + Add Customer
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Centered Search Section */
.search-center {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-box {
  width: 100%;
  max-width: 700px;
  padding: 2rem;
  text-align: center;
}

.search-heading {
  font-size: 1.25rem;
  font-weight: bold;
  color: rgb(0, 0, 0);
  margin-bottom: 1rem;
}

.search-input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  border: 2px solid #4b5563;
  background-color: #ffffff;
  color: #000000;
  font-size: 16px;
  outline: none;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #facc15;
  box-shadow: 0 0 0 2px rgba(250, 204, 21, 0.4);
}

.search-input::placeholder {
  color: #9ca3af;
}

.dropdown-menu {
  position: absolute;
  z-index: 10;
  margin-top: 0.25rem;
  width: 100%;
  background-color: white;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-height: 15rem;
  overflow-y: auto;
  list-style: none;
  padding: 0;
}

.dropdown-item {
  padding: 0.5rem 1rem;
  cursor: pointer;
  text-align: left;
}

.dropdown-item:hover {
  background-color: #f3f4f6;
}

.font-semibold {
  font-weight: 600;
}

.text-sm {
  font-size: 0.875rem;
}

.text-gray-600 {
  color: #4b5563;
}

.no-results {
  margin-top: 0.5rem;
  color: #9ca3af;
}

/* Add Customer Button */
.add-customer-btn {
  padding: 0.5rem 1.5rem;
  background-color: #facc15;
  color: black;
  font-weight: bold;
  border-radius: 0.375rem;
  text-decoration: none;
  transition: background-color 0.2s ease-in-out;
  display: inline-block;
  margin-top: 1rem;
}

.add-customer-btn:hover {
  background-color: #fbbf24;
}

/* Flexbox utilities */
.flex {
  display: flex;
}

.flex-col {
  flex-direction: column;
}

.items-center {
  align-items: center;
}

.gap-4 {
  gap: 1rem;
}

.relative {
  position: relative;
}

.w-full {
  width: 100%;
}

@media (min-width: 768px) {
  .md\:flex-row {
    flex-direction: row;
  }
}
</style>