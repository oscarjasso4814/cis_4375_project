<template>
    <div v-if="show" class="modal-overlay">
      <div class="modal">
        <h3 class="text-2xl font-bold text-center">Edit Task</h3>
  
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="font-semibold">Description</label>
            <input v-model="task.TaskDescription" class="input-field" />
          </div>
  
          <div>
            <label class="font-semibold">Type</label>
            <input v-model="task.TaskType" class="input-field" />
          </div>
  
          <div>
            <label class="font-semibold">Priority</label>
            <select v-model="task.TaskPriority" class="input-field">
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>
  
          <div>
            <label class="font-semibold">Status</label>
            <select v-model="task.TaskStatus" class="input-field">
              <option value="Pending">Pending</option>
              <option value="Completed">Completed</option>
            </select>
          </div>
  
          <div>
            <label class="font-semibold">Due Date</label>
            <input type="date" v-model="task.TaskDueDate" class="input-field" />
          </div>
  
          <div>
            <label class="font-semibold">Time</label>
            <input type="time" v-model="task.TaskTime" class="input-field" />
          </div>
  
          <div>
            <label class="font-semibold">Review Required</label>
            <input type="checkbox" v-model="task.TaskIsReviewRequired" class="mt-2" />
          </div>
  
          <div>
            <label class="font-semibold">Customer Name</label>
            <input v-model="task.CustomerName" class="input-field" />
          </div>
  
          <div>
            <label class="font-semibold">Customer ID</label>
            <input type="number" v-model="task.CustomerID" class="input-field" />
          </div>
  
          <div>
            <label class="block mb-2 font-semibold">Assigned Representative:</label>
            <select v-model="task.AssignedRepresentativeID" class="w-full border p-2 rounded mb-4">
            <option v-for="rep in reps" :key="rep.id" :value="rep.id">
            {{ rep.name }}
            </option>
            </select>

          </div>
  
          <div>
            <label class="font-semibold">Created By Rep ID</label>
            <input type="number" v-model="task.CreatedByRepresentativeID" class="input-field" />
          </div>
        </div>
  
        <div class="button-group">
          <button @click="$emit('save', task)" type="submit" class="btn save">Save</button>
          <button @click="$emit('delete', task.TaskID)" type="button" class="btn delete">Delete</button>
          <button @click="$emit('close')" type="button" class="btn cancel">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue'
  
  const props = defineProps({
    show: Boolean,
    task: Object,
    reps: Array
  })
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

/* Individual button styles */
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
  