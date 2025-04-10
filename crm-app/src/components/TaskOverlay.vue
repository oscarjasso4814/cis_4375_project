<script setup>
import { ref } from 'vue';

const showTasks = ref(false);
const tasks = ref([
  { id: 1, text: 'Call back Client A' },
  { id: 2, text: 'Update policy record' },
  { id: 3, text: 'Send renewal reminder' }
]);

const toggleTasks = () => {
  showTasks.value = !showTasks.value;
};
</script>

<template>
  <div>
    <button @click="toggleTasks">Toggle Tasks</button>
    <div v-if="showTasks" class="task-overlay">
      <h3>📝 Tasks</h3>
      <ul>
        <li v-for="task in tasks" :key="task.id">{{ task.text }}</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.task-overlay {
  background: #e6f0ff;
  border: 1px solid #3399ff;
  padding: 20px;
  margin-top: 20px;
  border-radius: 8px;
}
button {
  margin-top: 20px;
  padding: 8px 16px;
  background: #3399ff;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}
</style>
