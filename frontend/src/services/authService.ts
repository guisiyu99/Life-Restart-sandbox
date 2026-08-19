import api from './api'
import type { LoginRequest, RegisterRequest, LoginResponse, RegisterResponse, User, ApiResponse } from '@/types/auth'
import {
  mockLoginSuccessResponse,
  mockLoginFailResponse,
  mockRegisterSuccessResponse,
  mockRegisterFailResponse,
  mockGetMeResponse,
} from '@/mocks/auth'

const useMock = import.meta.env.VITE_USE_MOCK === 'true'

export const authService = {
  async login(credentials: LoginRequest): Promise<ApiResponse<LoginResponse>> {
    if (useMock) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          if (credentials.email === 'test@example.com' && credentials.password === 'password') {
            resolve(mockLoginSuccessResponse)
          } else {
            reject({ response: { data: mockLoginFailResponse } })
          }
        }, 500)
      })
    }

    const response = await api.post<ApiResponse<LoginResponse>>('/auth/login', credentials)
    return response.data
  },

  async register(data: RegisterRequest): Promise<ApiResponse<RegisterResponse>> {
    if (useMock) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          if (data.email === 'existing@example.com') {
            reject({ response: { data: mockRegisterFailResponse } })
          } else {
            resolve(mockRegisterSuccessResponse)
          }
        }, 500)
      })
    }

    const response = await api.post<ApiResponse<RegisterResponse>>('/auth/register', data)
    return response.data
  },

  async getMe(): Promise<ApiResponse<User>> {
    if (useMock) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(mockGetMeResponse)
        }, 300)
      })
    }

    const response = await api.get<ApiResponse<User>>('/auth/me')
    return response.data
  },
}
