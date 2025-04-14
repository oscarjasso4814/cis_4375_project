<template>
    <div class="notes-container">
      <div class="notes-header">
        <div class="filter-controls">
          <div class="filter-group">
            <label for="note-type-filter">Filter by Type:</label>
            <select v-model="selectedType" id="note-type-filter" class="filter-select">
              <option value="">All Types</option>
              <option value="General">General</option>
              <option v-for="category in categories" :key="category.CategoryID" :value="category.CategoryName">
                {{ category.CategoryName }}
              </option>
            </select>
          </div>
          <div class="filter-group">
            <label for="sort-order">Sort:</label>
            <select v-model="sortOrder" id="sort-order" class="filter-select">
              <option value="desc">Newest First</option>
              <option value="asc">Oldest First</option>
            </select>
          </div>
        </div>
        
        <button @click="showNoteForm = !showNoteForm" class="action-btn">
          {{ showNoteForm ? 'Cancel' : 'Add Note' }}
        </button>
      </div>
      
      <!-- Add Note Form -->
      <div v-if="showNoteForm" class="note-form">
        <div class="form-group">
          <label for="note-type">Note Type:</label>
          <select v-model="newNote.NoteType" id="note-type" class="input-field" required>
            <option value="" disabled selected>Select a type</option>
            <option value="General">General</option>
            <option v-for="category in categories" :key="category.CategoryID" :value="category.CategoryName">
              {{ category.CategoryName }}
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="note-content">Note Content:</label>
          <textarea 
            v-model="newNote.NoteContent" 
            id="note-content" 
            class="input-field note-textarea" 
            placeholder="Enter your note here..."
            required
          ></textarea>
        </div>
        
        <div class="form-actions">
          <button @click="saveNote" class="primary-btn">Save Note</button>
          <button @click="showNoteForm = false" class="secondary-btn">Cancel</button>
        </div>
      </div>
      
      <!-- Notes List -->
      <div v-if="isLoading" class="loading-message">
        Loading notes...
      </div>
      
      <div v-else-if="filteredNotes.length === 0" class="empty-notes">
        <p>No notes found for this customer.</p>
      </div>
      
      <div v-else class="notes-list">
        <div v-for="note in filteredNotes" :key="note.NoteID" class="note-card">
          <div class="note-header">
            <div class="note-meta">
              <span class="note-type">{{ note.NoteType }}</span>
              <span class="note-date">{{ formatDate(note.DateCreated) }}</span>
            </div>
            <div class="note-actions">
              <button @click="deleteNote(note.NoteID)" class="delete-btn">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
          
          <div class="note-content">{{ note.NoteContent }}</div>
          
          <div class="note-footer">
            <span class="note-author">Created by: {{ note.RepresentativeName || 'Unknown' }}</span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  import axios from 'axios';
  import { url } from '@/api/apiurl';
  
  const props = defineProps({
    customerId: {
      type: [Number, String], // Accept both Number and String types
      required: true
    },
    customerName: {
      type: String,
      required: true
    }
  });
  
  // State variables
  const notes = ref([]);
  const categories = ref([]);
  const isLoading = ref(true);
  const showNoteForm = ref(false);
  const selectedType = ref('');
  const sortOrder = ref('desc');
  
  // New note form data
  const newNote = ref({
    CustomerID: props.customerId,
    CustomerName: props.customerName,
    CreatedByRepresentativeID: localStorage.getItem('reps_id') || null,
    NoteType: '',
    NoteContent: ''
  });
  
  // Get notes for the customer with delay
  const fetchNotes = () => {
    isLoading.value = true;
    
    // Delay the notes API call by 1000ms (1 second)
    setTimeout(() => {
      axios.get(`${url}/api/customer/${props.customerId}/notes`)
        .then((response) => {
          console.log("Notes fetched successfully:", response.data);
          notes.value = response.data;
        })
        .catch((error) => {
          console.error('Error fetching notes:', error);
          if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            console.error('Response data:', error.response.data);
            console.error('Response status:', error.response.status);
          } else if (error.request) {
            // The request was made but no response was received
            console.error('No response received from server');
          } else {
            // Something happened in setting up the request that triggered an Error
            console.error('Error message:', error.message);
          }
          // Set empty notes array to prevent errors
          notes.value = [];
        })
        .finally(() => {
          isLoading.value = false;
        });
    }, 1000); // 1 second delay
  };
  
  // Get categories for the dropdown with delay
  const fetchCategories = () => {
    // Delay the categories API call
    setTimeout(() => {
      axios.get(`${url}/api/categories`)
        .then((response) => {
          console.log("Categories fetched successfully:", response.data);
          categories.value = response.data;
        })
        .catch((error) => {
          console.error('Error fetching categories:', error);
          if (error.response) {
            console.error('Response data:', error.response.data);
            console.error('Response status:', error.response.status);
          } else if (error.request) {
            console.error('No response received from server');
          } else {
            console.error('Error message:', error.message);
          }
          // Set default categories to prevent errors
          categories.value = [
            { CategoryID: 1, CategoryName: "Life" },
            { CategoryID: 2, CategoryName: "Health" },
            { CategoryID: 3, CategoryName: "Auto" },
            { CategoryID: 4, CategoryName: "Home" }
          ];
        });
    }, 2000); // 2 second delay
  };
  
  // Save a new note
  const saveNote = () => {
    if (!newNote.value.NoteType || !newNote.value.NoteContent) {
      alert('Please fill in all required fields');
      return;
    }
    
    const payload = {
      CustomerID: props.customerId,
      CustomerName: props.customerName,
      CreatedByRepresentativeID: localStorage.getItem('reps_id'),
      NoteType: newNote.value.NoteType,
      NoteContent: newNote.value.NoteContent,
      PolicyID: null
    };
    
    console.log("Sending note payload:", payload);
    
    axios.post(`${url}/api/note`, payload)
      .then((response) => {
        console.log("Note saved successfully:", response.data);
        
        // Reset form and refresh notes
        newNote.value.NoteType = '';
        newNote.value.NoteContent = '';
        showNoteForm.value = false;
        fetchNotes();
      })
      .catch((error) => {
        console.error('Error saving note:', error);
        if (error.response) {
          console.error('Response data:', error.response.data);
          console.error('Response status:', error.response.status);
        } else if (error.request) {
          console.error('No response received from server');
        } else {
          console.error('Error message:', error.message);
        }
        alert('Failed to save note. Please try again.');
      });
  };
  
  // Delete a note
  const deleteNote = (noteId) => {
    if (!confirm('Are you sure you want to delete this note?')) {
      return;
    }
    
    axios.delete(`${url}/api/note/${noteId}`)
      .then((response) => {
        console.log("Note deleted successfully:", response.data);
        fetchNotes();
      })
      .catch((error) => {
        console.error('Error deleting note:', error);
        if (error.response) {
          console.error('Response data:', error.response.data);
          console.error('Response status:', error.response.status);
        } else if (error.request) {
          console.error('No response received from server');
        } else {
          console.error('Error message:', error.message);
        }
        alert('Failed to delete note. Please try again.');
      });
  };
  
  // Format date for display
  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    
    const date = new Date(dateStr);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };
  
  // Filtered and sorted notes
  const filteredNotes = computed(() => {
    let result = [...notes.value];
    
    // Apply type filter
    if (selectedType.value) {
      result = result.filter(note => note.NoteType === selectedType.value);
    }
    
    // Apply sorting
    result.sort((a, b) => {
      const dateA = new Date(a.DateCreated);
      const dateB = new Date(b.DateCreated);
      
      return sortOrder.value === 'asc' 
        ? dateA - dateB 
        : dateB - dateA;
    });
    
    return result;
  });
  
  // Initialize data on component mount with staggered delays
  onMounted(() => {
    console.log("CustomerNotes component mounted for customer ID:", props.customerId);
    
    // Add a small delay before starting to fetch data
    setTimeout(() => {
      // Fetch categories first
      fetchCategories();
      
      // Then fetch notes with an additional delay
      setTimeout(() => {
        fetchNotes();
      }, 1500); // 1.5 second delay after categories
    }, 500); // Initial delay
  });
  </script>
  
  <style scoped>
  .notes-container {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #333;
  }
  
  /* Header and Filter Controls */
  .notes-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
  }
  
  .filter-controls {
    display: flex;
    gap: 15px;
  }
  
  .filter-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .filter-select {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    background-color: white;
  }
  
  .action-btn {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s;
  }
  
  .action-btn:hover {
    background-color: #0056b3;
  }
  
  /* Note Form */
  .note-form {
    background-color: #f8f9fa;
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 15px;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
  }
  
  .input-field {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
  }
  
  .note-textarea {
    min-height: 100px;
    resize: vertical;
  }
  
  .form-actions {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
  }
  
  .primary-btn, .secondary-btn {
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .primary-btn {
    background-color: #28a745;
    color: white;
    border: none;
  }
  
  .primary-btn:hover {
    background-color: #218838;
  }
  
  .secondary-btn {
    background-color: #6c757d;
    color: white;
    border: none;
  }
  
  .secondary-btn:hover {
    background-color: #5a6268;
  }
  
  /* Notes List */
  .notes-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
    max-height: 500px;
    overflow-y: auto;
    padding-right: 5px;
  }
  
  .note-card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 15px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }
  
  .note-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
  }
  
  .note-meta {
    display: flex;
    align-items: center;
    gap: 15px;
  }
  
  .note-type {
    font-weight: 600;
    color: #007bff;
    background-color: rgba(0, 123, 255, 0.1);
    padding: 3px 8px;
    border-radius: 12px;
    font-size: 12px;
  }
  
  .note-date {
    color: #666;
    font-size: 12px;
  }
  
  .note-content {
    margin-bottom: 10px;
    line-height: 1.5;
    word-break: break-word;
  }
  
  .note-footer {
    display: flex;
    justify-content: flex-end;
    font-size: 12px;
    color: #666;
    border-top: 1px solid #eee;
    padding-top: 8px;
    margin-top: 8px;
  }
  
  .note-author {
    font-style: italic;
  }
  
  .note-actions {
    display: flex;
    gap: 5px;
  }
  
  .delete-btn {
    background-color: transparent;
    color: #dc3545;
    border: none;
    padding: 3px;
    cursor: pointer;
    font-size: 14px;
    transition: color 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .delete-btn:hover {
    color: #bd2130;
  }
  
  /* Loading and Empty States */
  .loading-message, .empty-notes {
    text-align: center;
    padding: 30px 0;
    color: #6c757d;
    font-style: italic;
  }
  </style>