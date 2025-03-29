<template>
  <div>
    <!-- Navigation Bar -->
    <nav>
      <a href="#">Home</a>
      <a href="#profile">Profile</a>
      <a href="#tasks">Tasks</a>
      <a href="#settings">Settings</a>
    </nav>

    <!-- Add Customer -->
    <div class="add-customer">
      <h2>Customers</h2>
      <button class="add-customer-btn" @click="addCustomer">Add Customer</button>
    </div>

    <!-- Main Container -->
    <div class="container">
      <h1>Welcome, "EMPLOYEE NAME"</h1>

      <div class="video-section">
        <h2>Company Announcement</h2>
        <div class="video-container">
          <iframe src="https://www.youtube.com/embed/tMya2WkbQgM" allowfullscreen></iframe>
        </div>
      </div>

      <div class="profile">
        <h2>Your Profile</h2>
        <p>Name: John Doe</p>
        <p>Position: Insurance Agent</p>
      </div>

      <div class="tasks">
        <h2>Tasks</h2>
        <ul>
          <li>Complete project report</li>
          <li>Attend team meeting at 3 PM</li>
          <li>Review code updates</li>
        </ul>
      </div>

      <div class="settings">
        <h2>Settings</h2>
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
});

</script>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  text-align: center;
  background-color: #f4f4f4;
}

.container {
  max-width: 900px;
  margin: auto;
  padding: 20px;
  background: white;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-top: 50px;
}

nav {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 10px;
  background: #007bff;
}

nav a {
  color: white;
  text-decoration: none;
  font-size: 18px;
}

.profile,
.tasks,
.settings,
.video-section {
  margin-top: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
}

.profile h2,
.tasks h2,
.settings h2,
.video-section h2 {
  color: #333;
}

.video-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

iframe {
  width: 560px;
  height: 315px;
  border: none;
}

.add-customer {
  margin-top: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
}

.add-customer-btn {
  padding: 10px 20px;
  font-size: 16px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.add-customer-btn:hover {
  background: #218838;
}
</style>
