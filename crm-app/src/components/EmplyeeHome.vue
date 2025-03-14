<template>
  <div class="container mx-auto p-4">
    <header class="text-center py-5">
      <h1 class="text-3xl font-bold">Employee Dashboard</h1>
    </header>

    <nav class="flex justify-center space-x-4 py-4 border-b bg-blue-500 text-white">
      <router-link class="hover:underline" to="/">Home</router-link>
      <router-link class="hover:underline" to="/profile">Profile</router-link>
      <router-link class="hover:underline" to="/tasks">Tasks</router-link>
      <router-link class="hover:underline" to="/settings">Settings</router-link>
    </nav>

    <main class="py-10">
      <section class="text-center mb-6">
        <h2 class="text-2xl font-semibold">Welcome, Employee!</h2>
        <p class="text-lg">Your dashboard provides access to your profile, tasks, and settings.</p>
      </section>

      <section class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-4 border rounded shadow">
          <h3 class="text-xl font-semibold">Your Profile</h3>
          <p>Name: John Doe</p>
          <p>Position: Software Engineer</p>
          <p>Department: IT</p>
        </div>
        <div class="p-4 border rounded shadow">
          <h3 class="text-xl font-semibold">Tasks</h3>
          <ul>
            <li>Complete project report</li>
            <li>Attend team meeting at 3 PM</li>
            <li>Review code updates</li>
          </ul>
        </div>
      </section>

      <section class="p-4 border rounded shadow mt-6">
        <h3 class="text-xl font-semibold">Settings</h3>
        <p>Update your password, notification preferences, and other settings.</p>
      </section>

      <section class="p-4 border rounded shadow mt-6 text-center">
        <h3 class="text-xl font-semibold">Company Introduction</h3>
        <div class="flex justify-center mt-4">
          <iframe
            width="560"
            height="315"
            src="https://www.youtube.com/embed/dQw4w9WgXcQ"
            allowfullscreen
          ></iframe>
        </div>
      </section>

      <section class="p-4 border rounded shadow mt-6 text-center">
        <h3 class="text-xl font-semibold">Customers</h3>
        <button
          @click="addCustomer"
          class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Add Customer
        </button>
      </section>
    </main>

    <footer class="text-center py-5 border-t">
      <p class="text-sm text-gray-600">&copy; 2025 Employee Dashboard. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
// import { ref } from "vue";

const addCustomer = () => {
  alert("Customer added!");
};
</script>

<style>
.container {
  max-width: 900px;
}
</style>
