<template>
  <nav class="navbar">
    <div class="nav-brand">
      <router-link to="/">测试用例生成系统</router-link>
    </div>
    <div class="nav-links">
      <router-link to="/" class="nav-link">首页</router-link>
      <router-link to="/history" class="nav-link">历史记录</router-link>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background-color: #fff;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand a {
  color: #333;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: #666;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: #333;
  background-color: #f5f5f5;
}

.router-link-active {
  color: #1890ff;
  background-color: #e6f7ff;
}
</style> 