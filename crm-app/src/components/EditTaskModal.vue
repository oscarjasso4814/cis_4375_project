<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal">
      <h3 class="text-2xl font-bold text-center">Edit Task</h3>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="font-semibold">Description</label>
          <input v-model="editableTask.TaskDescription" class="input-field" />
        </div>

        <div>
          <label class="font-semibold">Type</label>
          <input v-model="editableTask.TaskType" class="input-field" />
        </div>

        <div>
          <label class="font-semibold">Priority</label>
          <select v-model="editableTask.TaskPriority" class="input-field">
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </div>

        <div>
          <label class="font-semibold">Status</label>
          <select v-model="editableTask.TaskStatus" class="input-field">
            <option value="Pending">Pending</option>
            <option value="Completed">Completed</option>
          </select>
        </div>

        <div>
          <label class="font-semibold">Due Date</label>
          <input type="date" v-model="editableTask.TaskDueDate" class="input-field" />
        </div>

        <div>
          <label class="font-semibold">Time</label>
          <input type="time" v-model="editableTask.TaskTime" class="input-field" />
        </div>

        <div>
          <label class="font-semibold">Review Required</label>
          <input type="checkbox" v-model="editableTask.TaskIsReviewRequired" class="mt-2" />
        </div>

        <div>
          <label class="font-semibold">Customer Name</label>
          <input v-model="editableTask.CustomerName" class="input-field" />
        </div>

        <div>
          <label class="font-semibold">Customer ID</label>
          <input type="number" v-model="editableTask.CustomerID" class="input-field" />
        </div>

        <div>
          <label>Assign To:</label>
          <select v-model="editableTask.AssignedRepresentativeID" class="input-field">
            <option 
              v-for="rep in representatives" 
              :key="rep.RepresentativeID" 
              :value="rep.RepresentativeID">
              {{ rep.FirstName }} {{ rep.LastName }}
            </option>
          </select>
        </div>

        <div>
          <label class="font-semibold">Created By Rep ID</label>
          <input type="number" v-model="editableTask.CreatedByRepresentativeID" class="input-field" />
        </div>
      </div>

      <div class="button-group">
        <button @click="$emit('save', { ...editableTask })" type="submit" class="btn save">Save</button>
        <button @click="$emit('delete', editableTask.TaskID)" type="button" class="btn delete">Delete</button>
        <button @click="$emit('close')" type="button" class="btn cancel">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, defineProps, defineEmits } from 'vue'
import axios from 'axios'

const emit = defineEmits(['close', 'save', 'delete'])

const props = defineProps({
  show: Boolean,
  task: Object
})

const editableTask = ref({})
const representatives = ref([])

watch(
  () => props.task,
  (newTask) => {
    editableTask.value = { ...newTask }
  },
  { immediate: true }
)
function fetchRep() {
  axios.get('http://127.0.0.1:5000/api/Representative')
    .then(res => {
      representatives.value = res.data
    })
    .catch(err => {
      console.error('Failed to fetch representatives:', err)
    })
}

// Call the fetch task function when the component mounts
onMounted(async () => {
  setTimeout(() => {
    fetchRep()
  }, 1000)
});

 
/*
onMounted(() => {
  axios.get('http://127.0.0.1:5000/api/Representative')
    .then(res => {
      representatives.value = res.data
    })
    .catch(err => {
      console.error('Failed to fetch representatives:', err)
    })
})*/
</script>

<style scoped>
.input-field {
  width: 100%;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  background: white;
  color: black;
  margin-top: 4px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 12px;
  width: 400px;
  max-height: 80vh;
  overflow-y: auto;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.btn {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn.save {
  background-color: #4CAF50;
  color: white;
}

.btn.save:hover {
  background-color: #45a049;
}

.btn.delete {
  background-color: #f44336;
  color: white;
}

.btn.delete:hover {
  background-color: #d32f2f;
}

.btn.cancel {
  background-color: #9e9e9e;
  color: white;
}

.btn.cancel:hover {
  background-color: #757575;
}
</style>
