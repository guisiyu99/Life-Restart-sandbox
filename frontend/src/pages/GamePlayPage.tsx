import { useCallback, useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Button, message, Spin } from 'antd'
import AppLayout from '@/components/AppLayout'
import { gameService } from '@/services/gameService'
import {
  AGE_ROUNDS,
  canPickCircleOnly,
  canPickTheme,
  CAREER_THEMES,
  getEventsPerRound,
  isFullyRandom,
  LIFE_THEMES,
} from '@/constants/game'
import { employmentStatusLabel } from '@/constants/employment'
import type { CircleType, Game, GameEvent } from '@/types/game'
import './GamePlayPage.css'

export default function GamePlayPage() {
  const { id } = useParams<{ id: string }>()
  const gameId = Number(id)
  const navigate = useNavigate()

  const [game, setGame] = useState<Game | null>(null)
  const [loading, setLoading] = useState(true)
  const [circle, setCircle] = useState<CircleType>('life')
  const [theme, setTheme] = useState<string>(LIFE_THEMES[0])
  const [currentEvent, setCurrentEvent] = useState<GameEvent | null>(null)
  const [eventCircle, setEventCircle] = useState<CircleType>('life')
  const [eventTheme, setEventTheme] = useState('')
  const [flipped, setFlipped] = useState(false)
  const [eventsDoneInRound, setEventsDoneInRound] = useState(0)
  const [drawing, setDrawing] = useState(false)
  const [choosing, setChoosing] = useState(false)

  const loadGame = useCallback(async () => {
    const res = await gameService.getGame(gameId)
    if (res.code === 200 && res.data) {
      setGame(res.data)
    } else {
      message.error('游戏不存在')
      navigate('/home')
    }
  }, [gameId, navigate])

  useEffect(() => {
    loadGame().finally(() => setLoading(false))
  }, [loadGame])

  const eventsPerRound = game ? getEventsPerRound(game.age_round) : 2

  const handleDraw = async () => {
    if (!game) return
    setDrawing(true)
    try {
      const payload: { circle?: CircleType; theme?: string } = {}
      if (isFullyRandom(game.age_round)) {
        /* random */
      } else if (canPickCircleOnly(game.age_round)) {
        payload.circle = circle
      } else if (canPickTheme(game.age_round)) {
        payload.circle = circle
        payload.theme = theme
      }
      const res = await gameService.drawEvent(gameId, payload)
      if (res.code === 200 && res.data?.events[0]) {
        const ev = res.data.events[0]
        setEventCircle(payload.circle ?? (Math.random() > 0.5 ? 'life' : 'career'))
        setEventTheme(payload.theme ?? theme)
        setFlipped(false)
        setCurrentEvent(ev)
        // 强制重播翻牌：先展示背面，下一帧再翻转
        requestAnimationFrame(() => {
          requestAnimationFrame(() => setFlipped(true))
        })
      }
    } catch {
      message.error('抽取事件失败')
    } finally {
      setDrawing(false)
    }
  }

  const handleChoice = async (optionId: string) => {
    if (!game || !currentEvent) return
    const opt = currentEvent.options.find((o) => o.option_id === optionId)
    if (!opt) return
    setChoosing(true)
    try {
      const res = await gameService.submitChoice(gameId, {
        event_id: currentEvent.event_id,
        option_id: opt.option_id,
        circle: eventCircle,
        theme: eventTheme,
        event_title: currentEvent.title,
        event_description: currentEvent.description,
        chosen_option_text: opt.text,
        money_change: opt.money_change,
        energy_change: opt.energy_change,
        joy_change: opt.joy_change,
      })
      if (res.code !== 200 || !res.data) return

      const updated = res.data as Game
      setGame(updated)
      setCurrentEvent(null)
      setFlipped(false)
      const done = eventsDoneInRound + 1
      setEventsDoneInRound(done)

      if (done >= eventsPerRound) {
        setEventsDoneInRound(0)
        if (updated.age_round >= 8) {
          const finishRes = await gameService.finishGame(gameId)
          if ((finishRes.code === 200 || finishRes.code === 5002) && finishRes.data) {
            navigate(`/game/${gameId}/review`, { state: finishRes.data })
          }
        } else {
          const adv = await gameService.advanceRound(gameId)
          if (adv.code === 200 && adv.data) {
            setGame(adv.data)
            const advData = adv.data as Game & { round_salary_income?: number }
            const income = advData.round_salary_income ?? 0
            const status = advData.employment_status ?? 'employed'
            if (income > 0) {
              message.success(
                `进入 ${adv.data.age_range} 岁阶段，本阶段工资收入 +¥${income.toLocaleString()}`
              )
            } else if (status !== 'employed') {
              message.success(
                `进入 ${adv.data.age_range} 岁阶段（${employmentStatusLabel(status)}，本阶段无固定工资）`
              )
            } else {
              message.success(`进入 ${adv.data.age_range} 岁阶段`)
            }
          }
        }
      }
    } catch {
      message.error('提交选择失败')
    } finally {
      setChoosing(false)
    }
  }

  if (loading || !game) {
    return (
      <AppLayout>
        <div style={{ padding: 80, textAlign: 'center' }}>
          <Spin size="large" />
        </div>
      </AppLayout>
    )
  }

  const characterName = gameService.loadCharacterName(gameId)
  const themes = circle === 'life' ? LIFE_THEMES : CAREER_THEMES
  const showPicker = !currentEvent && !isFullyRandom(game.age_round)
  const showRandomDraw = !currentEvent && isFullyRandom(game.age_round)

  return (
    <AppLayout
      showStats
      stats={{
        money: game.money,
        energy: game.energy,
        joy: game.joy,
        characterName,
        ageLabel: `第 ${game.age_round} 轮 · ${game.age_range} 岁`,
      }}
    >
      <div className="game-play-page">
        <aside className="timeline">
          <h3>人生阶段</h3>
          {AGE_ROUNDS.map((r) => (
            <div
              key={r.round}
              className={`timeline-item ${r.round === game.age_round ? 'active' : ''} ${r.round < game.age_round ? 'done' : ''}`}
            >
              <span className="timeline-dot">{r.round < game.age_round ? '✓' : r.round}</span>
              <span>{r.range} 岁</span>
            </div>
          ))}
        </aside>

        <section className="event-area">
          <div className="round-label">
            本轮事件 {Math.min(eventsDoneInRound + (currentEvent ? 1 : 0), eventsPerRound)} / {eventsPerRound}
          </div>
          <div className="flip-card">
            <div className={`flip-card-inner ${flipped && currentEvent ? 'flipped' : ''}`}>
              <div className={`flip-face back ${circle}`}>
                <span className="flip-back-icon">?</span>
                {!currentEvent && (
                  <span className="flip-back-hint">
                    {isFullyRandom(game.age_round) ? '点击右侧随机抽卡' : '右侧选主题后抽卡'}
                  </span>
                )}
              </div>
              <div className={`flip-face front ${eventCircle}`}>
                {currentEvent && (
                  <>
                    <div className="event-tags">
                      <span className={`event-tag ${eventCircle}`}>
                        {eventCircle === 'life' ? '生活圈' : '事业圈'}
                      </span>
                      <span className="event-tag">{eventTheme}</span>
                    </div>
                    <h2 className="event-title">{currentEvent.title}</h2>
                    <p className="event-desc">{currentEvent.description}</p>
                    {currentEvent.options.map((opt) => (
                      <Button
                        key={opt.option_id}
                        className="option-btn"
                        loading={choosing}
                        onClick={() => handleChoice(opt.option_id)}
                      >
                        {opt.text}
                        <span className="option-hint">
                          金钱 {opt.money_change >= 0 ? '+' : ''}
                          {opt.money_change} · 精力 {opt.energy_change >= 0 ? '+' : ''}
                          {opt.energy_change} · 喜悦 {opt.joy_change >= 0 ? '+' : ''}
                          {opt.joy_change}
                        </span>
                      </Button>
                    ))}
                  </>
                )}
              </div>
            </div>
          </div>
          <p className="event-area-hint">点击卡片选项以推进沙盘推演</p>
        </section>

        <aside className="picker-panel">
          <h3>选择事件主题</h3>
          {isFullyRandom(game.age_round) ? (
            <div className="picker-hint">60 岁后：事件完全随机，无需选择圈子或主题。</div>
          ) : (
            <>
              <p className="picker-section-label">人生圈子</p>
              <div className="circle-tabs">
                <button
                  type="button"
                  className={`circle-tab ${circle === 'life' ? 'active life' : ''}`}
                  onClick={() => {
                    setCircle('life')
                    setTheme(LIFE_THEMES[0])
                  }}
                >
                  生活圈
                </button>
                <button
                  type="button"
                  className={`circle-tab ${circle === 'career' ? 'active career' : ''}`}
                  onClick={() => {
                    setCircle('career')
                    setTheme(CAREER_THEMES[0])
                  }}
                >
                  事业圈
                </button>
              </div>
              {canPickTheme(game.age_round) && (
                <div className="theme-section">
                  <p className="picker-section-label">子主题</p>
                  <div className="theme-grid">
                    {themes.map((t) => (
                      <button
                        key={t}
                        type="button"
                        className={`theme-chip ${theme === t ? 'selected' : ''}`}
                        onClick={() => setTheme(t)}
                      >
                        {t}
                      </button>
                    ))}
                  </div>
                </div>
              )}
              {canPickCircleOnly(game.age_round) && (
                <div className="picker-hint">40–60 岁：仅可选择生活或事业，子主题由系统随机。</div>
              )}
              {canPickTheme(game.age_round) && (
                <div className="picker-hint">40 岁前：可选生活/事业及任意子主题，每轮 2 个事件。</div>
              )}
            </>
          )}
          {!currentEvent && (
            <Button
              type="primary"
              className="draw-btn"
              loading={drawing}
              onClick={handleDraw}
              disabled={!showPicker && !showRandomDraw}
            >
              {showRandomDraw ? '随机抽卡' : '翻牌抽事件'}
            </Button>
          )}
        </aside>
      </div>
    </AppLayout>
  )
}
