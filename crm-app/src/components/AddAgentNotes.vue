<!-- AddNotes -->
<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { url } from '@/api/apiurl'

const showNoteBox = ref(false);
const noteContent = ref('');
const savedNotes = ref([]);
const repsId = ref();

// onMounted(() => {
//   const storedNotes = localStorage.getItem('savedNotes');
//   if (storedNotes) {
//     savedNotes.value = JSON.parse(storedNotes);
//   }
// });

onMounted(async () => {
  repsId.value = localStorage.getItem("reps_id");
  setTimeout(() => {
    fetchNotes(repsId.value)
  }, 1500)
});


// Fetch all agent notes for the homepage
const fetchNotes = async (repid) => {
  try {
    const response = await axios.get(`${url}/api/agentnote/` + repid);

    // Sort by most recent
    savedNotes.value = response.data
      .sort((a, b) => new Date(b.DateCreated) - new Date(a.DateCreated))
      .map(note => ({
        id: note.AgentNoteID,
        content: note.NoteContent,
        timestamp: note.DateCreated
      }));
  } catch (error) {
    console.error('Error fetching notes:', error);
  }
};

const saveNote = async () => {
  if (noteContent.value.trim() !== '') {
    try {
      await axios.post(`${url}/api/agentnote`, {
        CreatedByRepresentativeID: repsId.value, // make sure 'repid' is available in your component
        NoteContent: noteContent.value
      });

      fetchNotes(repsId.value);
      noteContent.value = '';
      showNoteBox.value = false;
    } catch (error) {
      console.error('Error saving note:', error);
    }
  }
};


const openNoteBox = () => {
  showNoteBox.value = true;
};

// Cancel function
const cancelNote = () => {
  noteContent.value = '';
  showNoteBox.value = false;
};

// Delete note
const deleteNote = async(noteid, index) => {
  await axios.delete(`${url}/api/AgentNote/` + noteid);
  savedNotes.value.splice(index, 1); // Remove from array
  localStorage.setItem('savedNotes', JSON.stringify(savedNotes.value)); // Update localStorage
};
</script>

<template>
  <div>
    <div class="sidebar-panel">
      <h3 class="panel-title">Agent Notes</h3>

      <!-- Add Note button -->
      <button v-if="!showNoteBox" class="action-btn" @click="openNoteBox">
        Add Note
      </button>

      <!-- Textarea for adding a new note -->
      <div v-if="showNoteBox" class="note-input">
        <textarea
          v-model="noteContent"
          class="note-textarea"
          placeholder="Write your notes here..."
        ></textarea>
        <button class="action-btn" @click="saveNote">
          Save Note
        </button>
        <button class="action-btn" @click="cancelNote">
            Cancel
        </button>
      </div>

      <!-- Display saved notes -->
      <div v-if="savedNotes.length > 0" class="saved-notes">
        <p class="saved-notes-title"><strong>Saved Notes:</strong></p>
        <div v-for="(note, index) in savedNotes" :key="index" class="saved-note">
          <p class="note-content">{{ note.content }}</p>
          <small class="note-timestamp">{{ note.timestamp }}</small>
          <div class="button-group">
            <button class="delete-btn" @click="deleteNote(note.id, index)">
              Remove
            </button>
          </div>
          <hr />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fffae6;
  border: 2px solid #ffd700;
  padding: 10px;
  border-radius: 8px;
  font-size: 14px;
  color: #000;
}

.header {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  color: #000;
}

/* Sidebar Panel */
.sidebar-panel {
  border: 1px;
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 16px;
}


.panel-title {
  margin-bottom: 1rem;
  font-size: 18px;
    font-weight: 600;
    color: #333;
}

/* Note Input */
.note-input {
  margin-bottom: 1rem;
}

.note-textarea {
  width: 100%;
  height: 150px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: vertical;
}

/* Action Button */
.action-btn {
  background-color: #4A90E2;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  margin-top: 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  width: 100%;
  transition: background-color 0.3s ease;
}

.button-group {
  display: flex;
  justify-content: flex-end; /* pushes button to the right */
}
.delete-btn {
  background-color: #2b90c5;
  color: white;
  border: none;
  padding: 0.4rem 0.8rem; /* smaller padding */
  margin: 0 0 1rem 0;  /* remove margin auto, not needed */
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem; /* smaller font */
  width: auto; /* keep button size based on content */
  transition: background-color 0.3s ease;
}
.action-btn:hover {
  background-color: #1871a1;
}

/* Saved Notes */
.saved-notes {
  margin-top: 1rem;
  text-align: left;
}

.saved-notes-title {
  margin-bottom: 0.5rem;
}

.saved-note {
  margin-bottom: 1rem;
}

.note-content {
  margin: 0;
}

.note-timestamp {
  font-size: 0.8rem;
  color: #aaa;
}

/* Agent Notes Panel */
.sidebar-panel {
  padding: 15px;
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.panel-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

/* Loading and Empty Notes Messages */
.loading-message,
.no-notes {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #6c757d;
}

.no-notes p {
  margin: 0;
}

/* Notes Table */
.notes-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.notes-table th,
.notes-table td {
  padding: 8px 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.notes-table th {
  font-weight: 600;
  color: #555;
  background-color: #f5f5f5;
}

/* Cell Styling */
.id-cell {
  width: 80px;
  font-weight: 500;
  color: #444;
}

.content-cell {
  max-width: 400px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #333;
}

.date-cell {
  color: #666;
  font-size: 13px;
}

/* Row Hover */
.note-row:hover {
  background-color: #f8f9fa;
}

</style>