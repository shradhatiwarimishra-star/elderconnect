import { createContext, useContext, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

const AuthContext = createContext({})

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    // Check if user is logged in on mount
    const token = localStorage.getItem('access_token')
    if (token) {
      // Try to fetch user, but don't block if it fails
      fetchCurrentUser().catch(() => {
        // If fetch fails, just set loading to false
        // User might still be valid, tokens are in localStorage
        setLoading(false)
      })
    } else {
      setLoading(false)
    }
  }, [])

  const fetchCurrentUser = async () => {
    try {
      const response = await api.get('/auth/me')
      setUser(response.data.user)
      setProfile(response.data.profile)
    } catch (error) {
      console.error('Failed to fetch user:', error)
      // Only logout if it's an auth error (401), not network/CORS errors
      if (error.response?.status === 401) {
        logout()
      }
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    const response = await api.post('/auth/login', { email, password })
    const { user, profile, access_token, refresh_token } = response.data
    
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    
    setUser(user)
    setProfile(profile)
    
    // Redirect based on role
    if (user.role === 'elder') {
      navigate('/elder/dashboard')
    } else if (user.role === 'caregiver') {
      navigate('/caregiver/dashboard')
    }
    
    return response.data
  }

  const register = async (userData) => {
    const response = await api.post('/auth/register', userData)
    const { user, profile, access_token, refresh_token } = response.data
    
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    
    setUser(user)
    setProfile(profile)
    
    // Redirect based on role
    if (user.role === 'elder') {
      navigate('/elder/dashboard')
    } else if (user.role === 'caregiver') {
      navigate('/caregiver/dashboard')
    }
    
    return response.data
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
    setProfile(null)
    navigate('/login')
  }

  const updateProfile = (updatedProfile) => {
    setProfile(updatedProfile)
  }

  const value = {
    user,
    profile,
    loading,
    login,
    register,
    logout,
    updateProfile,
    isAuthenticated: !!user,
    isElder: user?.role === 'elder',
    isCaregiver: user?.role === 'caregiver',
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
