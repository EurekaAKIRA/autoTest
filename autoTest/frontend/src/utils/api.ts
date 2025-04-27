import axios from 'axios'
import type { TestCaseResponse } from '../types'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const uploadDocument = async (file: File): Promise<TestCaseResponse> => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post<TestCaseResponse>('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  
  return response.data
}

export default api 