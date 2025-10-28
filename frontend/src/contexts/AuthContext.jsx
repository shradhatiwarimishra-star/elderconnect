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
    console.log('🔄 AuthContext mounted, checking for existing session')
    // Check if user is logged in on mount
    const token = localStorage.getItem('access_token')
    console.log('🔑 Token in localStorage:', token ? 'EXISTS' : 'NONE')
    
    if (token) {
      console.log('📡 Fetching current user...')
      // TEMPORARILY DISABLED - just set loading false
      // fetchCurrentUser().catch((error) => {
      //   console.log('⚠️ Failed to fetch user, but keeping session:', error.message)
      //   setLoading(false)
      // })
      console.log('⚠️ AUTO-FETCH DISABLED FOR DEBUGGING')
      setLoading(false)
    } else {
      console.log('❌ No token, user not logged in')
      setLoading(false)
    }
  }, [])

  const fetchCurrentUser = async () => {
    try {
      console.log('📞 Calling /auth/me...')
      const response = await api.get('/auth/me')
      console.log('✅ Got user from /auth/me:', response.data.user)
      setUser(response.data.user)
      setProfile(response.data.profile)
    } catch (error) {
      console.error('❌ Failed to fetch user:', error.message)
      console.error('Status:', error.response?.status)
      // Only logout if it's an auth error (401), not network/CORS errors
      if (error.response?.status === 401) {
        console.log('🚪 Logging out due to 401')
        logout()
      } else {
        console.log('⚠️ Not logging out, just a network error')
      }
    } finally {
      console.log('✅ Setting loading = false')
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    console.log('🔐 Login attempt for:', email)
    const response = await api.post('/auth/login', { email, password })
    console.log('✅ Login response:', response.data)
    
    const { user, profile, access_token, refresh_token } = response.data
    
    console.log('💾 Saving tokens to localStorage')
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    
    console.log('👤 Setting user:', user)
    setUser(user)
    setProfile(profile)
    
    // Redirect based on role
    console.log('🚀 Redirecting to dashboard for role:', user.role)
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
