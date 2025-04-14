<!-- AddNotes -->
<script setup>
import { ref, onMounted } from 'vue';

const showNoteBox = ref(false);
const noteContent = ref('');
const savedNotes = ref([]);

onMounted(() => {
  const storedNotes = localStorage.getItem('savedNotes');
  if (storedNotes) {
    savedNotes.value = JSON.parse(storedNotes);
  }
});

const saveNote = () => {
  if (noteContent.value.trim() !== '') {
    savedNotes.value.push({
      content: noteContent.value,
      timestamp: new Date().toLocaleString()
    });

    localStorage.setItem('savedNotes', JSON.stringify(savedNotes.value));

    noteContent.value = '';
    showNoteBox.value = false;
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
const deleteNote = (index) => {
  savedNotes.value.splice(index, 1); // Remove from array
  localStorage.setItem('savedNotes', JSON.stringify(savedNotes.value)); // Update localStorage
};
</script>

<template>
  <div>
      <div class="sidebar-panel">
      <h3 class="panel-title">Customer Notes</h3>

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
            <button class="delete-btn" @click="deleteNote(index)">
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

</style>