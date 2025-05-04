import axios from 'axios'
import { ElMessage } from 'element-plus'
import { TestCase } from '../types'

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api'
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
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
    return Promise.reject(error)
  }
)

// API 接口定义
export const uploadDocument = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await api.post('/upload', formData)
  return response.data
}

export const generateTestCases = async (filename: string, originalFilename: string): Promise<TestCase[]> => {
  const formData = new FormData()
  formData.append('filename', filename)
  formData.append('original_filename', originalFilename)
  const response = await api.post('/generate', formData)
  return response.data.test_cases
}

export const cleanupFile = async (filename: string) => {
  const response = await api.delete(`/cleanup/${filename}`)
  return response.data
}

export const exportWord = async (testCases: any[]) => {
  const response = await api.post('/export_word', testCases, {
    responseType: 'blob'
  })
  return response.data
}

export const exportScript = async (testCases: any[], scriptType: string = 'pytest') => {
  const response = await api.post('/export_script', {
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

export default api 