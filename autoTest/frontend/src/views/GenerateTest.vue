<template>
  <div class="generate-test">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1>测试用例生成器</h1>
          <div class="header-actions">
            <el-button type="primary" @click="goHome">
              <el-icon><HomeFilled /></el-icon>
              返回首页
            </el-button>
          </div>
        </div>
      </el-header>
      <el-main class="main-content">
        <el-row :gutter="20" class="content-row">
          <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
            <el-card class="upload-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>文件上传</span>
                  <el-tag type="info" size="small">支持 Word/PDF</el-tag>
                </div>
              </template>
              <FileUpload />
            </el-card>
          </el-col>
        </el-row>
      </el-main>
      <el-footer class="footer">
        <p>© 2024 测试用例生成器 | 版本 1.0.0</p>
      </el-footer>
    </el-container>
    <GuidePopover />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { HomeFilled } from '@element-plus/icons-vue'
import FileUpload from '../components/FileUpload.vue'
import GuidePopover from '../components/GuidePopover.vue'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.generate-test {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #409EFF 0%, #1e88e5 100%);
  color: white;
  padding: 0 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  width: 100%;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.main-content {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.content-row {
  width: 100%;
  max-width: 1200px;
  display: flex;
  justify-content: center;
}

.upload-card {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  box-sizing: border-box;
  padding: 20px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.upload-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 0 16px 0;
  border-bottom: 1px solid #ebeef5;
}

.footer {
  background-color: #f5f7fa;
  color: #606266;
  text-align: center;
  padding: 20px 0;
  font-size: 14px;
  width: 100%;
  border-top: 1px solid #ebeef5;
}

@media (max-width: 1000px) {
  .header-content {
    padding: 0 10px;
  }
  
  .main-content {
    padding: 20px 10px;
  }
  
  .upload-card {
    padding: 15px;
  }
}
</style> 