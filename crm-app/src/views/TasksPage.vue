<template>
  <div class="container">
    <h2 class="title">Tasks</h2>
    
    <!-- Filter controls -->
    <div class="filter-controls">
      <div class="filter-group">
        <label for="status-filter">Status:</label>
        <select v-model="filters.status" id="status-filter" class="filter-input">
          <option value="">All</option>
          <option value="Pending">Pending</option>
          <option value="Completed">Completed</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="priority-filter">Priority:</label>
        <select v-model="filters.priority" id="priority-filter" class="filter-input">
          <option value="">All</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="search-filter">Search:</label>
        <input 
          v-model="filters.search" 
          id="search-filter" 
          placeholder="Search in description or customer..."
          class="filter-input search-input"
        />
      </div>
      
      <button @click="resetFilters" class="btn reset-btn">
        Reset Filters
      </button>
    </div>

    <table class="task-table">
      <thead>
        <tr>
          <th @click="sortBy('id')" :class="{ active: sortKey === 'id' }">
            ID
            <span v-if="sortKey === 'id'" class="sort-indicator">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
          </th>
          <th @click="sortBy('description')" :class="{ active: sortKey === 'description' }">
            Description
            <span v-if="sortKey === 'description'" class="sort-indicator">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
          </th>
          <th @click="sortBy('assigned_to')" :class="{ active: sortKey === 'assigned_to' }">
            Assigned To
            <span v-if="sortKey === 'assigned_to'" class="sort-indicator">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
          </th>
          <th @click="sortBy('customer_name')" :class="{ active: sortKey === 'customer_name' }">
            Customer
            <span v-if="sortKey === 'customer_name'" class="sort-indicator">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
          </th>
          <th @click="sortBy('created_by')" :class="{ active: sortKey === 'created_by' }">
            Created By
            <span v-if="sortKey === 'created_by'" class="sort-indicator">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
          </th>
          <th @click="sortBy('priority')" :class="{ active: sortKey === 'priority' }">
            Priority
            <span v-if="sortKey === 'priority'" class="sort-indicator">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
          </th>
          <th @click="sortBy('completed')" :class="{ active: sortKey === 'completed' }">
            Status
            <span v-if="sortKey === 'completed'" class="sort-indicator">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
          </th>
          <th @click="sortBy('due_date')" :class="{ active: sortKey === 'due_date' }">
            Due
            <span v-if="sortKey === 'due_date'" class="sort-indicator">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
          </th>
          <th @click="sortBy('time')" :class="{ active: sortKey === 'time' }">
            Time Created
            <span v-if="sortKey === 'time'" class="sort-indicator">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
          </th>
          <th @click="sortBy('review_required')" :class="{ active: sortKey === 'review_required' }">
            Review Required
            <span v-if="sortKey === 'review_required'" class="sort-indicator">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
          </th>
          <th colspan="2">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="isLoading" class="loading-row">
          <td colspan="12" class="loading-cell">Loading tasks...</td>
        </tr>
        <tr v-else-if="filteredTasks.length === 0" class="empty-row">
          <td colspan="12" class="empty-cell">No tasks found matching your filters</td>
        </tr>
        <tr v-for="task in filteredTasks" :key="task.id">
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
    :reps="representatives"
    @save="submitEdit"
    @delete="deleteTask"
    @close="closeModal"
  />
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import EditTaskModal from '@/components/EditTaskModal.vue'
import { url } from '@/api/apiurl'

// State variables
const tasks = ref([])
const representatives = ref([])
const showModal = ref(false)
const editableTask = ref({})
const isLoading = ref(true)

// Sorting state
const sortKey = ref('id')
const sortOrder = ref('desc')

// Filtering state
const filters = ref({
  status: '',
  priority: '',
  search: ''
})

// Sort tasks by the selected key
const sortBy = (key) => {
  // If clicking on the same column, toggle the sort order
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    // If clicking on a new column, set it as the sort key and default to ascending
    sortKey.value = key
    sortOrder.value = 'asc'
  }
}

// Reset all filters to their default values
const resetFilters = () => {
  filters.value = {
    status: '',
    priority: '',
    search: ''
  }
}

// Filter and sort the tasks based on the current filters and sort settings
const filteredTasks = computed(() => {
  // Start with all tasks
  let result = [...tasks.value]
  
  // Apply status filter
  if (filters.value.status) {
    const isCompleted = filters.value.status === 'Completed'
    result = result.filter(task => task.completed === isCompleted)
  }
  
  // Apply priority filter
  if (filters.value.priority) {
    result = result.filter(task => 
      task.priority.toLowerCase() === filters.value.priority.toLowerCase()
    )
  }
  
  // Apply search filter (case-insensitive search in description and customer name)
  if (filters.value.search) {
    const searchTerm = filters.value.search.toLowerCase()
    result = result.filter(task => 
      task.description.toLowerCase().includes(searchTerm) || 
      task.customer_name.toLowerCase().includes(searchTerm)
    )
  }
  
  // Sort the filtered results
  result.sort((a, b) => {
    let valueA = a[sortKey.value]
    let valueB = b[sortKey.value]
    
    // Handle string comparison (case-insensitive)
    if (typeof valueA === 'string' && typeof valueB === 'string') {
      valueA = valueA.toLowerCase()
      valueB = valueB.toLowerCase()
    }
    
    // Handle undefined values
    if (valueA === undefined) return sortOrder.value === 'asc' ? -1 : 1
    if (valueB === undefined) return sortOrder.value === 'asc' ? 1 : -1
    
    // Compare values
    if (valueA < valueB) return sortOrder.value === 'asc' ? -1 : 1
    if (valueA > valueB) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })
  
  return result
})

