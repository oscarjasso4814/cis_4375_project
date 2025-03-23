<template>
  <div class="bg-[#f4f4f4] min-h-screen py-10">
    <!-- Navigation Bar -->
    <nav class="flex justify-center gap-6 py-4 bg-[#007bff] text-white text-lg">
      <router-link class="hover:underline" to="/">Home</router-link>
      <router-link class="hover:underline" to="/profile">Profile</router-link>
      <router-link class="hover:underline" to="/tasks">Tasks</router-link>
      <router-link class="hover:underline" to="/settings">Settings</router-link>
    </nav>

    <!-- Add Customer (Top Section) -->
    <div class="max-w-[900px] mx-auto mt-8 p-6 bg-white rounded shadow">
      <h2 class="text-2xl font-semibold text-center">Customers</h2>
      <div class="text-center mt-4">
        <button
          @click="addCustomer"
          class="px-5 py-2 text-lg bg-green-600 text-white rounded hover:bg-green-700"
        >
          Add Customer
        </button>
      </div>
    </div>

    <!-- Main Container -->
    <div class="max-w-[900px] mx-auto mt-8 p-6 bg-white rounded shadow">
      <h1 class="text-3xl font-bold text-center">Welcome, {{ repName }}</h1>
      <!-- Video Section -->
      <div class="mt-10 p-4 border rounded bg-white shadow">
        <h2 class="text-xl font-semibold">Company Announcement</h2>
        <div class="flex justify-center mt-4">
          <iframe
            width="560"
            height="315"
            src="https://www.youtube.com/embed/tMya2WkbQgM"
            allowfullscreen
          ></iframe>
        </div>
      </div>

      <!-- Profile -->
      <div class="profile mt-8 p-4 border rounded bg-white shadow">
        <h2 class="text-xl font-semibold">Your Profile</h2>
        <p>Name: {{ repName }}</p>
        <p>Position: Insurance Agent</p>
      </div>

      <!-- Tasks -->
      <div class="tasks mt-8 p-4 border rounded bg-white shadow">
        <h2 class="text-xl font-semibold">Tasks</h2>
        <ul class="list-disc list-inside mt-2 text-left">
          <li>Complete project report</li>
          <li>Attend team meeting at 3 PM</li>
          <li>Review code updates</li>
        </ul>
      </div>

      <!-- Settings -->
      <div class="settings mt-8 p-4 border rounded bg-white shadow">
        <h2 class="text-xl font-semibold">Settings</h2>
        <p>Update your password, notification preferences, and other settings.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from "axios";

const repName = ref("")

const addCustomer = () => {
  alert("Customer added!");
};

// function to get the representative's name
async function getRepName(repid) {
  axios.get('http://127.0.0.1:5000/api/rep/' + repid + '/name')
  .then((response) => {
    let representative = response.data[0].FirstName + " " + response.data[0].LastName
    repName.value = representative;
  });
}

onMounted(async () => {
  // TODO: Needs to be passed a prop for which representative to load.
  getRepName(1);
  console.log(repName.value)
});

</script>

<style>
/* Optional global font fallback if you're not using Tailwind's font classes */
body {
  font-family: Arial, sans-serif;
}
</style>
