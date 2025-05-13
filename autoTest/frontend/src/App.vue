<template>
  <div class="app">
    <nav-bar />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import NavBar from '@/components/NavBar.vue'
</script>

<style>
.app {
  min-height: 100vh;
  background-color: #f5f7fa;
}

body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style> 