import type {
  ApiResponse,
  ChoicePayload,
  CreateGamePayload,
  DrawEventPayload,
  FinishResult,
  Game,
  GameEvent,
  ArchiveItem,
} from '@/types/game'
import { CAREER_THEMES, getAgeRange, getEventsPerRound, LIFE_THEMES, annualSalaryForRound, roundSalaryIncome } from '@/constants/game'
import { resolveEmploymentStatus } from '@/constants/employment'
import type { CircleType } from '@/types/game'

let nextGameId = 1
const games = new Map<number, Game>()
const characterNames = new Map<number, string>()

const MOCK_EVENTS: Record<string, GameEvent[]> = {
  友情: [
    {
      event_id: 'evt_friend_1',
      title: '老友婚礼上的抉择',
      description:
        '大学室友邀请你担任伴郎，但需要请假三天并承担往返费用。你最近项目正忙，精力也所剩不多。',
      options: [
        { option_id: 'o1', text: '答应前往，维护友情', money_change: -3000, energy_change: -2, joy_change: 3 },
        { option_id: 'o2', text: '礼金祝贺，人不到场', money_change: -500, energy_change: 0, joy_change: 1 },
        { option_id: 'o3', text: '专注工作，暂时失联', money_change: 2000, energy_change: 1, joy_change: -2 },
      ],
    },
  ],
  工作: [
    {
      event_id: 'evt_work_1',
      title: '大厂 Offer 摆在面前',
      description: '你收到一份高薪工作机会，但需要频繁加班，个人时间会被大幅压缩。',
      options: [
        { option_id: 'o1', text: '接受 Offer，先积累资本', money_change: 15000, energy_change: -3, joy_change: 1 },
        { option_id: 'o2', text: '选择平衡的小公司', money_change: 5000, energy_change: -1, joy_change: 2 },
      ],
    },
  ],
  default: [
    {
      event_id: 'evt_default_1',
      title: '人生岔路口',
      description: '一个 unexpected 的机会出现在你面前，你需要在稳定与冒险之间做出选择。',
      options: [
        { option_id: 'o1', text: '稳妥前行', money_change: 1000, energy_change: 0, joy_change: 1 },
        { option_id: 'o2', text: '冒险尝试', money_change: -2000, energy_change: -2, joy_change: 3 },
        { option_id: 'o3', text: '保持观望', money_change: 0, energy_change: 1, joy_change: 0 },
      ],
    },
  ],
}

function getGameOrThrow(id: number): Game {
  const game = games.get(id)
  if (!game) throw { response: { data: { code: 4004, message: '游戏不存在', data: null } } }
  return { ...game }
}

function saveGame(game: Game) {
  games.set(game.id, { ...game, updated_at: new Date().toISOString() })
}

export function mockCreateGame(payload: CreateGamePayload): ApiResponse<Game> {
  const id = nextGameId++
  const game: Game = {
    id,
    user_id: 1,
    status: 'in_progress',
    age_round: 1,
    age_range: getAgeRange(1),
    money: payload.money,
    energy: payload.energy,
    joy: payload.joy,
    employment_status: 'employed',
    decisions: [],
    ai_review: null,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  }
  characterNames.set(id, payload.character_name)
  saveGame(game)
  return { code: 200, message: 'success', data: game }
}

export function mockGetGame(id: number): ApiResponse<Game> {
  return { code: 200, message: 'success', data: getGameOrThrow(id) }
}

function pickRandomTheme(circle?: CircleType): string {
  if (circle === 'career') {
    return CAREER_THEMES[Math.floor(Math.random() * CAREER_THEMES.length)]
  }
  if (circle === 'life') {
    return LIFE_THEMES[Math.floor(Math.random() * LIFE_THEMES.length)]
  }
  const all = [...LIFE_THEMES, ...CAREER_THEMES]
  return all[Math.floor(Math.random() * all.length)]
}

export function mockDrawEvent(id: number, payload: DrawEventPayload): ApiResponse<{ events: GameEvent[]; count: number }> {
  const game = getGameOrThrow(id)
  const theme = payload.theme ?? pickRandomTheme(payload.circle)
  const pool = MOCK_EVENTS[theme] ?? MOCK_EVENTS.default
  const event = pool[0]
  const count = getEventsPerRound(game.age_round)
  return { code: 200, message: 'success', data: { events: [event], count } }
}

