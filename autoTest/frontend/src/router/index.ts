import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import HistoryView from '../views/HistoryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/history',
      name: 'history',
      component: HistoryView
    }
  ]
})

// 路由守卫相关内容已移除，专注核心功能

export default router 