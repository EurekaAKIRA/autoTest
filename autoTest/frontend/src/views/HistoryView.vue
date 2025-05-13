<template>
  <div class="history-view">
    <HistoryList />
  </div>
</template>

<script setup lang="ts">
import HistoryList from '@/components/HistoryList.vue'
</script>

<style scoped>
.history-view {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}
</style> 