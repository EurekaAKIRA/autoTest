<template>
  <div class="test-case-list">
    <el-collapse v-model="activeNames">
      <el-collapse-item
        v-for="testCase in store.testCases"
        :key="testCase.id"
        :name="testCase.id"
      >
        <template #title>
          <div class="test-case-header">
            <span class="test-case-title">{{ testCase.title }}</span>
            <el-tag size="small" type="info">ID: {{ testCase.id }}</el-tag>
          </div>
        </template>
        <div class="test-case-content">
          <div class="test-case-section">
            <h4>描述</h4>
            <p>{{ testCase.description }}</p>
          </div>
          <div class="test-case-section">
            <h4>测试步骤</h4>
            <ol>
              <li v-for="(step, index) in testCase.steps" :key="index">
                {{ step }}
              </li>
            </ol>
          </div>
          <div class="test-case-section">
            <h4>预期结果</h4>
            <p>{{ testCase.expected_result }}</p>
          </div>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useTestStore } from '@/store'
import type { TestCase } from '../types'
import { exportWord, exportScript } from '../utils/api'
import { ElMessage } from 'element-plus'

const store = useTestStore()
const activeNames = ref<string[]>([])
const scriptType = ref('pytest')

const exportWord = async () => {
  if (!store.testCases.length) {
    ElMessage.warning('没有可导出的测试用例')
    return
  }
  try {
    console.log('开始导出Word:', store.testCases.length, '个测试用例')
    const blob = await exportWord(store.testCases)
    if (!(blob instanceof Blob)) {
      throw new Error('导出格式错误')
    }
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'test_cases.docx')
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (err) {
    console.error('导出Word失败:', err)
    ElMessage.error(err instanceof Error ? err.message : '导出Word失败')
  }
}

const exportScript = async () => {
  if (!store.testCases.length) {
    ElMessage.warning('没有可导出的测试用例')
    return
  }
  try {
    console.log('开始导出脚本:', store.testCases.length, '个测试用例, 类型:', scriptType.value)
    const blob = await exportScript(store.testCases, scriptType.value)
    if (!(blob instanceof Blob)) {
      throw new Error('导出格式错误')
    }
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `test_cases_${scriptType.value}.py`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (err) {
    console.error('导出脚本失败:', err)
    ElMessage.error(err instanceof Error ? err.message : '导出脚本失败')
  }
}
</script>

<style scoped>
.test-case-list {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
}
.el-collapse-item__content {
  padding: 24px 32px;
  font-size: 16px;
}
.test-case-header {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 10px;
}
.test-case-title {
  font-weight: 500;
}
.test-case-content {
  padding: 10px 0;
}
.test-case-section {
  margin-bottom: 20px;
}
.test-case-section h4 {
  margin: 0 0 10px 0;
  color: #606266;
}
.test-case-section p {
  margin: 0;
  color: #606266;
  line-height: 1.6;
}
.test-case-section ol {
  margin: 0;
  padding-left: 20px;
}
.test-case-section li {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 5px;
}
</style> 