// Fetch all tasks from the API
const fetchTasks = async () => {
  try {
    isLoading.value = true
    await axios.get(`${url}/api/tasks`).then((response) => {
    tasks.value = response.data.map(task => ({
      id: task.TaskID,
      description: task.TaskDescription,
      assigned_to: `${task.AssignedFirstName || ''} ${task.AssignedLastName || ''}`.trim(),
      created_by: `${task.CreatedByFirstName || ''} ${task.CreatedByLastName || ''}`.trim(),
      customer_id: task.CustomerID,
      customer_name: `${task.CustomerFirstName || ''} ${task.CustomerLastName || ''}`.trim(),
      priority: task.TaskPriority || 'Medium',
      status: task.TaskStatus,
      due_date: task.TaskDueDate,
      time: task.TaskTime,
      review_required: !!task.TaskIsReviewRequired,
      completed: task.TaskStatus === 'Completed',
      full: task
    }))})
  } catch (error) {
    console.error('Error fetching tasks:', error)
  } finally {
    isLoading.value = false
  }
}

// Fetch representatives for the task assignment dropdown
const fetchRepresentatives = async () => {
  try {
    // Replace with your actual API endpoint for representatives
    // const response = await axios.get(`${url}/api/representatives`)
    // representatives.value = response.data
    
    // For now, using placeholder data
    representatives.value = [
      { id: 1, name: 'Amin Lalani' },
      { id: 2, name: 'John Doe' }
    ]
  } catch (error) {
    console.error('Error fetching representatives:', error)
  }
}

// Open the edit modal for a task
const openEditModal = (task) => {
  editableTask.value = {
    TaskID: task.id,
    CustomerID: task.customer_id,
    AssignedRepresentativeID: task.full.AssignedRepresentativeID,
    CreatedByRepresentativeID: task.full.CreatedByRepresentativeID,
    CustomerName: task.customer_name,
    TaskType: task.full.TaskType || 'Follow-Up Call',
    TaskIsReviewRequired: task.review_required,
    TaskDueDate: task.due_date,
    TaskTime: task.time,
    TaskPriority: task.priority,
    TaskStatus: task.status,
    TaskDescription: task.description
  }
  showModal.value = true
}

// Close the edit modal
const closeModal = () => {
  showModal.value = false
}

// Submit edits to a task
const submitEdit = async (updatedTask) => {
  try {
    await axios.put(`${url}/api/tasks/${updatedTask.TaskID}`, updatedTask)
    fetchTasks()
    showModal.value = false
  } catch (error) {
    console.error('Error updating task:', error)
  }
}

// Delete a task
const deleteTask = async (taskId) => {
  try {
    await axios.delete(`${url}/api/tasks/${taskId}`)
    fetchTasks()
    showModal.value = false
  } catch (error) {
    console.error('Error deleting task:', error)
  }
}

// Update a task's status (toggle between Pending and Completed)
const updateTask = async (taskId) => {
  const task = tasks.value.find(t => t.id === taskId)
  if (task) {
    const updatedStatus = task.completed ? 'Pending' : 'Completed'

    try {
      await axios.put(`${url}/api/tasks/${task.id}`, {
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

// Watch for changes in filters to update filtered tasks
watch(filters, () => {
  // No additional action needed as filteredTasks is a computed property
}, { deep: true })

// On component mount, fetch data
onMounted(() => {
  fetchTasks()
  fetchRepresentatives()
})
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

/* Filter Controls */
.filter-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 1px solid #e9ecef;
}

.filter-group {
  display: flex;
  flex-direction: column;
  min-width: 150px;
}

.filter-input {
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
}

.search-input {
  min-width: 250px;
}

.reset-btn {
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 15px;
  margin-left: auto;
  align-self: flex-end;
  cursor: pointer;
  transition: background-color 0.2s;
}

.reset-btn:hover {
  background-color: #5a6268;
}

/* Table Styles */
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

.task-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  position: relative;
  cursor: pointer;
  transition: background-color 0.2s;
}

.task-table th:hover {
  background-color: #e9ecef;
}

.task-table th.active {
  background-color: #e2e6ea;
}

.sort-indicator {
  margin-left: 5px;
  font-size: 10px;
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

.loading-cell, .empty-cell {
  padding: 30px !important;
  text-align: center;
  color: #6c757d;
  font-style: italic;
}

@media screen and (max-width: 768px) {
  .filter-controls {
    flex-direction: column;
  }
  
  .filter-group, .search-input {
    width: 100%;
    min-width: auto;
  }
  
  .task-table {
    display: block;
    overflow-x: auto;
  }
}
</style>