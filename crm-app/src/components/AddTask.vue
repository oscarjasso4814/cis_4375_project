<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>Add Task for {{ props.customerName }}</h3>

      <div class="customer-info">
        <p><strong>Customer ID:</strong> {{ props.customerId }}</p>
        <p><strong>Created By:</strong> {{ createdByName }}</p>
      </div>

      <form @submit.prevent="submitTask">
        <label>Type:</label>
        <input v-model="task.type" required />

        <label>Description:</label>
        <textarea v-model="task.description" required />

        <label>Assign To Representative:</label>
        <select v-model="task.assignedRep" required>
          <option disabled value="">-- Select Representative --</option>
          <option
            v-for="rep in representatives"
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
import { ref, defineEmits, defineProps, onMounted } from 'vue'
import axios from 'axios'
import { url } from "../api/apiurl"

const emit = defineEmits(['close'])

const props = defineProps({
  customerId: Number,
  customerName: String
})

const representatives = ref([])
const createdByRep = ref(null)
const createdByName = ref('')

const task = ref({
  assignedRep: '',
  createdByRep: null,
  customerId: props.customerId,
  customerName: props.customerName,
  description: '',
  dueDate: '',
  time: '',
  priority: '',
  type: '',
  isReviewRequired: false
})

function fetchRep() {
  axios.get(`${url}/api/Representative`)  //${url}/api/tasks
    .then(res => {
      representatives.value = res.data
    })
    .catch(err => {
      console.error('Failed to fetch representatives:', err)
    })
}

function fetchCreatorName() {
  axios.get(`${url}/api/rep/${createdByRep.value}/name`)
    .then(res => {
      if (res.data.length > 0) {
        const rep = res.data[0]
        createdByName.value = `${rep.FirstName} ${rep.LastName}`
      }
    })
    .catch(err => {
      console.error('Failed to fetch rep name:', err)
    })
}

const submitTask = async () => {
  const payload = {
  CustomerID: task.value.customerId,
  AssignedRepresentativeID: task.value.assignedRep,
  CreatedByRepresentativeID: task.value.createdByRep,
  CustomerName: task.value.customerName,
  TaskType: task.value.type,
  TaskIsReviewRequired: task.value.isReviewRequired ? 1 : 0,
  TaskDueDate: task.value.dueDate,
  TaskTime: task.value.time,
  TaskPriority: task.value.priority,
  TaskStatus: 'Pending',
  TaskDescription: task.value.description
}


  try {
    await axios.post(url + '/api/tasks', payload)
    alert('Task added successfully!')
    emit('close')
  } catch (err) {
    console.error(err)
    alert('Failed to add task.')
  }
}

onMounted(() => {
  createdByRep.value = Number(localStorage.getItem('reps_id'))
  task.value.createdByRep = createdByRep.value
  fetchCreatorName()
  setTimeout(fetchRep, 1000)
})
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

