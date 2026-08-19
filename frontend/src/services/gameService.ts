import api from './api'
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
import {
  mockAdvanceRound,
  mockChoice,
  mockCreateGame,
  mockDrawEvent,
  mockFinish,
  mockGetArchive,
  mockGetArchives,
  mockGetGame,
  setCharacterName,
  getCharacterName,
} from '@/mocks/game'

const useMock = import.meta.env.VITE_USE_MOCK === 'true'

export const gameService = {
  async createGame(payload: CreateGamePayload): Promise<ApiResponse<Game>> {
    if (useMock) {
      return new Promise((resolve) => setTimeout(() => resolve(mockCreateGame(payload)), 400))
    }
    const res = await api.post<ApiResponse<Game>>('/games', payload)
    return res.data
  },

  async getGame(gameId: number): Promise<ApiResponse<Game>> {
    if (useMock) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          try {
            resolve(mockGetGame(gameId))
          } catch (e) {
            reject(e)
          }
        }, 200)
      })
    }
    const res = await api.get<ApiResponse<Game>>(`/games/${gameId}`)
    return res.data
  },

  async drawEvent(
    gameId: number,
    payload: DrawEventPayload
  ): Promise<ApiResponse<{ events: GameEvent[]; count: number }>> {
    if (useMock) {
      return new Promise((resolve) => setTimeout(() => resolve(mockDrawEvent(gameId, payload)), 600))
    }
    const res = await api.post<ApiResponse<{ events: GameEvent[]; count: number }>>(
      `/games/${gameId}/draw-event`,
      payload
    )
    return res.data
  },

  async submitChoice(gameId: number, payload: ChoicePayload): Promise<ApiResponse<Game>> {
    if (useMock) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          try {
            resolve(mockChoice(gameId, payload) as ApiResponse<Game>)
          } catch (e) {
            reject(e)
          }
        }, 300)
      })
    }
    const res = await api.post<ApiResponse<Game>>(`/games/${gameId}/choices`, payload)
    return res.data
  },

  async advanceRound(gameId: number): Promise<ApiResponse<Game>> {
    if (useMock) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          try {
            resolve(mockAdvanceRound(gameId))
          } catch (e) {
            reject(e)
          }
        }, 300)
      })
    }
    const res = await api.post<ApiResponse<Game>>(`/games/${gameId}/advance-round`)
    return res.data
  },

  async finishGame(gameId: number): Promise<ApiResponse<FinishResult>> {
    if (useMock) {
      return new Promise((resolve) => setTimeout(() => resolve(mockFinish(gameId)), 800))
    }
    const res = await api.post<ApiResponse<FinishResult>>(`/games/${gameId}/finish`)
    return res.data
  },

  async getArchives(): Promise<ApiResponse<{ items: ArchiveItem[]; total: number; page: number; page_size: number }>> {
    if (useMock) {
      return new Promise((resolve) => setTimeout(() => resolve(mockGetArchives()), 300))
    }
    const res = await api.get('/archives')
    return res.data
  },

  async getArchive(id: number): Promise<ApiResponse<FinishResult & { character_name: string }>> {
    if (useMock) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          try {
            resolve(mockGetArchive(id))
          } catch (e) {
            reject(e)
          }
        }, 300)
      })
    }
    const res = await api.get(`/archives/${id}`)
    return res.data
  },

  saveCharacterName(gameId: number, name: string) {
    localStorage.setItem(`character_name_${gameId}`, name)
    if (useMock) setCharacterName(gameId, name)
  },

  loadCharacterName(gameId: number): string {
    return localStorage.getItem(`character_name_${gameId}`) ?? getCharacterName(gameId)
  },
}
