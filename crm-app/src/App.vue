<script setup>
import { RouterLink, RouterView, useRouter } from "vue-router";
import HelloWorld from "./components/HelloWorld.vue";
import { ref, onMounted } from "vue";
import { user, clearUser } from "./stores/userSession";
import Navbar from './components/Navbar.vue';

const router = useRouter();
const isLoggedIn = ref(false);
const username = ref("");

// Check login status on mount
onMounted(() => {
  const userData = sessionStorage.getItem("user");
  if (userData) {
    const user = JSON.parse(userData);
    isLoggedIn.value = true;
    username.value = user.username;
  }
});

const handleLogout = () => {
  clearUser();
  router.push("/login");
};
</script>

<template>
  <div id="app-container">
    <Navbar />
    <RouterView />
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100%;
  background-color: #f0f0f0; /* Add background color for visibility */
}
</style>
