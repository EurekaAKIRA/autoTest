import { defineStore } from 'pinia'
import type { TestCase } from '../types'

export const useTestStore = defineStore('test', {
  state: () => ({
    testCases: [] as TestCase[],
    loading: false,
    error: null as string | null,
    uploadedFilename: (localStorage.getItem('uploadedFilename') || '') as string
  }),

  actions: {
    setTestCases(cases: TestCase[]) {
      this.testCases = cases
      this.loading = false
      this.error = null
    },

    setLoading(status: boolean) {
      this.loading = status
      if (status) {
        this.error = null
      }
    },

    setError(message: string | null) {
      this.error = message
      this.loading = false
    },

    clearTestCases() {
      this.testCases = []
      this.error = null
    },

    setUploadedFilename(name: string) {
      this.uploadedFilename = name
      if (name) {
        localStorage.setItem('uploadedFilename', name)
      } else {
        localStorage.removeItem('uploadedFilename')
      }
    }
  }
})
