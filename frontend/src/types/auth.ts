export interface User {
  id: number
  email: string
  created_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export interface RegisterRequest {
  email: string
  password: string
}

export interface RegisterResponse {
  access_token: string
  token_type: string
  user: User
}

export interface ApiResponse<T> {
  code: number
  message: string
  data: T | null
}
