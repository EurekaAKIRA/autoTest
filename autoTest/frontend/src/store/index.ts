import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TestCase } from '../types'

export const useTestStore = defineStore('test', () => {
  const uploadedFilename = ref<string>('')
  const originalFilename = ref<string>('')
  const testCases = ref<TestCase[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const setUploadedFilename = (filename: string) => {
    uploadedFilename.value = filename
    localStorage.setItem('uploadedFilename', filename)
  }

  const setOriginalFilename = (filename: string) => {
    originalFilename.value = filename
    localStorage.setItem('originalFilename', filename)
  }

  const setTestCases = (cases: TestCase[]) => {
    testCases.value = cases
  }

  const setLoading = (value: boolean) => {
    loading.value = value
  }

  const setError = (message: string | null) => {
    error.value = message
  }

  const clearTestCases = () => {
    testCases.value = []
  }

  // 从 localStorage 恢复状态
  const restoreState = () => {
    const savedFilename = localStorage.getItem('uploadedFilename')
    const savedOriginalFilename = localStorage.getItem('originalFilename')
    if (savedFilename) uploadedFilename.value = savedFilename
    if (savedOriginalFilename) originalFilename.value = savedOriginalFilename
  }

  return {
    uploadedFilename,
    originalFilename,
    testCases,
    loading,
    error,
    setUploadedFilename,
    setOriginalFilename,
    setTestCases,
    setLoading,
    setError,
    clearTestCases,
    restoreState
  }
}) 