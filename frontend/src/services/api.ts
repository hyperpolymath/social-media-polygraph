import axios from 'axios'
import type { ClaimCreate, ClaimResponse, ClaimAnalysis, Claim } from '@/types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const claimsApi = {
  verifyClaim: async (data: ClaimCreate): Promise<ClaimResponse> => {
    const response = await api.post<ClaimResponse>('/api/v1/claims/verify', data)
    return response.data
  },

  getClaim: async (claimId: string): Promise<ClaimAnalysis> => {
    const response = await api.get<ClaimAnalysis>(`/api/v1/claims/${claimId}`)
    return response.data
  },

  listClaims: async (params?: {
    skip?: number
    limit?: number
    status?: string
  }): Promise<Claim[]> => {
    const response = await api.get<Claim[]>('/api/v1/claims/', { params })
    return response.data
  },

  getClaimHistory: async (claimId: string): Promise<any[]> => {
    const response = await api.get<any[]>(`/api/v1/claims/${claimId}/history`)
    return response.data
  },
}

export const authApi = {
  register: async (data: {
    email: string
    username: string
    password: string
    full_name?: string
  }) => {
    const response = await api.post('/api/v1/auth/register', data)
    return response.data
  },

  login: async (username: string, password: string) => {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    const response = await api.post('/api/v1/auth/login', formData)
    return response.data
  },

  getCurrentUser: async () => {
    const response = await api.get('/api/v1/auth/me')
    return response.data
  },
}

export default api
