<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

// Mocked Data
const tasks = ref([]);
const employees = ref([
  { id: 1, username: "Alice" },
  { id: 2, username: "Bob" },
  { id: 3, username: "Joe" }
]);
const customers = ref([
  { id: 101, name: "John Doe" },
  { id: 102, name: "Jane Smith" },
  { id: 103, name: "Mike Johnson" },
  { id: 104, name: "Emily Davis" },
  { id: 105, name: "William Brown" },
  { id: 106, name: "Chris Evans" },
  { id: 107, name: "Emma Watson" }
]);

const newTask = ref({ 
  description: '', 
  assigned_to: '', 
  customer_id: '', 
  priority: 'Medium', 
  status: 'Pending', 
  due_date: '' 
});

// Customer Search Feature
const customerSearch = ref('');
const filteredCustomers = ref([]);
const isDropdownOpen = ref(false);

// Filter customers based on search input
const filterCustomers = () => {
  const query = customerSearch.value.toLowerCase();
  filteredCustomers.value = customers.value.filter(customer =>
    customer.name.toLowerCase().includes(query) || customer.id.toString().includes(query)
  );
  isDropdownOpen.value = true;
};

// Select a customer and close dropdown
const selectCustomer = (customer) => {
  newTask.value.customer_id = customer.id;
  customerSearch.value = `${customer.id} - ${customer.name}`;
  isDropdownOpen.value = false;
};

// Close dropdown when clicking outside
const closeDropdown = (event) => {
  if (!event.target.closest('.dropdown-container')) {
    isDropdownOpen.value = false;
  }
};

// Add event listener when component mounts
onMounted(() => {
  document.addEventListener("click", closeDropdown);
});

// Remove event listener when component unmounts
onUnmounted(() => {
  document.removeEventListener("click", closeDropdown);
});

// Helper function to get employee name
const getEmployeeName = (id) => {
  const employee = employees.value.find(emp => emp.id === id);
  return employee ? employee.username : 'Unknown';
};

// Helper function to get customer name
const getCustomerName = (id) => {
  const customer = customers.value.find(cust => cust.id === id);
  return customer ? customer.name : 'Unknown';
};

// Simulate Fetching Tasks (No Backend)
const fetchTasks = () => {
  setTimeout(() => {
    tasks.value = [
      { id: 1, description: "Call customer", assigned_to: 1, customer_id: 101, priority: "High", status: "Pending", due_date: "2025-03-15", completed: false },
      { id: 2, description: "Send policy email", assigned_to: 2, customer_id: 102, priority: "Low", status: "Completed", due_date: "2025-03-14", completed: true }
    ];
  }, 500);
};

// Simulate Task Creation (No Backend)
const createTask = () => {
  const newId = tasks.value.length + 1;
  tasks.value.push({ id: newId, ...newTask.value, completed: false });
  newTask.value.description = '';
  newTask.value.assigned_to = '';
  newTask.value.customer_id = '';
  newTask.value.priority = 'Medium';
  newTask.value.status = 'Pending';
  newTask.value.due_date = '';
};

// Simulate Task Update (No Backend)
const updateTask = (taskId) => {
  const task = tasks.value.find(t => t.id === taskId);
  if (task) {
    task.completed = !task.completed;
    task.status = task.completed ? 'Completed' : 'Pending';
  }
};

// Load Mock Data on Page Load
onMounted(fetchTasks);
</script>

<template>
    <div class="container">
      <h2 class="title">Tasks</h2>
  
      <!-- Task Creation Form -->
      <form @submit.prevent="createTask" class="task-form">
        <!-- Task Description -->
        <label for="description">Task Description</label>
        <input id="description" v-model="newTask.description" placeholder="Enter task description" required class="input-field" />
  
        <!-- Assigned Employee -->
        <label for="assigned">Assigned To</label>
        <select id="assigned" v-model="newTask.assigned_to" required class="select-field">
          <option value="" disabled selected>-- Select Employee --</option>
          <option v-for="employee in employees" :key="employee.id" :value="employee.id">
            {{ employee.username }}
          </option>
        </select>
  
        <!-- Searchable Customer Selection -->
        <label for="customer">Customer</label>
        <div class="dropdown-container">
          <input id="customerSearch" 
                 v-model="customerSearch" 
                 placeholder="Search customer..." 
                 class="input-field" 
                 @input="filterCustomers" 
                 @focus="isDropdownOpen = true" />
  
          <ul v-if="isDropdownOpen && filteredCustomers.length" class="dropdown-list">
            <li v-for="customer in filteredCustomers" 
                :key="customer.id" 
                @click="selectCustomer(customer)">
              {{ customer.id }} - {{ customer.name }}
            </li>
          </ul>
        </div>
  
        <!-- Priority Dropdown -->
        <label for="priority">Priority</label>
        <select id="priority" v-model="newTask.priority" required class="select-field">
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
  
        <!-- Due Date Input -->
        <label for="dueDate">Due Date</label>
        <input id="dueDate" v-model="newTask.due_date" type="date" required class="input-field" />
  
        <!-- Submit Button -->
        <button type="submit" class="btn">Create Task</button>
      </form>
  
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

<style scoped>
/* Container */
.container {
  width: 90%;
  max-width: 800px; /* Prevents stretching */
  margin: auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden; /* Prevents overflow */
}

/* Title */
.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #000;
  margin-bottom: 20px;
}

/* Form Styling */
.task-form {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 20px;
  justify-content: space-between;
}

/* Ensure labels appear above inputs */
.task-form label {
  width: 100%;
  font-size: 14px;
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

/* Input Fields & Select Boxes */
.input-field,
.select-field {
  flex: 1;
  min-width: 48%; /* Ensures two fields fit per row */
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  background: white;
  color: black;
}

input:focus,
select:focus {
  border-color: #007bff;
  outline: none;
}

/* Full-width button */
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

/* Task Table */
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

/* Table Headers & Cells */
.task-table th,
.task-table td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: center;
  color: #000;
}

/* Priority Colors */
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

/* Customer Dropdown */
.dropdown-container {
  flex: 1;
  min-width: 48%;
  position: relative;
}

.dropdown-list {
  position: absolute;
  width: 100%;
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  list-style: none;
  padding: 0;
  margin-top: 4px;
}

.dropdown-list li {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  color: #000;
  font-weight: bold;
  background: #fff;
}

.dropdown-list li:hover {
  background: #f3f3f3;
}

/* Responsive Design */
@media (max-width: 768px) {
  .task-form {
    flex-direction: column;
  }

  .input-field,
  .select-field,
  .dropdown-container {
    min-width: 100%; /* Make fields stack on small screens */
  }

  .btn {
    font-size: 14px;
    padding: 10px;
  }
}

</style>
