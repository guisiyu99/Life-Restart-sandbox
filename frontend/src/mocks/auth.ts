import type { User, LoginResponse, RegisterResponse, ApiResponse } from '@/types/auth'

export const mockUser: User = {
  id: 1,
  email: 'test@example.com',
  created_at: '2026-06-07T15:30:00Z',
}

export const mockLoginSuccessResponse: ApiResponse<LoginResponse> = {
  code: 200,
  message: 'success',
  data: {
    access_token: 'mock-jwt-token-12345',
    token_type: 'bearer',
    user: mockUser,
  },
}

export const mockLoginFailResponse: ApiResponse<null> = {
  code: 4001,
  message: '用户名或密码错误',
  data: null,
}

export const mockRegisterSuccessResponse: ApiResponse<RegisterResponse> = {
  code: 200,
  message: 'success',
  data: {
    access_token: 'mock-jwt-token-67890',
    token_type: 'bearer',
    user: mockUser,
  },
}

export const mockRegisterFailResponse: ApiResponse<null> = {
  code: 4003,
  message: '用户已存在',
  data: null,
}

export const mockGetMeResponse: ApiResponse<User> = {
  code: 200,
  message: 'success',
  data: mockUser,
}
