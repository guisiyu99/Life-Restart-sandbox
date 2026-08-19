export type EmploymentStatus = 'employed' | 'entrepreneur' | 'unemployed'

const NO_SALARY_THEMES = new Set(['创业'])
const EMPLOYED_THEMES = new Set(['工作'])

const ENTREPRENEUR_HINTS = ['创业', '开店', '开公司', '自立门户', '全职创业', '当老板', '自己当老板', '辞职创业']

const UNEMPLOYED_HINTS = ['辞职', '离职', '裸辞', '失业', '被裁', '裁员', '待业', '不干了', '关停', '破产', '躺平', '休息一阵']

const REEMPLOY_HINTS = [
  '入职',
  '重返职场',
  '重新工作',
  '找到新工作',
  '回去上班',
  '继续上班',
  '重返岗位',
  '接受offer',
  '接受 offer',
  '接受这份',
  '留任',
  '晋升',
  '坚守岗位',
  '认真工作',
]

function containsAny(text: string, hints: string[]): boolean {
  const lowered = text.toLowerCase()
  return hints.some((hint) => lowered.includes(hint.toLowerCase()))
}

export function resolveEmploymentStatus(
  current: EmploymentStatus,
  theme: string,
  _eventTitle: string,
  _eventDescription: string,
  chosenOption: string
): EmploymentStatus {
  if (NO_SALARY_THEMES.has(theme)) return 'entrepreneur'
  if (containsAny(chosenOption, UNEMPLOYED_HINTS)) return 'unemployed'
  if (containsAny(chosenOption, ENTREPRENEUR_HINTS)) return 'entrepreneur'
  if (containsAny(chosenOption, REEMPLOY_HINTS)) return 'employed'
  if (EMPLOYED_THEMES.has(theme)) return 'employed'
  return current
}

export function isSalaryEligible(status: EmploymentStatus): boolean {
  return status === 'employed'
}

export function employmentStatusLabel(status: EmploymentStatus): string {
  if (status === 'entrepreneur') return '创业中'
  if (status === 'unemployed') return '失业中'
  return '在职'
}