export function mockChoice(id: number, payload: ChoicePayload): ApiResponse<Game & { last_decision: Game['decisions'][0] }> {
  const game = getGameOrThrow(id)
  const decision = {
    round: game.age_round,
    age_range: game.age_range,
    circle: payload.circle,
    theme: payload.theme,
    event_title: payload.event_title,
    event_description: payload.event_description,
    chosen_option: payload.chosen_option_text,
    money_change: payload.money_change,
    energy_change: payload.energy_change,
    joy_change: payload.joy_change,
  }
  game.money += payload.money_change
  game.energy = Math.max(0, game.energy + payload.energy_change)
  game.joy = Math.max(0, game.joy + payload.joy_change)
  game.employment_status = resolveEmploymentStatus(
    game.employment_status,
    payload.theme,
    payload.event_title,
    payload.event_description,
    payload.chosen_option_text
  )
  game.decisions = [...game.decisions, decision]
  saveGame(game)
  return {
    code: 200,
    message: 'success',
    data: { ...game, last_decision: decision },
  }
}

export function mockAdvanceRound(id: number): ApiResponse<Game & { round_salary_income: number; annual_salary: number }> {
  const game = getGameOrThrow(id)
  if (game.age_round >= 8) {
    throw { response: { data: { code: 4005, message: '已是最后一轮', data: null } } }
  }
  const income = roundSalaryIncome(game.age_round, game.employment_status)
  game.money += income
  game.age_round += 1
  game.age_range = getAgeRange(game.age_round)
  saveGame(game)
  return {
    code: 200,
    message: 'success',
    data: {
      ...game,
      round_salary_income: income,
      annual_salary: annualSalaryForRound(game.age_round),
    },
  }
}

export function mockFinish(id: number): ApiResponse<FinishResult> {
  const game = getGameOrThrow(id)
  const name = characterNames.get(id) ?? '玩家'
  if (game.age_round === 8) {
    game.money += roundSalaryIncome(8, game.employment_status)
  }
  game.status = 'completed'
  const aiReview = `${name} 的一生在选择与随机之间展开。从 22 岁到 70 岁，你经历了 ${game.decisions.length} 次关键抉择，最终积累了 ${game.money.toLocaleString()} 元财富，精力 ${game.energy}，喜悦 ${game.joy}。每一次选择都塑造了独特的人生轨迹。`
  game.ai_review = aiReview
  saveGame(game)
  return {
    code: 200,
    message: 'success',
    data: {
      id: game.id,
      outcome_tags: game.joy >= 8 ? ['平衡人生', '温暖关系'] : game.money >= 200000 ? ['事业达人'] : ['平凡之路'],
      money: game.money,
      energy: game.energy,
      joy: game.joy,
      ai_review: aiReview,
      decisions: game.decisions,
    },
  }
}

export function mockGetArchives(): ApiResponse<{ items: ArchiveItem[]; total: number; page: number; page_size: number }> {
  const items: ArchiveItem[] = []
  games.forEach((game, id) => {
    if (game.status !== 'completed') return
    items.push({
      id,
      character_name: characterNames.get(id) ?? '玩家',
      outcome_tags: game.joy >= 8 ? ['平衡人生'] : ['事业达人'],
      money: game.money,
      energy: game.energy,
      joy: game.joy,
      decision_count: game.decisions.length,
      summary: game.ai_review?.slice(0, 40) ?? '',
      created_at: game.created_at,
    })
  })
  return { code: 200, message: 'success', data: { items, total: items.length, page: 1, page_size: 20 } }
}

export function mockGetArchive(id: number): ApiResponse<FinishResult & { character_name: string }> {
  const game = getGameOrThrow(id)
  if (game.status !== 'completed' || !game.ai_review) {
    throw { response: { data: { code: 4004, message: '档案不存在', data: null } } }
  }
  return {
    code: 200,
    message: 'success',
    data: {
      id: game.id,
      character_name: characterNames.get(id) ?? '玩家',
      outcome_tags: game.joy >= 8 ? ['平衡人生', '温暖关系'] : ['事业达人'],
      money: game.money,
      energy: game.energy,
      joy: game.joy,
      ai_review: game.ai_review,
      decisions: game.decisions,
    },
  }
}

export function setCharacterName(gameId: number, name: string) {
  characterNames.set(gameId, name)
}

export function getCharacterName(gameId: number): string {
  return characterNames.get(gameId) ?? '玩家'
}
