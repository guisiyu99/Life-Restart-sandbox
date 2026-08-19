import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { Input, Button, message } from 'antd'
import { MinusOutlined, PlusOutlined } from '@ant-design/icons'
import AppLayout from '@/components/AppLayout'
import { gameService } from '@/services/gameService'
import { DEFAULT_STATS } from '@/constants/game'
import './GameNewPage.css'

export default function GameNewPage() {
  const navigate = useNavigate()
  const [name, setName] = useState('林小然')
  const [money, setMoney] = useState<number>(DEFAULT_STATS.money)
  const [energy, setEnergy] = useState<number>(DEFAULT_STATS.energy)
  const [joy, setJoy] = useState<number>(DEFAULT_STATS.joy)
  const [loading, setLoading] = useState(false)

  const startGame = async () => {
    if (!name.trim()) {
      message.error('请输入角色姓名')
      return
    }
    setLoading(true)
    try {
      const res = await gameService.createGame({ character_name: name, money, energy, joy })
      if (res.code === 200 && res.data) {
        gameService.saveCharacterName(res.data.id, name.trim())
        navigate(`/game/${res.data.id}`)
      } else {
        message.error(res.message || '创建失败')
      }
    } catch (e) {
      if (axios.isAxiosError(e) && e.response?.status === 404) {
        message.error('游戏接口不可用，请确认后端已重启（需加载 /api/games 路由）')
      } else if (axios.isAxiosError(e)) {
        const data = e.response?.data as { message?: string } | undefined
        message.error(data?.message || '创建失败')
      } else {
        message.error('创建失败')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <AppLayout>
      <div className="game-new-page">
        <div className="step-badge">步骤 1/1 · 创建角色</div>
        <div className="game-new-grid">
          <div className="game-new-card">
            <h2>角色信息</h2>
            <label htmlFor="char-name">角色姓名</label>
            <Input id="char-name" value={name} onChange={(e) => setName(e.target.value)} size="large" maxLength={8} />
            <h3 className="stats-title">初始属性</h3>
            <StatRow label="金钱" value={`¥${money.toLocaleString()}`} onDec={() => setMoney((v) => Math.max(0, v - 5000))} onInc={() => setMoney((v) => v + 5000)} />
            <StatRow label="精力值" value={`${energy} 点`} onDec={() => setEnergy((v) => Math.max(0, v - 1))} onInc={() => setEnergy((v) => Math.min(20, v + 1))} />
            <StatRow label="喜悦值" value={`${joy}`} onDec={() => setJoy((v) => Math.max(0, v - 1))} onInc={() => setJoy((v) => Math.min(20, v + 1))} />
            <div className="hint-box">人生从 22 岁开始，共 8 个人生阶段。你当前每一个选择都将影响未来的可能。</div>
            <div className="game-new-actions">
              <Button onClick={() => navigate('/home')}>返回首页</Button>
              <Button type="primary" loading={loading} onClick={startGame} className="start-btn">
                开始人生
              </Button>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  )
}

function StatRow({
  label,
  value,
  onDec,
  onInc,
}: {
  label: string
  value: string
  onDec: () => void
  onInc: () => void
}) {
  return (
    <div className="stat-row">
      <span className="stat-label">{label}</span>
      <div className="stat-controls">
        <Button icon={<MinusOutlined />} onClick={onDec} size="small" />
        <span className="stat-value">{value}</span>
        <Button icon={<PlusOutlined />} onClick={onInc} size="small" />
      </div>
    </div>
  )
}
