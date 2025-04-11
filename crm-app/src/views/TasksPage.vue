<template>
  <div class="container">
    <h2 class="title">Tasks</h2>

    <!-- Task Table -->
    <table class="task-table">
      <thead>
        <tr>
          <th>Task ID</th>
          <th>Description</th>
          <th>Assigned To</th>
          <th>Customer</th>
          <th>Priority</th>
          <th>Status</th>
          <th>Due Date</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks" :key="task.id">
          <td>{{ task.id }}</td>
          <td>{{ task.description }}</td>
          <td>{{ getEmployeeName(task.assigned_to) }}</td>
          <td>({{ task.customer_id }}) {{ getCustomerName(task.customer_id) }}</td>
          <td :class="['priority', task.priority]">{{ task.priority }}</td>
          <td :class="{ 'completed': task.completed, 'pending': !task.completed }">{{ task.status }}</td>
          <td>{{ task.due_date }}</td>
          <td>
            <button @click="updateTask(task.id)" class="btn btn-update">
              {{ task.completed ? 'Mark as Pending' : 'Mark as Completed' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { url } from "../api/apiurl"

const tasks = ref([])

// Fetch tasks from your backend
const fetchTasks = async () => {
  try {
    const response = await axios.get(url + '/api/Task') // Adjust endpoint if needed
    tasks.value = response.data
  } catch (error) {
    console.error("Error fetching tasks:", error)
  }
}

// Toggle task completion status (optional)
const updateTask = async (taskId) => {
  try {
    await axios.put(url + `/api/Task/${TaskId}/toggle`)
    const task = tasks.value.find(t => t.id === taskId)
    if (task) {
      task.completed = !task.completed
      task.status = task.completed ? 'Completed' : 'Pending'
    }
  } catch (error) {
    console.error("Error updating task:", error)
  }
}

// Load data on mount
onMounted(fetchTasks)
</script>


<style scoped>
/* Keep the same styling for the table and layout */

.container {
  width: 90%;
  max-width: 800px;
  margin: auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #000;
  margin-bottom: 20px;
}

.task-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  font-size: 16px;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.task-table th,
.task-table td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: center;
  color: #000;
}

.priority {
  font-weight: bold;
}

.priority.High {
  color: red;
}

.priority.Medium {
  color: orange;
}

.priority.Low {
  color: green;
}

.btn {
  background: #007bff;
  color: white;
  font-size: 16px;
  padding: 10px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
  width: 100%;
}

.btn:hover {
  background: #0056b3;
}

.btn-update {
  background: #28a745;
}

.btn-update:hover {
  background: #218838;
}
</style>