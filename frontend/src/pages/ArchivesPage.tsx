import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Spin } from 'antd'
import AppLayout from '@/components/AppLayout'
import { gameService } from '@/services/gameService'
import type { ArchiveItem } from '@/types/game'
import './ArchivesPage.css'

export default function ArchivesPage() {
  const navigate = useNavigate()
  const [items, setItems] = useState<ArchiveItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    gameService
      .getArchives()
      .then((res) => {
        if (res.data?.items) setItems(res.data.items)
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <AppLayout>
      <div className="archives-page">
        <button type="button" className="back-link" onClick={() => navigate('/home')}>
          ← 返回首页
        </button>
        <h1>历史人生档案</h1>
        <p className="archives-subtitle">回望每一个转折点，见证平行时空的可能。</p>

        {loading ? (
          <Spin />
        ) : items.length === 0 ? (
          <div className="archives-empty">
            <p>暂无人生档案</p>
            <button type="button" className="empty-cta" onClick={() => navigate('/game/new')}>
              创建角色
            </button>
          </div>
        ) : (
          <div className="archives-list">
            {items.map((item) => (
              <button
                key={item.id}
                type="button"
                className="archive-card"
                onClick={() => navigate(`/archives/${item.id}`)}
              >
                <div className="archive-main">
                  <strong>{gameService.loadCharacterName(item.id)}</strong>
                  <span className="archive-tag">{item.outcome_tags[0] ?? '人生'}</span>
                </div>
                <div className="archive-stats">
                  ¥{Math.round(item.money / 10000)}万 · 喜悦 {item.joy} · {item.decision_count} 次抉择
                </div>
                <div className="archive-date">{item.created_at.slice(0, 10)}</div>
              </button>
            ))}
          </div>
        )}
      </div>
    </AppLayout>
  )
}
