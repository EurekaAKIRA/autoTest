<template>
  <el-container>
    <el-header>
      <h1>测试用例生成系统</h1>
    </el-header>
    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
// 组件逻辑
</script>

<style>
.el-header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  line-height: 60px;
}

.el-main {
  padding: 20px;
}
</style> 