<script setup>
import CustomerSearch from '../components/CustomerSearch.vue';
import AnnouncementOverlay from '../components/AnnouncementOverlay.vue';
import TaskOverlay from '../components/TaskOverlay.vue';
</script>

<template>
  <div class="home-container">
    <!-- Main Content Section -->
    <main class="main-content">
      <!-- Left Column -->
      <div class="left-column">
        <div class="box box-1">
          <AnnouncementOverlay />
        </div>
        <div class="box box-2">
          <TaskOverlay />
        </div>
      </div>
      <!-- Right Column -->
      <div class="right-column">
        <div class="box box-3">
          <CustomerSearch />
        </div>
      </div>
    </main>
    <!-- Footer Section -->
    <footer class="footer">
      <p>&copy; 2025 Lalani Insurance Agency. All rights reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f9f9f9;
  margin-top: 60px; /* Matches the navbar height */
  color: #000; /* Set default text color to black */
}

.main-content {
  display: flex;
  flex: 1;
  padding: 15px;
  gap: 15px; /* Increased gap for better spacing */
  overflow: hidden; /* Prevents overflow issues */
}

.left-column {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 15px; /* Increased gap for better spacing */
  overflow-y: auto; /* Makes the left column scrollable if content overflows */
}

.right-column {
  flex: 2;
  overflow-y: auto; /* Makes the right column scrollable if content overflows */
}

.box {
  background-color: white;
  padding: 0px; /* Reduced padding since components have their own padding */
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden; /* Ensures content stays within the box */
  word-wrap: break-word; /* Ensures long text wraps within the box */
  overflow-y: auto; /* Adds scrollbars if content overflows vertically */
  color: #000; /* Ensure text inside boxes is black */
}

.box-1 {
  flex: 1; /* Takes 1/3 of the vertical space */
  min-height: 150px; /* Ensures a minimum height for better visibility */
}

.box-2 {
  flex: 2; /* Takes 2/3 of the vertical space */
  min-height: 300px; /* Ensures a minimum height for better visibility */
}

.box-3 {
  height: 100%; /* Occupies the full height of the right column */
  min-height: 450px; /* Ensures a minimum height for better visibility */
}

.footer {
  text-align: center;
  padding: 15px; /* Increased padding for better spacing */
  background-color: #007bff;
  color: white;
  font-size: 14px; /* Slightly larger font for better readability */
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-content {
    flex-direction: column; /* Stacks columns vertically on smaller screens */
  }
  .left-column,
  .right-column {
    flex: none;
    width: 100%; /* Makes columns full-width on smaller screens */
  }
  .box {
    margin-bottom: 15px; /* Adds spacing between boxes */
  }
}
</style>