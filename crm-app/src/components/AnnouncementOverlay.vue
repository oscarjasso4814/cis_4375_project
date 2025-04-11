<script setup>
const announcementMessage = "";
const videoUrl = "https://www.youtube.com/embed/tMya2WkbQgM";
</script>

<template>
  <div class="overlay">
    <h3 class="header">📣 Company Announcement</h3>
    <p class="message">{{ announcementMessage }}</p>
    <div class="video-container">
      <iframe
        :src="videoUrl"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  display: flex;
  flex-direction: column;
  height: 100%; /* Make the overlay fill the parent box */
  background: #fffae6;
  border: 2px solid #ffd700;
  padding: 10px;
  border-radius: 8px;
  font-size: 14px;
  color: #000; /* Changed text color to black for better contrast */
}

.header {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  color: #000; /* Ensure header text is black */
}

.message {
  margin: 5px 0 0px;
  text-align: center;
  color: #000; /* Ensure message text is black */
}

.video-container {
  flex: 1; /* Allow the video container to take up the remaining space */
  position: relative;
  width: 100%;
  height: 100%; /* Fill the available height */
  overflow: hidden;
  border-radius: 8px;
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%; /* Ensure the iframe fills the container */
  border-radius: 8px;
}
</style>