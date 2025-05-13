<template>
  <div class="nav-bar-wrapper">
    <el-menu
      :default-active="activeIndex"
      class="nav-menu"
      mode="horizontal"
      router
    >
      <el-menu-item index="/">测试用例生成器</el-menu-item>
      
      <div class="flex-grow" />
      
      <template v-if="!userStore.user">
        <el-menu-item index="/login">登录</el-menu-item>
      </template>
    </el-menu>
    <template v-if="userStore.user">
      <div class="user-menu-area">
        <el-dropdown trigger="click">
          <span class="user-dropdown-trigger">
            <el-avatar :size="32" class="user-avatar">
              {{ userStore.user.username.charAt(0).toUpperCase() }}
            </el-avatar>
            <span class="username">{{ userStore.user.username }}</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'
import { getCurrentUser } from '@/utils/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const activeIndex = ref(route.path)

onMounted(async () => {
  if (userStore.token && !userStore.user) {
    try {
      const user = await getCurrentUser()
      userStore.setUser(user)
    } catch (error) {
      userStore.logout()
    }
  }
})

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.nav-bar-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
}

.nav-menu {
  padding: 0 20px;
  display: flex;
  align-items: center;
}

.flex-grow {
  flex-grow: 1;
}

.user-avatar {
  margin-right: 8px;
  background-color: #409EFF;
  color: white;
}

.username {
  margin-left: 8px;
}

.user-dropdown-trigger {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0 12px;
  height: 60px;
}

/* 彻底隐藏下拉箭头 */
:deep(.el-dropdown) {
  display: flex;
  align-items: center;
}

:deep(.el-dropdown__caret),
:deep(.el-dropdown__caret-button),
:deep(.el-dropdown__caret-button::before),
:deep(.el-dropdown__caret-button::after) {
  display: none !important;
  opacity: 0 !important;
  visibility: hidden !important;
  width: 0 !important;
  height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
}

/* 优化下拉菜单样式 */
:deep(.el-dropdown-menu) {
  margin-top: 0;
  padding: 4px 0;
  min-width: 100px;
}

:deep(.el-dropdown-menu__item) {
  padding: 8px 16px;
  font-size: 14px;
  line-height: 1.5;
}

:deep(.el-dropdown-menu__item:hover) {
  background-color: #f5f7fa;
}

/* 确保下拉菜单正确定位 */
:deep(.el-popper) {
  margin-top: 0 !important;
}

:deep(.el-sub-menu__icon-more) {
  display: none !important;
}

.user-menu-area {
  display: flex;
  align-items: center;
  margin-right: 24px;
  margin-left: auto;
}
</style> 