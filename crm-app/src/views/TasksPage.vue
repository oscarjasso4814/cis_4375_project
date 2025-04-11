<template>
  <div class="container">
    <h2 class="title">Tasks</h2>

    <table class="task-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Description</th>
          <th>Assigned To:</th>
          <th>Customer</th>
          <th>Created By:</th>
          <th>Priority</th>
          <th>Status</th>
          <th>Due</th>
          <th>Time Created</th>
          <th>Review Required</th>
          <th colspan="2">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks" :key="task.id">
          <td>{{ task.id }}</td>
          <td class="wrap-cell">{{ task.description }}</td>
          <td class="wrap-cell">{{ task.assigned_to }}</td>
          <td class="wrap-cell">({{ task.customer_id }}) {{ task.customer_name }}</td>
          <td>{{ task.created_by }}</td>
          <td :class="['priority', task.priority]">{{ task.priority }}</td>
          <td :class="{ completed: task.completed, pending: !task.completed }">
            {{ task.completed ? 'Completed' : 'Pending' }}
          </td>
          <td>{{ task.due_date }}</td>
          <td>{{ task.time }}</td>
          <td>{{ task.review_required ? 'Yes' : 'No' }}</td>
          <td class="action-cell">
            <button @click="updateTask(task.id)" class="btn small">✓</button>
          </td>
          <td class="action-cell">
            <button @click="openEditModal(task)" class="btn small">Edit Task</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <EditTaskModal
    :show="showModal"
    :task="editableTask"
    @save="submitEdit"
    @delete="deleteTask"
    @close="closeModal"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import EditTaskModal from '@/components/EditTaskModal.vue'

const tasks = ref([])
const showModal = ref(false)
const editableTask = ref({})

const fetchTasks = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/tasks')
    tasks.value = response.data.map(task => ({
      id: task.TaskID,
      description: task.TaskDescription,
      assigned_to: `${task.AssignedFirstName} ${task.AssignedLastName}`,
      created_by: `${task.CreatedByFirstName} ${task.CreatedByLastName}`,
      customer_id: task.CustomerID,
      customer_name: `${task.CustomerFirstName} ${task.CustomerLastName}`,
      priority: task.TaskPriority,
      status: task.TaskStatus,
      due_date: task.TaskDueDate,
      time: task.TaskTime,
      review_required: !!task.TaskIsReviewRequired,
      completed: task.TaskStatus === 'Completed',
      full: task
    }))
  } catch (error) {
    console.error('Error fetching tasks:', error)
  }
}

const openEditModal = (task) => {
  editableTask.value = {
    TaskID: task.id,
    CustomerID: task.customer_id,
    AssignedRepresentativeID: 1,
    CreatedByRepresentativeID: 1,
    CustomerName: task.customer_name,
    TaskType: 'Follow-Up Call',
    TaskIsReviewRequired: task.review_required,
    TaskDueDate: task.due_date,
    TaskTime: task.time,
    TaskPriority: task.priority,
    TaskStatus: task.status,
    TaskDescription: task.description
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const submitEdit = async (updatedTask) => {
  try {
    await axios.put(`http://127.0.0.1:5000/api/tasks/${updatedTask.TaskID}`, updatedTask)
    fetchTasks()
    showModal.value = false
  } catch (error) {
    console.error('Error updating task:', error)
  }
}

const deleteTask = async (taskId) => {
  try {
    await axios.delete(`http://127.0.0.1:5000/api/tasks/${taskId}`)
    fetchTasks()
    showModal.value = false
  } catch (error) {
    console.error('Error deleting task:', error)
  }
}

const updateTask = async (taskId) => {
  const task = tasks.value.find(t => t.id === taskId)
  if (task) {
    const updatedStatus = task.completed ? 'Pending' : 'Completed'

    try {
      await axios.put(`http://127.0.0.1:5000/api/tasks/${task.id}`, {
        TaskID: task.id,
        TaskDescription: task.description,
        TaskType: task.full.TaskType,
        TaskPriority: task.priority,
        TaskStatus: updatedStatus,
        TaskDueDate: task.due_date,
        TaskTime: task.time,
        TaskIsReviewRequired: task.review_required,
        CustomerID: task.customer_id,
        CustomerName: task.customer_name,
        AssignedRepresentativeID: task.full.AssignedRepresentativeID,
        CreatedByRepresentativeID: task.full.CreatedByRepresentativeID
      })

      // Re-fetch task list to reflect changes
      fetchTasks()
    } catch (error) {
      console.error('Error toggling task status:', error)
    }
  }
}



onMounted(fetchTasks)
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 100%;
  margin: auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  color: #000;
  margin-bottom: 16px;
}

.task-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.05);
  table-layout: fixed;
}

.task-table th,
.task-table td {
  padding: 8px;
  border: 1px solid #ddd;
  text-align: center;
  color: #000;
  word-wrap: break-word;
  vertical-align: top;
}

.wrap-cell {
  max-width: 120px;
  white-space: normal;
  word-break: break-word;
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

.completed {
  color: green;
  font-weight: bold;
}

.pending {
  color: gray;
  font-weight: bold;
}

.btn {
  background: #28a745;
  color: white;
  font-size: 14px;
  padding: 6px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn:hover {
  background: #218838;
}

.btn.small {
  width: auto;
  padding: 4px 8px;
  font-size: 12px;
}

.action-cell {
  padding: 6px;
}
</style>