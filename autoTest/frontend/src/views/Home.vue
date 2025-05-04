<template>
  <div class="home">
    <el-container>
      <el-header>
        <h1>测试用例生成器</h1>
      </el-header>
      
      <el-main>
        <el-row :gutter="20">
          <el-col :span="24">
            <file-upload />
          </el-col>
        </el-row>

        <el-row :gutter="20" class="mt-4">
          <el-col :span="24">
            <el-card v-if="store.testCases && store.testCases.length > 0">
              <template #header>
                <div class="card-header">
                  <span>生成的测试用例</span>
                  <div class="header-actions">
                    <el-button-group>
                      <el-button type="primary" @click="handleExportWord">
                        <el-icon><document /></el-icon>
                        导出Word
                      </el-button>
                      <el-button type="success" @click="handleExportScript">
                        <el-icon><document /></el-icon>
                        导出脚本
                      </el-button>
                    </el-button-group>
                  </div>
                </div>
              </template>
              <test-case-list />
            </el-card>
          </el-col>
        </el-row>
      </el-main>
      
      <el-footer>
        <p>© 2024 测试用例生成系统</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { Document } from '@element-plus/icons-vue'
import FileUpload from '@/components/FileUpload.vue'
import TestCaseList from '@/components/TestCaseList.vue'
import { useTestStore } from '@/store'
import { exportWord, exportScript } from '@/utils/api'

const store = useTestStore()

const handleExportWord = async () => {
  if (!store.testCases || store.testCases.length === 0) {
    ElMessage.warning('没有可导出的测试用例')
    return
  }
  
  try {
    const response = await exportWord(store.testCases)
    const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = '测试用例.docx'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const handleExportScript = async () => {
  if (!store.testCases || store.testCases.length === 0) {
    ElMessage.warning('没有可导出的测试用例')
    return
  }
  
  try {
    const response = await exportScript(store.testCases)
    const blob = new Blob([response], { type: 'text/plain' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'test_cases.py'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.el-container {
  min-height: 100vh;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
}

.el-header h1 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.el-main {
  padding: 20px;
}

.mt-4 {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.el-footer {
  text-align: center;
  padding: 20px;
  background-color: #f5f7fa;
  color: #666;
}
</style> 