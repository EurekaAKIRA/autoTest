<template>
  <div class="test-case-list">
    <el-collapse v-model="activeNames">
      <el-collapse-item
        v-for="testCase in testCases"
        :key="testCase.id"
        :title="testCase.title"
        :name="testCase.id"
      >
        <div class="test-case-content">
          <h3>描述</h3>
          <p>{{ testCase.description }}</p>
          
          <h3>测试步骤</h3>
          <ol>
            <li v-for="(step, index) in testCase.steps" :key="index">
              {{ step }}
            </li>
          </ol>
          
          <h3>预期结果</h3>
          <p>{{ testCase.expected_result }}</p>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { TestCase } from '../types'

const props = defineProps<{
  testCases: TestCase[]
}>()

const activeNames = ref<string[]>([])
</script>

<style scoped>
.test-case-list {
  padding: 20px;
}

.test-case-content {
  padding: 10px;
}

h3 {
  margin: 15px 0 10px;
  color: #409EFF;
}

ol {
  padding-left: 20px;
}

li {
  margin: 5px 0;
}
</style> 