<script setup>
import AnnouncementOverlay from '../components/AnnouncementOverlay.vue';
import CustomerSearch from '../components/CustomerSearch.vue';
import TaskOverlay from '../components/TaskOverlay.vue';
import AddCustomerNotes from '../components/AddCustomerNotes.vue';
import AddAgentNotes from '@/components/AddAgentNotes.vue';
import ClockInOut from '../components/ClockInOut.vue';

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
        <div class="box box-4">
          <AddCustomerNotes />
        </div>
        <div class="box box-4">
          <ClockInOut />
        </div>
      </div>
      <!-- Right Column -->
      <div class="right-column">
        <div class="box box-3">
          <CustomerSearch />
          <AddAgentNotes />
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

/* Tasks Preview Styles */
.tasks-preview {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 15px;
}

.tasks-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.tasks-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.view-all-btn {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background-color 0.2s;
}

.view-all-btn:hover {
  background-color: #0056b3;
}

.tasks-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.tasks-table th,
.tasks-table td {
  padding: 8px 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.tasks-table th {
  font-weight: 600;
  color: #555;
  background-color: #f5f5f5;
}

.description-cell {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.priority-cell {
  font-weight: 600;
}

.priority-cell.high {
  color: #dc3545;
}

.priority-cell.medium {
  color: #fd7e14;
}

.priority-cell.low {
  color: #28a745;
}

.status-cell.completed {
  color: #28a745;
}

.status-cell.pending {
  color: #6c757d;
}

.task-row:hover {
  background-color: #f8f9fa;
}

.loading-message,
.no-tasks {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #6c757d;
}

.no-tasks button {
  margin-top: 10px;
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