<template>
  <div class="file-upload">
    <template v-if="!store.uploadedFilename">
      <el-upload
        class="upload-demo"
        drag
        :auto-upload="false"
        :before-upload="beforeUpload"
        :on-change="handleFileChange"
        :file-list="fileList"
        ref="uploadRef"
        :show-file-list="true"
        :limit="1"
        :on-remove="clearFiles"
        accept=".docx,.pdf"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持上传 Word 和 PDF 格式的需求文档
          </div>
        </template>
      </el-upload>
      <div class="upload-actions">
        <el-button 
          type="primary" 
          @click="submitUpload"
          :disabled="!fileList.length || store.loading"
        >
          {{ store.loading ? '上传中...' : '上传文件' }}
        </el-button>
        <el-button 
          @click="clearFiles"
          :disabled="!fileList.length || store.loading"
        >
          清空文件
        </el-button>
      </div>
    </template>

    <template v-else>
      <div class="uploaded-info">
        <el-icon style="color: #67c23a; font-size: 32px;"><upload-filled /></el-icon>
        <span class="filename">{{ store.uploadedFilename }}</span>
        <el-button type="danger" @click="clearFiles" size="small" plain>重新上传</el-button>
      </div>
      <div class="generate-actions">
        <el-button 
          type="success"
          @click="generateTestCases"
          :loading="store.loading"
          :disabled="!store.uploadedFilename"
        >
          生成测试用例
        </el-button>
      </div>
      <div class="testcase-list-area" v-if="store.loading">
        <el-skeleton :rows="3" animated />
      </div>
      <div class="testcase-list-area" v-else-if="store.error">
        <el-alert :title="store.error" type="error" show-icon />
      </div>
      <TestCaseList v-else-if="store.testCases.length > 0" />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useTestStore } from '../store'
import api, { cleanupFile } from '../utils/api'
import type { UploadInstance, UploadFile } from 'element-plus'
import { useRouter } from 'vue-router'
import TestCaseList from './TestCaseList.vue'

const store = useTestStore()
const fileList = ref<UploadFile[]>([])
const uploadRef = ref<UploadInstance>()
const router = useRouter()

const beforeUpload = (file: File) => {
  const isWord = file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  const isPDF = file.type === 'application/pdf'
  if (!isWord && !isPDF) {
    ElMessage.error('只能上传 Word 或 PDF 文件！')
    return false
  }
  return true
}

const handleFileChange = (file: any, fileListRaw: UploadFile[]) => {
  fileList.value = fileListRaw.slice(-1) // 只保留最新的一个文件
}

const submitUpload = async () => {
  if (!fileList.value.length) return
  store.setLoading(true)
  store.setError(null)
  try {
    const formData = new FormData()
    formData.append('file', fileList.value[0].raw as File)
    const response = await api.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    store.setUploadedFilename(response.data.filename)
    ElMessage.success('文件上传成功！请点击生成测试用例')
    fileList.value = [] // 上传成功后清空文件列表，触发 v-if 切换
  } catch (err: any) {
    store.setError(err?.response?.data?.detail || '上传失败')
    ElMessage.error('上传失败')
  } finally {
    store.setLoading(false)
  }
}

const clearFiles = async () => {
  fileList.value = []
  uploadRef.value?.clearFiles()
  if (store.uploadedFilename) {
    try {
      await cleanupFile(store.uploadedFilename)
    } catch (err) {
      console.error('清理文件失败:', err)
    }
  }
  store.setUploadedFilename('')
  store.clearTestCases()
  localStorage.removeItem('uploadedFilename')
}

const generateTestCases = async () => {
  if (!store.uploadedFilename) return
  store.setLoading(true)
  store.setError(null)
  try {
    const formData = new FormData()
    formData.append('filename', store.uploadedFilename)
    const response = await api.post('/generate', formData)
    store.setTestCases(response.data.test_cases)
    ElMessage.success('生成成功！')
    router.push('/generate')
    // 生成成功后清理文件
    // await clearFiles()
  } catch (err: any) {
    store.setError(err?.response?.data?.detail || '生成失败')
    ElMessage.error('生成失败')
  } finally {
    store.setLoading(false)
  }
}
</script>

<style scoped>
.file-upload {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.upload-demo {
  width: 100%;
  margin-bottom: 20px;
}

.upload-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
}
.generate-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
.uploaded-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin: 30px 0 20px 0;
}
.filename {
  font-size: 16px;
  color: #409EFF;
  font-weight: bold;
}
</style> 