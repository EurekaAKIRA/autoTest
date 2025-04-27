<template>
  <div class="home">
    <el-card class="upload-card">
      <template #header>
        <div class="card-header">
          <span>上传需求文档</span>
        </div>
      </template>
      <FileUpload @upload-success="handleUploadSuccess" />
    </el-card>

    <el-card class="result-card" v-if="testCases.length > 0">
      <template #header>
        <div class="card-header">
          <span>生成的测试用例</span>
        </div>
      </template>
      <TestCaseList :test-cases="testCases" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import FileUpload from '../components/FileUpload.vue'
import TestCaseList from '../components/TestCaseList.vue'
import type { TestCase } from '../types'

const testCases = ref<TestCase[]>([])

const handleUploadSuccess = (cases: TestCase[]) => {
  testCases.value = cases
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.upload-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 