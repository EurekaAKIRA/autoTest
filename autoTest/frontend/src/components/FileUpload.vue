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
            支持上传 Word 和 PDF 格式的需求文档（最大 10MB）
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
        <span class="filename">{{ store.originalFilename }}</span>
        <el-button type="danger" @click="clearFiles" size="small" plain>重新上传</el-button>
      </div>
      <div class="generate-actions">
        <el-button 
          type="success"
          @click="handleGenerateTestCases"
          :loading="store.loading"
          :disabled="!store.uploadedFilename"
        >
          生成测试用例
        </el-button>
      </div>
      <div class="testcase-list-area" v-if="store.loading">
        <div class="generation-progress">
          <el-progress 
            :percentage="generationProgress.percentage" 
            :status="generationProgress.status"
          >
            <template #default="{ percentage }">
              <span class="progress-text">{{ generationProgress.text }}</span>
            </template>
          </el-progress>
        </div>
      </div>
      <div class="testcase-list-area" v-else-if="store.error">
        <el-alert
          :title="store.error"
          type="error"
          show-icon
          class="error-alert"
        />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage, ElLoading } from 'element-plus'
import { useTestStore } from '../store'
import { uploadDocument, cleanupFile, generateTestCases } from '../utils/api'
import type { UploadInstance, UploadFile } from 'element-plus'
import { useRouter } from 'vue-router'
import TestCaseList from './TestCaseList.vue'

const store = useTestStore()
const fileList = ref<UploadFile[]>([])
const uploadRef = ref<UploadInstance>()
const router = useRouter()

const generationProgress = reactive({
  percentage: 0,
  status: '' as '' | 'success' | 'exception' | 'warning',
  text: '准备中...'
})

const beforeUpload = (file: File) => {
  const isWord = file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  const isPDF = file.type === 'application/pdf'
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isWord && !isPDF) {
    ElMessage.error('只能上传 Word 或 PDF 文件！')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB！')
    return false
  }
  return true
}

const handleFileChange = (file: any, fileListRaw: UploadFile[]) => {
  fileList.value = fileListRaw.slice(-1)
}

const submitUpload = async () => {
  if (!fileList.value.length) return
  store.setLoading(true)
  store.setError(null)
  try {
    const file = fileList.value[0].raw as File
    const response = await uploadDocument(file)
    store.setUploadedFilename(response.filename)
    store.setOriginalFilename(file.name)
    ElMessage.success('文件上传成功！请点击生成测试用例')
    fileList.value = []
  } catch (err) {
    const errorMessage = err instanceof Error ? err.message : '上传失败'
    store.setError(errorMessage)
    store.setTestCases([])
    ElMessage.error(errorMessage)
  } finally {
    store.setLoading(false)
  }
}

const clearFiles = async () => {
  fileList.value = []
  uploadRef.value?.clearFiles()
  if (store.uploadedFilename) {
    await cleanupFile(store.uploadedFilename)
  }
  store.setUploadedFilename('')
  store.setOriginalFilename('')
  store.clearTestCases()
  localStorage.removeItem('uploadedFilename')
  localStorage.removeItem('originalFilename')
}

const handleGenerateTestCases = async () => {
  if (!store.uploadedFilename) {
    ElMessage.warning('请先上传文件')
    return
  }
  
  if (store.loading) {
    ElMessage.warning('正在生成中，请稍候...')
    return
  }
  
  store.setLoading(true)
  store.setError(null)
  
  const loadingInstance = ElLoading.service({
    lock: true,
    text: '正在生成测试用例，请稍候...',
    background: 'rgba(0, 0, 0, 0.7)'
  })
  
  try {
    const testCases = await generateTestCases(store.uploadedFilename)
    store.setTestCases(testCases)
    ElMessage.success('测试用例生成成功！')
  } catch (err) {
    const errorMessage = err instanceof Error ? err.message : '生成失败'
    store.setError(errorMessage)
    store.setTestCases([])
    ElMessage.error(errorMessage)
  } finally {
    store.setLoading(false)
    loadingInstance.close()
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

.generation-progress {
  margin: 20px 0;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.progress-text {
  font-size: 14px;
  color: #606266;
}

.error-alert {
  margin-top: 20px;
}
</style> 