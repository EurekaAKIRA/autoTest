import { defineStore } from 'pinia'
import type { TestCase } from '../types'

export const useTestStore = defineStore('test', {
  state: () => ({
    testCases: [] as TestCase[],
    loading: false,
    error: null as string | null
  }),
  
  actions: {
    setTestCases(cases: TestCase[]) {
      this.testCases = cases
    },
    
    setLoading(status: boolean) {
      this.loading = status
    },
    
    setError(message: string | null) {
      this.error = message
    }
  }
}) 