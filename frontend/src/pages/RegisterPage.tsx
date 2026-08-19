import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Form, Input, Button, message } from 'antd'
import { authService } from '@/services/authService'
import { useAuthStore } from '@/stores/authStore'
import '@/styles/auth-layout.css'

export default function RegisterPage() {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const setAuth = useAuthStore((s) => s.setAuth)

  const onFinish = async (values: { email: string; password: string; confirm: string }) => {
    if (values.password !== values.confirm) {
      message.error('两次密码输入不一致')
      return
    }
    setLoading(true)
    try {
      const response = await authService.register({ email: values.email, password: values.password })
      if (response.code === 200 && response.data) {
        setAuth(response.data.access_token, response.data.user)
        message.success('注册成功')
        navigate('/home')
      }
    } catch (error: unknown) {
      const errMsg =
        (error as { response?: { data?: { message?: string } } })?.response?.data?.message ||
        '注册失败，请重试'
      message.error(errMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card register-card">
        <div className="auth-header">
          <h1 className="auth-title">创建账号</h1>
          <p className="auth-subtitle">开启你的第一段虚拟人生</p>
        </div>
        <Form name="register" onFinish={onFinish} layout="vertical" className="auth-form">
          <Form.Item label="邮箱" name="email" rules={[{ required: true, type: 'email' }]}>
            <Input placeholder="example@life.com" size="large" className="auth-input" />
          </Form.Item>
          <Form.Item label="密码" name="password" rules={[{ required: true, min: 6 }]}>
            <Input.Password size="large" className="auth-input" />
          </Form.Item>
          <Form.Item label="确认密码" name="confirm" rules={[{ required: true }]}>
            <Input.Password size="large" className="auth-input" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" size="large" loading={loading} className="auth-button" block>
              注册并登录
            </Button>
          </Form.Item>
        </Form>
        <div className="auth-footer">
          <Link to="/login" className="auth-link">
            已有账号？去登录 →
          </Link>
        </div>
        <div className="auth-divider" />
        <div className="auth-footer-note">人生模拟器 v2.0</div>
      </div>
    </div>
  )
}
