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