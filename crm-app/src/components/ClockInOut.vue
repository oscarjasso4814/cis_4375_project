<script setup>
// Clock In / Clock Out Timer System

import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { user, totalWorkedTime } from '@/stores/userSession';

// Save the check-in timestamp
const saveCheckInTime = () => {
  sessionStorage.setItem('checkInTime', Date.now().toString());
};

// Load and resume timer
const loadCheckInTime = () => {
  const savedTime = sessionStorage.getItem('checkInTime');
  if (savedTime) {
    const elapsed = Math.floor((Date.now() - parseInt(savedTime)) / 1000);
    totalWorkedTime.value = elapsed;
    startTimer();
    isCheckedIn.value = true;
  }
};

// Timer Logic
const isCheckedIn = ref(false);       // Tracks if the user is checked in
let timerInterval = null;             // Holds the interval ID
const previousWorkedTime = ref('');      // Stores the last worked session time

// Start counting time
const startTimer = () => {
  timerInterval = setInterval(() => {
    totalWorkedTime.value++;
  }, 1000); // Every second, add 1 to the timer
};

// Stop counting time
const stopTimer = () => {
  clearInterval(timerInterval); // Stop the interval
  timerInterval = null;
};

// Format seconds into readable text (h m s)
const formatTime = (seconds) => {
  const hrs = Math.floor(seconds / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  return `${hrs}h ${mins}m ${secs}s`;
};

// When the user clicks the button
const handleCheck = () => {
  if (!isCheckedIn.value) {
    // Checking In
    saveCheckInTime();
    startTimer();
    isCheckedIn.value = true;
  } else {
    // Checking Out
    stopTimer();
    previousWorkedTime.value = formatTime(totalWorkedTime.value);
    isCheckedIn.value = false;
    sessionStorage.removeItem('checkInTime'); // Clear stored time
  }
};

// Computed live formatted timer
const formattedTime = computed(() => formatTime(totalWorkedTime.value));

// When the page loads
onMounted(() => {
  loadCheckInTime();
  // Starts the timer on login
  if (user && !isCheckedIn.value) {
    startTimer();
    isCheckedIn.value = true;
  }
});

// When the component unmounts
onBeforeUnmount(() => {
  if (timerInterval) {
    clearInterval(timerInterval);
  }
});
</script>

<template>
  <div class="overlay">
    <div class="sidebar-panel">
      <h2>Work Timer</h2>
      <button class="timer-btn" @click="handleCheck">
        {{ isCheckedIn ? 'Check Out' : 'Check In' }}
      </button>

      <!-- Shows live timer when checked in -->
      <div class="timer-display">
        Time Working: {{ formattedTime }}
      </div>

      <!-- Shows current session worked time after checking out -->
      <div v-if="!isCheckedIn" class="worked-time-log">
        Paused
      </div>
    </div>
  </div>
</template>


<style scoped>
/* Sidebar Panel */
.sidebar-panel {
  background-color: #f0f4ff; /* light blue background */
  border: 1px solid #80b3ff; /* soft blue border */
  border-radius: 8px;
  padding: 16px;
  margin-top: 16px;
  margin-bottom: 16px;
  margin-left: 10px;
  margin-right: 10px;
  min-width: 300px;
  text-align: center; /* CENTER everything inside */
}

/* Sidebar Title */
.sidebar-title {
  font-size: 1.5rem;
  color: #333; /* dark grey text */
  margin-bottom: 1rem;
  font-weight: bold;
}

/* Timer Button */
.timer-btn {
  background-color: #4A90E2; /* soft blue button */
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
  width: 100%;
}

.timer-btn:hover {
  background-color: #357ABD; /* darker blue on hover */
}

/* Timer Display */
.timer-display {
  font-size: 1.25rem;
  margin-top: 1rem;
  color: #333; /* dark text */
  font-weight: bold;
}

/* Worked Time Log */
.worked-time-log {
  font-size: 1rem;
  margin-top: 0.5rem;
  color: #666; /* medium grey */
}
</style>