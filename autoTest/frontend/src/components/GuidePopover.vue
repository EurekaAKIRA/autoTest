<template>
  <div class="guide-popover">
    <el-popover
      v-model:visible="visible"
      placement="right"
      :width="300"
      trigger="manual"
    >
      <template #reference>
        <el-button 
          type="info" 
          :icon="QuestionFilled" 
          circle 
          class="guide-button"
          @click="toggleGuide"
        />
      </template>
      <template #default>
        <div class="guide-content">
          <h4>使用指南</h4>
          <ol>
            <li>上传 Word 或 PDF 格式的需求文档（最大 10MB）</li>
            <li>等待文件上传完成</li>
            <li>点击"生成测试用例"按钮</li>
            <li>等待系统分析文档并生成测试用例</li>
            <li>查看生成的测试用例列表</li>
          </ol>
          <div class="guide-footer">
            <el-checkbox v-model="dontShowAgain">不再显示</el-checkbox>
            <el-button type="primary" size="small" @click="closeGuide">
              知道了
            </el-button>
          </div>
        </div>
      </template>
    </el-popover>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { QuestionFilled } from '@element-plus/icons-vue'

const visible = ref(false)
const dontShowAgain = ref(false)

const toggleGuide = () => {
  visible.value = !visible.value
}

const closeGuide = () => {
  visible.value = false
  if (dontShowAgain.value) {
    localStorage.setItem('hideGuide', 'true')
  }
}

onMounted(() => {
  const hideGuide = localStorage.getItem('hideGuide')
  if (!hideGuide) {
    visible.value = true
  }
})
</script>

<style scoped>
.guide-popover {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 1000;
}

.guide-button {
  opacity: 0.6;
  transition: opacity 0.3s;
}

.guide-button:hover {
  opacity: 1;
}

.guide-content {
  padding: 10px;
}

.guide-content h4 {
  margin-top: 0;
  margin-bottom: 12px;
  color: #303133;
}

.guide-content ol {
  margin: 0;
  padding-left: 20px;
  color: #606266;
}

.guide-content li {
  margin-bottom: 8px;
  line-height: 1.4;
}

.guide-footer {
  margin-top: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 