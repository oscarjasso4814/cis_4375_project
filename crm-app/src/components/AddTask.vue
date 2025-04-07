<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>Add Task</h3>

      <div class="customer-info">
      <p><strong>Customer:</strong> {{ props.customerName }}</p>
      <p><strong>Customer ID:</strong> {{ props.customerId }}</p>
      <p><strong>Created By:</strong> {{ props.createdByName }}</p>

      </div>

      <form @submit.prevent="submitTask">
        <!-- Form fields here -->
        <label>Type:</label>
        <input v-model="task.type" required />

        <label>Description:</label>
        <textarea v-model="task.description" required />

        <label>Assign To Representative:</label>
          <select v-model="task.assignedRep" required>
          <option disabled value="">-- Select Representative --</option>
          <option
            v-for="rep in props.representatives"
            :key="rep.RepresentativeID"
            :value="rep.RepresentativeID"
          >
          {{ rep.FirstName }} {{ rep.LastName }}
          </option>
          </select>


        <label>Due Date:</label>
        <input type="date" v-model="task.dueDate" required />

        <label>Time:</label>
        <input type="time" v-model="task.time" required />

        <label>Priority:</label>
        <input v-model="task.priority" />

        <label>Review Required:</label>
        <input type="checkbox" v-model="task.isReviewRequired" />

        <div class="actions">
          <button type="submit">Submit</button>
          <button type="button" @click="$emit('close')">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>


<script setup>
import { ref, defineEmits, defineProps } from 'vue'
import axios from 'axios'
import { url } from "../api/apiurl"

const emit = defineEmits(['close'])
const props = defineProps({
  customerId: Number,
  customerName: String,
  createdByRep: Number,
  createdByName: String,
  representatives: Array
})

const task = ref({
  assignedRep: props.createdByRep,
  createdByRep: props.createdByRep,
  customerId: props.customerId,
  customerName: props.customerName,
  description: '',
  dueDate: '',
  time: '',
  priority: '',
  status: '',
  type: '',
  isReviewRequired: false
})

const submitTask = async () => {
  try {
    await axios.post(url + '/api/Task', task.value)
    alert('Task added successfully!')
    emit('close')
  } catch (err) {
    console.error(err)
    alert('Failed to add task.')
  }
}

</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 12px;
  width: 400px;
  max-width: 90%;
}
.actions {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
}
.modal-content {
  background: white;
  padding: 24px;
  border-radius: 12px;
  width: 400px;
  max-width: 90%;
  font-size: 16px;
  color: #333;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  max-height: 90vh;
  overflow-y: auto;
}


label {
  display: block;
  margin-top: 12px;
  font-weight: 600;
}

input,
textarea {
  width: 100%;
  padding: 8px;
  margin-top: 4px;
  margin-bottom: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  color: #333;
}

button {
  padding: 8px 16px;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button[type="submit"] {
  background-color: #4CAF50;
  color: white;
}

button[type="button"] {
  background-color: #ccc;
  color: black;
}

select {
  width: 100%;
  padding: 8px;
  margin-top: 4px;
  margin-bottom: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  color: #333;
}

.customer-info {
  margin-bottom: 16px;
  padding: 12px;
  background-color: #f5f5f5;
  border-radius: 8px;
  font-size: 15px;
  color: #333;
}
.customer-info p {
  margin: 4px 0;
}

</style>

