import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Form, Input, Button, message } from 'antd'
import { authService } from '@/services/authService'
import { useAuthStore } from '@/stores/authStore'
import '@/styles/auth-layout.css'

export default function LoginPage() {
  const [loading, setLoading] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')
  const navigate = useNavigate()
  const setAuth = useAuthStore((state) => state.setAuth)

  const onFinish = async (values: { email: string; password: string }) => {
    setLoading(true)
    setErrorMsg('')
    try {
      const response = await authService.login(values)
      if (response.code === 200 && response.data) {
        setAuth(response.data.access_token, response.data.user)
        message.success('登录成功')
        navigate('/home')
      } else {
        setErrorMsg(response.message || '登录失败')
      }
    } catch (error: unknown) {
      const errMsg =
        (error as { response?: { data?: { message?: string } } })?.response?.data?.message ||
        '邮箱或密码错误，请重试'
      setErrorMsg(errMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-header">
          <h1 className="auth-title">欢迎回来</h1>
          <p className="auth-subtitle">登录后继续你的人生沙盘</p>
        </div>
        <Form name="login" onFinish={onFinish} layout="vertical" className="auth-form">
          <Form.Item label="邮箱" name="email" rules={[{ required: true, type: 'email', message: '请输入邮箱' }]}>
            <Input placeholder="name@example.com" size="large" className="auth-input" />
          </Form.Item>
          <Form.Item
            label="密码"
            name="password"
            rules={[{ required: true, message: '请输入密码' }]}
            validateStatus={errorMsg ? 'error' : ''}
            help={errorMsg}
          >
            <Input.Password placeholder="••••••••" size="large" className="auth-input" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" size="large" loading={loading} className="auth-button" block>
              登录
            </Button>
          </Form.Item>
        </Form>
        <div className="auth-footer">
          <Link to="/register" className="auth-link">
            还没有账号？立即注册
          </Link>
        </div>
        <div className="auth-divider" />
        <div className="auth-footer-note">© 2026 重启人生沙盘模拟 - 所有的选择都是最好的安排</div>
      </div>
    </div>
  )
}
