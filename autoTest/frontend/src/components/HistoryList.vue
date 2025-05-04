<template>
  <div class="history-list">
    <h2>历史记录</h2>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="histories.length === 0" class="empty">暂无历史记录</div>
    <div v-else class="history-items">
      <div v-for="history in histories" :key="history.id" class="history-item">
        <div class="history-header">
          <span class="time">{{ formatDate(history.created_at) }}</span>
          <button @click="deleteHistory(history.id)" class="delete-btn">删除</button>
        </div>
        <div class="history-content">
          <div class="query">
            <strong>查询：</strong>
            <p>{{ history.query }}</p>
          </div>
          <div class="response">
            <strong>响应：</strong>
            <p>{{ history.response }}</p>
          </div>
          <button class="detail-btn" @click="toggleDetail(history.id)">
            {{ showDetailId === history.id ? '收起详情' : '查看详情' }}
          </button>
          <div v-if="showDetailId === history.id && parseTestcases(history.testcases).length > 0" class="testcase-detail">
            <div style="margin-bottom: 10px;">
              <button class="export-btn" @click="exportWord(history)">导出Word文档</button>
              <button class="export-btn" @click="exportScript(history)">导出脚本</button>
            </div>
            <div v-for="(tc, idx) in parseTestcases(history.testcases)" :key="tc.id || idx" class="testcase-block">
              <div><strong>用例{{ idx + 1 }}：</strong> {{ tc.title }}</div>
              <div>描述：{{ tc.description }}</div>
              <div>步骤：
                <ul>
                  <li v-for="(step, sidx) in tc.steps" :key="sidx">{{ step }}</li>
                </ul>
              </div>
              <div>预期结果：{{ tc.expected_result }}</div>
              <hr v-if="idx !== parseTestcases(history.testcases).length - 1" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="pagination" v-if="histories.length > 0">
      <button 
        :disabled="currentPage === 1" 
        @click="changePage(currentPage - 1)"
      >
        上一页
      </button>
      <span>第 {{ currentPage }} 页</span>
      <button 
        :disabled="histories.length < pageSize" 
        @click="changePage(currentPage + 1)"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { format } from 'date-fns'

interface TestCase {
  id: string
  title: string
  description: string
  steps: string[]
  expected_result: string
}

interface History {
  id: number
  query: string
  response: string
  testcases?: string
  created_at: string
}

const histories = ref<History[]>([])
const loading = ref(true)
const error = ref('')
const currentPage = ref(1)
const pageSize = 10
const showDetailId = ref<number | null>(null)

const fetchHistories = async () => {
  try {
    loading.value = true
    error.value = ''
    const skip = (currentPage.value - 1) * pageSize
    const response = await axios.get('/api/history', {
      params: { skip, limit: pageSize }
    })
    histories.value = response.data
  } catch (err) {
    error.value = '加载历史记录失败'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const deleteHistory = async (id: number) => {
  try {
    await axios.delete(`/api/history/${id}`)
    await fetchHistories()
  } catch (err) {
    error.value = '删除历史记录失败'
    console.error(err)
  }
}

const changePage = (page: number) => {
  currentPage.value = page
  fetchHistories()
}

const formatDate = (date: string) => {
  return format(new Date(date), 'yyyy-MM-dd HH:mm:ss')
}

function parseTestcases(testcases?: string): TestCase[] {
  if (!testcases) return []
  try {
    return JSON.parse(testcases)
  } catch {
    return []
  }
}

function toggleDetail(id: number) {
  showDetailId.value = showDetailId.value === id ? null : id
}

async function exportWord(history: History) {
  const testcases = parseTestcases(history.testcases)
  if (!testcases.length) return
  try {
    const response = await axios.post('/api/export_word', testcases, {
      responseType: 'blob',
      headers: { 'Content-Type': 'application/json' }
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'test_cases.docx')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    error.value = '导出Word文档失败'
    console.error(err)
  }
}

async function exportScript(history: History) {
  const testcases = parseTestcases(history.testcases)
  if (!testcases.length) return
  try {
    const response = await axios.post('/api/export_script', {
      test_cases: testcases,
      script_type: 'pytest'
    }, {
      responseType: 'blob',
      headers: { 'Content-Type': 'application/json' }
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'test_script_pytest.py')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    error.value = '导出脚本失败'
    console.error(err)
  }
}

onMounted(() => {
  fetchHistories()
})
</script>

<style scoped>
.history-list {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.history-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #fff;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.time {
  color: #666;
  font-size: 0.9em;
}

.delete-btn {
  background-color: #ff4444;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.delete-btn:hover {
  background-color: #cc0000;
}

.history-content {
  margin-top: 10px;
}

.query, .response {
  margin-bottom: 10px;
}

.query p, .response p {
  margin: 5px 0;
  white-space: pre-wrap;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.pagination button {
  padding: 5px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.loading, .error, .empty {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: #ff4444;
}

.detail-btn {
  margin: 10px 0;
  background: #1890ff;
  color: #fff;
  border: none;
  padding: 5px 12px;
  border-radius: 4px;
  cursor: pointer;
}
.detail-btn:hover {
  background: #40a9ff;
}
.testcase-detail {
  background: #f7faff;
  border: 1px solid #e6f7ff;
  border-radius: 6px;
  padding: 12px;
  margin-top: 10px;
}
.testcase-block {
  margin-bottom: 10px;
}
.export-btn {
  margin-right: 10px;
  background: #52c41a;
  color: #fff;
  border: none;
  padding: 5px 12px;
  border-radius: 4px;
  cursor: pointer;
}
.export-btn:last-child {
  margin-right: 0;
  background: #faad14;
}
.export-btn:hover {
  opacity: 0.85;
}
</style> 