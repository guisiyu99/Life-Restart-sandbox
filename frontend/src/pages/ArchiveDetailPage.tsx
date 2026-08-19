import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Button, Spin, Tag } from 'antd'
import AppLayout from '@/components/AppLayout'
import { gameService } from '@/services/gameService'
import type { FinishResult } from '@/types/game'
import './ArchiveDetailPage.css'

export default function ArchiveDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [data, setData] = useState<(FinishResult & { character_name: string }) | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    gameService
      .getArchive(Number(id))
      .then((res) => {
        if (res.data) {
          setData({
            ...res.data,
            character_name: gameService.loadCharacterName(Number(id)),
          })
        }
      })
      .finally(() => setLoading(false))
  }, [id])

  if (loading) {
    return (
      <AppLayout>
        <div style={{ padding: 80, textAlign: 'center' }}>
          <Spin />
        </div>
      </AppLayout>
    )
  }

  if (!data) {
    return (
      <AppLayout>
        <div className="archive-detail-page">
          <p>档案不存在</p>
          <Button onClick={() => navigate('/archives')}>返回列表</Button>
        </div>
      </AppLayout>
    )
  }

  return (
    <AppLayout
      showStats
      stats={{
        money: data.money,
        energy: data.energy,
        joy: data.joy,
        characterName: data.character_name,
      }}
    >
      <div className="archive-detail-page">
        <button type="button" className="back-link" onClick={() => navigate('/archives')}>
          ← 返回档案列表
        </button>
        <span className="history-badge">历史记录</span>
        <h1>{data.character_name}</h1>
        <div className="outcome-tags">
          {data.outcome_tags.map((t) => (
            <Tag key={t}>{t}</Tag>
          ))}
        </div>

        <div className="ai-summary">
          <h3>AI 人生总结</h3>
          <p>{data.ai_review}</p>
        </div>

        <div className="decision-list">
          <h3>生命轨迹溯源</h3>
          {data.decisions.map((d, i) => (
            <div key={i} className="decision-item">
              <strong>
                {d.age_range} · {d.theme}
              </strong>
              <p>{d.chosen_option}</p>
            </div>
          ))}
        </div>

        <div className="detail-actions">
          <Button type="primary" size="large" onClick={() => navigate('/game/new')}>
            基于此重开
          </Button>
          <Button size="large" onClick={() => navigate('/archives')}>
            返回档案列表
          </Button>
        </div>
      </div>
    </AppLayout>
  )
}
