<template>
  <div class="file-upload">
    <el-upload
      class="upload-demo"
      drag
      action="/api/upload"
      :on-success="handleSuccess"
      :on-error="handleError"
      :before-upload="beforeUpload"
      accept=".docx,.pdf"
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        拖拽文件到此处或 <em>点击上传</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">
          支持 .docx 和 .pdf 格式的需求文档
        </div>
      </template>
    </el-upload>
  </div>
</template>

<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { TestCase } from '../types'

const emit = defineEmits<{
  (e: 'upload-success', cases: TestCase[]): void
}>()

const beforeUpload = (file: File) => {
  const isDocx = file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  const isPdf = file.type === 'application/pdf'
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isDocx && !isPdf) {
    ElMessage.error('只能上传 Word 或 PDF 文件!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB!')
    return false
  }
  return true
}

const handleSuccess = (response: any) => {
  if (response.test_cases && response.test_cases.length > 0) {
    emit('upload-success', response.test_cases)
    ElMessage.success('文件上传成功，已生成测试用例')
  } else {
    ElMessage.warning('文件上传成功，但未生成测试用例')
  }
}

const handleError = () => {
  ElMessage.error('文件上传失败')
}
</script>

<style scoped>
.file-upload {
  padding: 20px;
}

.upload-demo {
  width: 100%;
}
</style> 