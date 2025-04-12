<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { url } from "../api/apiurl";

const router = useRouter();
const tasks = ref([]);
const isLoading = ref(true);

// Fetch a limited number of tasks for the homepage
const fetchTasks = async () => {
  try {
    isLoading.value = true;
    const response = await axios.get(url + '/api/tasks');
    
    // Limit to 5 most recent tasks for the homepage view
    tasks.value = response.data
      .sort((a, b) => new Date(b.DateCreated) - new Date(a.DateCreated))
      .slice(0, 5)
      .map(task => ({
        id: task.TaskID,
        description: task.TaskDescription,
        assigned_to: `${task.AssignedFirstName || ''} ${task.AssignedLastName || ''}`.trim(),
        customer_name: `${task.CustomerFirstName || ''} ${task.CustomerLastName || ''}`.trim(),
        priority: task.TaskPriority,
        status: task.TaskStatus,
        due_date: task.TaskDueDate,
        time: task.TaskTime
      }));
  } catch (error) {
    console.error('Error fetching tasks:', error);
  } finally {
    isLoading.value = false;
  }
};

// Navigate to the full tasks page
const viewAllTasks = () => {
  router.push('/TaskPage');
};

// Call the fetch task function when the component mounts
onMounted(() => {
  fetchTasks();
});
</script>

<template>
  <div class="tasks-preview">
            <div class="tasks-header">
              <h3>Recent Tasks</h3>
              <button @click="viewAllTasks" class="view-all-btn">
                <i class="fas fa-list"></i> View All Tasks
              </button>
            </div>
            
            <div v-if="isLoading" class="loading-message">
              Loading tasks...
            </div>
            
            <div v-else-if="tasks.length === 0" class="no-tasks">
              <p>No pending tasks found.</p>
              <button @click="viewAllTasks" class="view-all-btn">View Task Manager</button>
            </div>
            
            <div v-else class="tasks-list">
              <table class="tasks-table">
                <thead>
                  <tr>
                    <th>Description</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>Due Date</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="task in tasks" :key="task.id" class="task-row">
                    <td class="description-cell">{{ task.description }}</td>
                    <td :class="['priority-cell', task.priority.toLowerCase()]">{{ task.priority }}</td>
                    <td :class="['status-cell', task.status === 'Completed' ? 'completed' : 'pending']">
                      {{ task.status }}
                    </td>
                    <td class="date-cell">{{ task.due_date }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
</template>

<style scoped>
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
</style>
