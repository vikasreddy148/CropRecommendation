import { useEffect, useMemo, useState } from 'react'
import AuthContext from './authContext.js'
import { fetchCurrentUser, logoutSession } from '../features/auth/authApi.js'

function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  async function refreshUser() {
    try {
      const me = await fetchCurrentUser()
      setUser(me)
      return me
    } catch {
      setUser(null)
      return null
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    refreshUser()
  }, [])

  async function logout() {
    await logoutSession()
    setUser(null)
  }

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      isLoading,
      setUser,
      refreshUser,
      logout,
    }),
    [user, isLoading]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export { AuthProvider }
