export interface User {
  id: number
  email: string
  username: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
  updated_at: string
}

export interface TestCase {
  id: string
  title: string
  description: string
  steps: string[]
  expected_result: string
}

export interface TestCaseResponse {
  message: string
  test_cases: TestCase[]
}

export interface History {
  id: number
  user_id: string
  query: string
  response: string
  testcases: string
  created_at: string
  updated_at: string
} 