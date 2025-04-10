<script setup>
import { RouterView } from "vue-router";
import Navbar from './components/Navbar.vue';
</script>

<template>
  <div id="app-container">
    <Navbar />
    <RouterView />
  </div>
</template>

<style scoped>
#app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f0f0f0; /* Add background color for visibility */
}
</style>