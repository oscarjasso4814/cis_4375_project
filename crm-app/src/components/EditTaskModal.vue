<template>
    <div v-if="show" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div class="bg-white p-6 rounded-xl shadow-lg w-full max-w-2xl space-y-4">
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
  
        <div class="flex justify-end gap-4 pt-4">
          <button @click="$emit('save', task)" class="btn bg-blue-600 hover:bg-blue-800 text-white">Save</button>
          <button @click="$emit('delete', task.TaskID)" class="btn bg-red-600 hover:bg-red-800 text-white">Delete</button>
          <button @click="$emit('close')" class="btn bg-gray-300 text-black">Cancel</button>
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
  </style>
  