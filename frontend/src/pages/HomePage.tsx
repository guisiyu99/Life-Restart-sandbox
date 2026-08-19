import { useNavigate } from 'react-router-dom'
import AppLayout from '@/components/AppLayout'
import './HomePage.css'

export default function HomePage() {
  const navigate = useNavigate()

  return (
    <AppLayout>
      <div className="home-page">
        <div className="home-hero">
          <h1 className="home-title">
            重启人生<span className="home-title-accent">沙盘模拟</span>
          </h1>
          <p className="home-subtitle">八段人生旅程，探索另一种可能</p>
          <div className="home-actions">
            <button type="button" className="home-btn primary" onClick={() => navigate('/game/new')}>
              创建角色 →
            </button>
            <button type="button" className="home-btn secondary" onClick={() => navigate('/archives')}>
              历史人生档案
            </button>
          </div>
        </div>
      </div>
    </AppLayout>
  )
}
