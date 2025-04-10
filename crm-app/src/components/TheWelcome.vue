<script setup>
import { ref } from "vue";
import axios from "axios";
import { url } from "../api/apiurl";

// State for managing overlays
const showAnnouncementOverlay = ref(false);
const showTasksOverlay = ref(false);

// State for search query and results
const query = ref("");
const results = ref([]);
const hasSearched = ref(false);
const showDropdown = ref(false);
const selectedCustomerId = ref(null);

// Toggle functions for overlays
const toggleAnnouncements = () => {
  showAnnouncementOverlay.value = !showAnnouncementOverlay.value;
  if (showAnnouncementOverlay.value) {
    showTasksOverlay.value = false;
  }
};

const toggleTasks = () => {
  showTasksOverlay.value = !showTasksOverlay.value;
  if (showTasksOverlay.value) {
    showAnnouncementOverlay.value = false;
  }
};

// Dummy data for company announcements
const announcements = [
  {
    title: "Company Announcement",
    videoUrl: "https://www.youtube.com/embed/tMya2WkbQgM",
  },
];

// Dummy data for tasks
const tasks = ["Complete project report", "Attend team meeting at 3 PM", "Review code updates"];

//ANDREWS Script Start
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
// Function to handle customer selection
// Stores ID of selected customer in a variable
// and closes the dropdown
const selectCustomer = (customer) => {
  query.value = customer.name;
  selectedCustomerId.value = customer.id;
  showDropdown.value = false;
  console.log("Selected customer ID:", customer.id);
};

//ANDREWS Script End

// Add customer functionality
const addCustomer = () => {
  console.log("Add customer button clicked");
  // Implement customer addition logic here
};
</script>

<template>
  <main class="bg-black min-h-screen relative">
    <!-- Side navigation container - absolute positioning with buttons stacked vertically -->
    <div class>
      <!-- First yellow box button - positioned higher on the page -->
      <button
        @click="toggleAnnouncements"
        class="cabutton"
        :class="{ 'bg-yellow-500': showAnnouncementOverlay }"
      >
        <span class="sidebuttons">Company Announcement</span>
      </button>

      <!-- Second yellow box button - positioned directly below first button -->
      <button
        @click="toggleTasks"
        class="tasks-button"
        :class="{ 'bg-yellow-500': showTasksOverlay }"
      >
        <span class="sidebuttons">Task</span>
      </button>
    </div>

    <!-- Main content area with margin to account for the sidebar -->
    <div class="ml-16 p-4 flex flex-col items-center justify-center min-h-screen">
      <!-- Customer search section -->
      <div class="w-full max-w-3xl text-center">
        <div class="flex space-x-4">
          <!-- Andrews START-->
          <div class="relative max-w-xl w-full mx-auto p-4">
            <h2 class="text-xl font-bold text-white mb-4">Search Customers</h2>

            <input
              v-model="query"
              @input="searchCustomers"
              @focus="showDropdown = true"
              type="text"
              placeholder="Enter a name..."
              class="w-full px-3 py-2 rounded text-black"
            />

            <!-- Dropdown menu -->
            <ul
              v-if="showDropdown && results.length > 0"
              class="absolute z-10 mt-1 w-full bg-white border border-gray-300 rounded shadow max-h-60 overflow-y-auto"
            >
              <li
                v-for="customer in results"
                :key="customer.id"
                @click="selectCustomer(customer)"
                class="px-4 py-2 cursor-pointer hover:bg-gray-100"
              >
                <div class="font-semibold">{{ customer.name }}</div>
                <div class="text-sm text-gray-600">
                  ID: {{ customer.id }} | {{ customer.email }} | {{ customer.phone }}
                </div>
              </li>
            </ul>

            <p v-if="results.length === 0 && hasSearched" class="text-gray-400 mt-2">
              No matching customers found.
            </p>
          </div>

          <!-- Andrews END-->

          <!-- Add Customer Button -->
          <button
            @click="addCustomer"
            class="px-6 py-2 bg-yellow-400 text-black font-bold rounded hover:bg-yellow-500 flex items-center transition duration-150 ease-in-out"
          >
            <RouterLink to="/AddCustomer">+ Add Customer</RouterLink>
          </button>
        </div>
      </div>
    </div>

    <!-- Overlay for announcements (if needed) -->
    <div
      v-if="showAnnouncementOverlay"
      class="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-4"
    >
      <div class="bg-gray-800 p-6 rounded-lg max-w-2xl w-full">
        <h2 class="text-white text-xl font-bold mb-4">Company Announcement</h2>
        <div class="aspect-video w-full">
          <iframe
            width="100%"
            height="100%"
            src="https://www.youtube.com/embed/tMya2WkbQgM"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
        </div>
        <button
          @click="toggleAnnouncements"
          class="mt-4 px-4 py-2 bg-yellow-400 text-black font-bold rounded hover:bg-yellow-500"
        >
          Close
        </button>
      </div>
    </div>

    <!-- Overlay for tasks (if needed) -->
    <div
      v-if="showTasksOverlay"
      class="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-4"
    >
      <div class="bg-gray-800 p-6 rounded-lg max-w-md w-full">
        <h2 class="text-white text-xl font-bold mb-4">Tasks</h2>
        <ul class="text-white space-y-2">
          <li v-for="(task, index) in tasks" :key="index" class="flex items-start">
            <span class="mr-2">•</span>
            <span>{{ task }}</span>
          </li>
        </ul>
        <button
          @click="toggleTasks"
          class="mt-4 px-4 py-2 bg-yellow-400 text-black font-bold rounded hover:bg-yellow-500"
        >
          Close
        </button>
      </div>
    </div>
  </main>
</template>

<style>
/* Global CSS */
body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

/* Remove any spacing that might affect the positioning */
main {
  padding: 0;
  margin: 0;
}

/* Search styles from CodePen example */
.search-container {
  position: relative;
  width: 100%;
}

.search-icon {
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  fill: #9ca3af; /* gray-400 */
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 10px 10px 10px 40px;
  font-size: 16px;
  color: #f3f4f6; /* gray-100 */
  background-color: #374151; /* gray-700 */
  border: 2px solid #4b5563; /* gray-600 */
  border-radius: 6px;
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #facc15; /* yellow-400 */
  box-shadow: 0 0 0 2px rgba(250, 204, 21, 0.4);
}

.search-input::placeholder {
  color: #9ca3af; /* gray-400 */
}

/* Fixed positioning for the cabutton class - moved higher on page */
.cabutton {
  position: absolute;
  top: 80px; /* Moved higher from the top */
  left: 0;
  width: 6rem;
  height: 4rem;
  background-color: #facc15; /* yellow-400 equivalent */
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  z-index: 10;
}

/* Style for the tasks button - positioned directly below the cabutton */
.tasks-button {
  position: absolute;
  top: 160px; /* 20px (top of first button) + 4rem (height of first button) */
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

.sidebuttons {
  align-items: center;
}
</style>
