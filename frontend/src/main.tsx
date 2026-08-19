import { StrictMode, useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'
import { router } from './router'
import { useAuthStore } from './stores/authStore'
import './styles/theme.css'
import './index.css'

function AppBootstrap() {
  const loadAuth = useAuthStore((s) => s.loadAuth)
  useEffect(() => {
    loadAuth()
  }, [loadAuth])
  return <RouterProvider router={router} />
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AppBootstrap />
  </StrictMode>,
)
