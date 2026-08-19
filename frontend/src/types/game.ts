export type CircleType = 'life' | 'career'

export type EmploymentStatus = 'employed' | 'entrepreneur' | 'unemployed'

export interface Decision {
  round: number
  age_range: string
  circle: CircleType
  theme: string
  event_title: string
  event_description: string
  chosen_option: string
  money_change: number
  energy_change: number
  joy_change: number
}

export interface Game {
  id: number
  user_id: number
  status: 'in_progress' | 'completed'
  age_round: number
  age_range: string
  money: number
  energy: number
  joy: number
  employment_status: EmploymentStatus
  decisions: Decision[]
  ai_review: string | null
  created_at: string
  updated_at: string
}

export interface EventOption {
  option_id: string
  text: string
  money_change: number
  energy_change: number
  joy_change: number
}

export interface GameEvent {
  event_id: string
  title: string
  description: string
  options: EventOption[]
}

export interface CreateGamePayload {
  character_name: string
  money: number
  energy: number
  joy: number
}

export interface DrawEventPayload {
  circle?: CircleType
  theme?: string
}

export interface ChoicePayload {
  event_id: string
  option_id: string
  circle: CircleType
  theme: string
  event_title: string
  event_description: string
  chosen_option_text: string
  money_change: number
  energy_change: number
  joy_change: number
}

export interface ArchiveItem {
  id: number
  character_name?: string
  outcome_tags: string[]
  money: number
  energy: number
  joy: number
  decision_count: number
  summary: string
  created_at: string
}

export interface FinishResult {
  id: number
  outcome_tags: string[]
  money: number
  energy: number
  joy: number
  ai_review: string
  decisions: Decision[]
}

export interface ApiResponse<T> {
  code: number
  message: string
  data: T | null
}
