<script setup>
import { ref } from "vue";
import axios from "axios";
import { url } from "../api/apiurl";
import { useRouter } from "vue-router";

const query = ref("");
const results = ref([]);
const hasSearched = ref(false);
const showResults = ref(false);
const router = useRouter();

const searchCustomers = async () => {
  if (!query.value.trim()) {
    results.value = [];
    hasSearched.value = false;
    showResults.value = false;
    return;
  }

  try {
    const res = await axios.get(url + "/api/customers/search", {
      params: { query: query.value },
    });
    results.value = res.data;
    hasSearched.value = true;

    if (results.value.length === 1) {
      // Navigate to the customer's profile if only one result is found
      selectCustomer(results.value[0]);
    } else {
      showResults.value = true; // Show results if multiple customers are found
    }
  } catch (err) {
    console.error("Error searching customers:", err);
    results.value = [];
    hasSearched.value = true;
    showResults.value = false;
  }
};

const selectCustomer = (customer) => {
  router.push({ name: "Ex_Cust", query: { id: customer.id } }); // Navigate to ViewCustomer with customer ID
};

const resetSearch = () => {
  query.value = "";
  results.value = [];
  hasSearched.value = false;
  showResults.value = false;
};
</script>

<template>
  <div class="search-center">
    <div class="search-box">
      <h2 class="search-heading">Search Customers</h2>

      <div v-if="!showResults">
        <input
          v-model="query"
          @keyup.enter="searchCustomers"
          type="text"
          placeholder="Enter a name..."
          class="search-input"
        />
        <p v-if="results.length === 0 && hasSearched" class="no-results">
          No matching customers found.
        </p>
      </div>

      <div v-else>
        <ul class="results-list">
          <li
            v-for="customer in results"
            :key="customer.id"
            @click="selectCustomer(customer)"
            class="result-item"
          >
            <div class="font-semibold">{{ customer.name }}</div>
            <div class="text-sm text-gray-600">
              ID: {{ customer.id }} | {{ customer.email }} | {{ customer.phone }}
            </div>
          </li>
        </ul>
        <button @click="resetSearch" class="back-button">Back</button>
      </div>
    </div>
  </div>
</template>

<style>
/* Base */
body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

.main-container {
  background-color: black;
  min-height: 100vh;
  position: relative;
  margin: 0;
  padding: 0;
}

/* Sidebar Buttons */
.cabutton,
.tasks-button {
  position: absolute;
  left: 0;
  width: 6rem;
  height: 4rem;
  background-color: #facc15;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  z-index: 10;
}

.cabutton {
  top: 80px;
}

.tasks-button {
  top: 160px;
}

.sidebuttons {
  text-align: center;
  font-weight: bold;
}

/* Centered Search Section */
.search-center {
  margin-left: 6rem;
  min-height: 100vh;
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
  background-color: #374151;
  color: #f3f4f6;
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
}

.dropdown-item {
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f3f4f6;
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
}

.add-customer-btn:hover {
  background-color: #fbbf24;
}

/* Overlay */
.overlay-container {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.75);
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.overlay-box {
  background-color: #1f2937;
  padding: 1.5rem;
  border-radius: 0.75rem;
  width: 100%;
  max-width: 32rem;
}

.overlay-heading {
  color: white;
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.close-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #facc15;
  color: black;
  font-weight: bold;
  border-radius: 0.375rem;
  transition: background-color 0.2s ease-in-out;
}

.close-btn:hover {
  background-color: #fbbf24;
}

/* Results List */
.results-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.result-item {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #ddd;
  transition: background-color 0.2s;
}

.result-item:hover {
  background-color: #f3f3f3;
}

.back-button {
  margin-top: 10px;
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: #0056b3;
}
</style>
