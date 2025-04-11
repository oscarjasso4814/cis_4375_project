<script setup>
import { ref } from 'vue';

const showTasks = ref(true); // Default to showing tasks
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
  <div class="task-container">
    <button @click="toggleTasks" class="task-toggle">
      {{ showTasks ? 'Hide Tasks' : 'Show Tasks' }}
    </button>
    <div v-if="showTasks" class="task-overlay">
      <h3>📝 Tasks</h3>
      <ul class="task-list">
        <li v-for="task in tasks" :key="task.id" class="task-item">{{ task.text }}</li>
      </ul>
    </div>
  </div>
</template>





<style scoped>
.task-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.task-toggle {
  margin: 10px;
  padding: 8px 16px;
  background: #3399ff;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  align-self: flex-start;
}

.task-toggle:hover {
  background: #2288ee;
}

.task-overlay {
  background: #e6f0ff;
  border: 1px solid #3399ff;
  padding: 20px;
  border-radius: 8px;
  flex: 1;
  display: flex;
  flex-direction: column;
  margin: 10px;
}

.task-overlay h3 {
  margin-top: 0;
  font-size: 18px;
  color: #333;
}

.task-list {
  padding-left: 20px;
}

.task-item {
  margin-bottom: 10px;
  color: #333;
}
</style>