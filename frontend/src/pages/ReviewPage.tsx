import { useNavigate, useParams, useLocation } from 'react-router-dom'
import { Button, Tag } from 'antd'
import AppLayout from '@/components/AppLayout'
import { gameService } from '@/services/gameService'
import type { FinishResult } from '@/types/game'
import './ReviewPage.css'

export default function ReviewPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const location = useLocation()
  const data = location.state as FinishResult | undefined
  const gameId = Number(id)
  const name = gameService.loadCharacterName(gameId)

  if (!data) {
    return (
      <AppLayout>
        <div className="review-page">
          <p>暂无回顾数据，请从对局完成页进入。</p>
          <Button onClick={() => navigate('/home')}>返回首页</Button>
        </div>
      </AppLayout>
    )
  }

  return (
    <AppLayout
      showStats
      stats={{ money: data.money, energy: data.energy, joy: data.joy, characterName: name }}
    >
      <div className="review-page">
        <h1>人生回顾</h1>
        <p className="review-meta">{name} · 22—70 岁</p>
        <div className="outcome-tags">
          {data.outcome_tags.map((tag) => (
            <Tag key={tag} color="purple" className="outcome-tag">
              {tag}
            </Tag>
          ))}
        </div>

        <div className="review-stats">
          <div className="review-stat">
            <span>最终金钱</span>
            <strong>¥{data.money.toLocaleString()}</strong>
          </div>
          <div className="review-stat">
            <span>精力</span>
            <strong>{data.energy}</strong>
          </div>
          <div className="review-stat">
            <span>喜悦</span>
            <strong>{data.joy}</strong>
          </div>
        </div>

        <div className="ai-summary">
          <h3>AI 人生总结</h3>
          <p>{data.ai_review}</p>
        </div>

        <div className="decision-list">
          <h3>关键抉择</h3>
          {data.decisions.map((d, i) => (
            <div key={i} className="decision-item">
              <strong>
                {d.age_range} · {d.theme}
              </strong>
              <p>
                {d.event_title} → {d.chosen_option}
              </p>
            </div>
          ))}
        </div>

        <div className="review-actions">
          <Button type="primary" size="large" onClick={() => navigate('/game/new')}>
            再来一次
          </Button>
          <Button size="large" onClick={() => navigate('/home')}>
            返回首页
          </Button>
        </div>
      </div>
    </AppLayout>
  )
}
