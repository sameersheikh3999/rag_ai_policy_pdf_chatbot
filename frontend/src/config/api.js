// API Configuration
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001'

export const apiClient = {
  chat: async (question, includeWebSearch = true) => {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question,
        include_web_search: includeWebSearch
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response
  },

  evaluatePolicy: async (policyText) => {
    const response = await fetch(`${API_URL}/evaluate-policy`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ policy_text: policyText })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  },

  health: async () => {
    const response = await fetch(`${API_URL}/health`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return response.json()
  }
}

export default API_URL
