<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { url } from "../api/apiurl";
import { user, setUser, clearUser, totalWorkedTime } from "../stores/userSession";

const username = ref("");
const password = ref("");
const showPassword = ref(false);
const errorMessage = ref("");
const router = useRouter();

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const handleLogin = async () => {
  errorMessage.value = "";

  if (!username.value || !password.value) {
    errorMessage.value = "Username and password are required.";
    return;
  }

  try {
    await axios.post(`${url}/api/login`, {
      username: username.value,
      password: password.value,
    }).then((response) => {
      // Login successful
      alert(`Welcome ${response.data.user.username}`);
      setUser(response.data.user);
      console.log("Logged in user:", response.data.user);
      localStorage.setItem("reps_id", response.data.user.representative_id);
      console.log("User ID:", response.data.user.representative_id);
      router.push({ name: "home" });
    })} catch (err) {
    if (err.response?.status === 401) {
      errorMessage.value = "Invalid username or password.";
    } else {
      errorMessage.value = "Something went wrong. Please try again.";
      console.error(err);
    }
  }
};

// Andrews End

onMounted(async () => {
  if (totalWorkedTime.value) {
    const repsId = localStorage.getItem("reps_id");
    await axios.post(`${url}/api/WorkSession`, {
      RepresentativeID: repsId,
      TotalWorkedTime: totalWorkedTime.value
    });
  }
  clearUser();
});

//Old Test Code
//   if (username.value === 'admin' && password.value === 'password') {
//     alert('Login successful!')
//   } else {
//     errorMessage.value = 'Invalid username or password.'
//   }
// }
</script>

<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h2 class="title">Login</h2>

      <form @submit.prevent="handleLogin" class="login-form">
        <label for="username">Username</label>
        <input
          id="username"
          v-model="username"
          placeholder="Enter username"
          class="input"
          required
        />

        <label for="password">Password</label>
        <div class="input-password-wrapper">
          <input
            :type="showPassword ? 'text' : 'password'"
            id="password"
            v-model="password"
            placeholder="Enter password"
            class="input password-input"
            required
          />
          <button type="button" class="show-button" @click="togglePasswordVisibility">
            {{ showPassword ? "Hide" : "Show" }}
          </button>
        </div>

        <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

        <button type="submit" class="login-btn">Login</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-wrapper {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #181818;
  padding: 20px;
}

.login-card {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 360px;
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #000;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.input {
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  width: 100%;
  box-sizing: border-box;
}

.input:focus {
  border-color: #007bff;
  outline: none;
}

.input-password-wrapper {
  position: relative;
  width: 100%;
}

.password-input {
  padding-right: 70px; /* space for the show button */
}

.show-button {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: #007bff;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
}

.show-button:hover {
  color: #0056b3;
}

.login-btn {
  background: #007bff;
  color: white;
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

.login-btn:hover {
  background: #0056b3;
}

.error {
  color: red;
  font-size: 14px;
  text-align: center;
}

label {
  color: #000 !important; /* Force solid black text */
  font-weight: bold;
}
</style>
