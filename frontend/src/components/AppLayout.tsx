import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import './AppLayout.css'

interface AppLayoutProps {
  children: React.ReactNode
  showStats?: boolean
  stats?: { money: number; energy: number; joy: number; characterName?: string; ageLabel?: string }
}

export default function AppLayout({ children, showStats, stats }: AppLayoutProps) {
  const user = useAuthStore((s) => s.user)
  const clearAuth = useAuthStore((s) => s.clearAuth)
  const navigate = useNavigate()

  const logout = () => {
    clearAuth()
    navigate('/login')
  }

  return (
    <div className="app-layout">
      <header className="app-header">
        <div className="app-header-left">
          <Link to="/home" className="app-brand">
            重启人生沙盘模拟
          </Link>
          {stats?.characterName && (
            <span className="app-character">
              {stats.characterName}
              {stats.ageLabel && ` · ${stats.ageLabel}`}
            </span>
          )}
        </div>
        <div className="app-header-right">
          {showStats && stats && (
            <div className="stat-chips">
              <span className="stat-chip money">¥{stats.money.toLocaleString()}</span>
              <span className="stat-chip energy">精力 {stats.energy}</span>
              <span className="stat-chip joy">喜悦 {stats.joy}</span>
            </div>
          )}
          <span className="user-email">{user?.email}</span>
          <button type="button" className="logout-btn" onClick={logout}>
            退出
          </button>
        </div>
      </header>
      <main className="app-main">{children}</main>
      <footer className="app-footer">
        © 2026 重启人生沙盘模拟 - 所有的选择都是最好的安排
      </footer>
    </div>
  )
}
