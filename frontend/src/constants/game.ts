import type { EmploymentStatus } from '@/constants/employment'
import { isSalaryEligible } from '@/constants/employment'

export const AGE_ROUNDS = [
  { round: 1, range: '22-25', eventsPerRound: 2 },
  { round: 2, range: '25-30', eventsPerRound: 2 },
  { round: 3, range: '30-35', eventsPerRound: 2 },
  { round: 4, range: '35-40', eventsPerRound: 2 },
  { round: 5, range: '40-45', eventsPerRound: 2 },
  { round: 6, range: '45-50', eventsPerRound: 2 },
  { round: 7, range: '50-60', eventsPerRound: 2 },
  { round: 8, range: '60-70', eventsPerRound: 1 },
] as const

export const LIFE_THEMES = [
  '父母',
  '子女',
  '对象',
  '身体健康',
  '消费娱乐',
  '自我觉察',
  '亲情爱情',
  '友情',
] as const

export const CAREER_THEMES = [
  '工作',
  '创业',
  '副业',
  '感性',
  '地产',
  '理性',
  '公益',
  '保险信托',
] as const

export const DEFAULT_STATS = {
  money: 50000,
  energy: 10,
  joy: 0,
} as const

export const DEFAULT_ANNUAL_SALARY = 100_000
export const SALARY_GROWTH_PER_ROUND = 0.12

const YEARS_PER_ROUND: Record<number, number> = {
  1: 3,
  2: 5,
  3: 5,
  4: 5,
  5: 5,
  6: 5,
  7: 10,
  8: 10,
}

export function annualSalaryForRound(round: number): number {
  return Math.floor(DEFAULT_ANNUAL_SALARY * (1 + SALARY_GROWTH_PER_ROUND) ** Math.max(round - 1, 0))
}

export function roundSalaryIncome(round: number, employmentStatus: EmploymentStatus = 'employed'): number {
  if (!isSalaryEligible(employmentStatus)) return 0
  const years = YEARS_PER_ROUND[round] ?? 5
  return annualSalaryForRound(round) * years
}

export function getAgeRange(round: number): string {
  return AGE_ROUNDS.find((r) => r.round === round)?.range ?? '22-25'
}

export function getEventsPerRound(round: number): number {
  return AGE_ROUNDS.find((r) => r.round === round)?.eventsPerRound ?? 2
}

export function canPickTheme(round: number): boolean {
  return round <= 4
}

export function canPickCircleOnly(round: number): boolean {
  return round >= 5 && round <= 7
}

export function isFullyRandom(round: number): boolean {
  return round >= 8
}
