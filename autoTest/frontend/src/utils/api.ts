import axios from 'axios'
import { ElMessage } from 'element-plus'
import type { TestCase, User } from '../types'

// 创建 axios 实例
const api = axios.create({
  baseURL: '/'
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 如果是FormData，不设置Content-Type
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// 用户相关 API
export const login = async (email: string, password: string) => {
  const formData = new FormData()
  formData.append('username', email)
  formData.append('password', password)
  const response = await api.post('/auth/token', formData)
  return response.data
}

export const register = async (data: { email: string; password: string; username: string }) => {
  const response = await api.post('/auth/register', data)
  return response.data
}

export const getCurrentUser = async () => {
  const response = await api.get('/api/me')
  return response.data
}

// 测试用例相关 API
export const uploadDocument = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await api.post('/api/upload', formData)
  return response.data
}

export const generateTestCases = async (filename: string, originalFilename: string): Promise<TestCase[]> => {
  const formData = new FormData()
  formData.append('filename', filename)
  formData.append('original_filename', originalFilename)
  const response = await api.post('/api/generate', formData)
  return response.data.test_cases
}

export const cleanupFile = async (filename: string) => {
  const response = await api.delete(`/api/cleanup/${filename}`)
  return response.data
}

export const exportWord = async (testCases: TestCase[]) => {
  const response = await api.post('/api/export_word', testCases, {
    responseType: 'blob'
  })
  return response.data
}

export const exportScript = async (testCases: TestCase[], scriptType: string = 'pytest') => {
  const response = await api.post('/api/export_script', {
    test_cases: testCases,
    script_type: scriptType
  }, {
    responseType: 'blob',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  return response.data
}

// 历史记录相关 API
export const getHistory = async (skip: number = 0, limit: number = 10) => {
  const response = await api.get(`/api/history?skip=${skip}&limit=${limit}`)
  return response.data
}

export const deleteHistory = async (historyId: number) => {
  const response = await api.delete(`/api/history/${historyId}`)
  return response.data
}

export default api 