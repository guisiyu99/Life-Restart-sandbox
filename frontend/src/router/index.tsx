import { createBrowserRouter, Navigate } from 'react-router-dom'
import LoginPage from '../pages/LoginPage'
import RegisterPage from '../pages/RegisterPage'
import HomePage from '../pages/HomePage'
import GameNewPage from '../pages/GameNewPage'
import GamePlayPage from '../pages/GamePlayPage'
import ReviewPage from '../pages/ReviewPage'
import ArchivesPage from '../pages/ArchivesPage'
import ArchiveDetailPage from '../pages/ArchiveDetailPage'
import ProtectedRoute from '../components/ProtectedRoute'

export const router = createBrowserRouter(
  [
  {
    path: '/',
    element: <Navigate to="/login" replace />,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/register',
    element: <RegisterPage />,
  },
  {
    path: '/home',
    element: (
      <ProtectedRoute>
        <HomePage />
      </ProtectedRoute>
    ),
  },
  {
    path: '/game/new',
    element: (
      <ProtectedRoute>
        <GameNewPage />
      </ProtectedRoute>
    ),
  },
  {
    path: '/game/:id',
    element: (
      <ProtectedRoute>
        <GamePlayPage />
      </ProtectedRoute>
    ),
  },
  {
    path: '/game/:id/review',
    element: (
      <ProtectedRoute>
        <ReviewPage />
      </ProtectedRoute>
    ),
  },
  {
    path: '/archives',
    element: (
      <ProtectedRoute>
        <ArchivesPage />
      </ProtectedRoute>
    ),
  },
  {
    path: '/archives/:id',
    element: (
      <ProtectedRoute>
        <ArchiveDetailPage />
      </ProtectedRoute>
    ),
  },
  ],
  { basename: import.meta.env.BASE_URL },
)
