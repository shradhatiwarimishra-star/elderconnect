import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const PrivateRoute = ({ children, role }) => {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  // If a specific role is required, check it
  if (role && user.role !== role) {
    // Redirect to appropriate dashboard
    if (user.role === 'elder') {
      return <Navigate to="/elder/dashboard" replace />
    } else if (user.role === 'caregiver') {
      return <Navigate to="/caregiver/dashboard" replace />
    }
  }

  return children
}

export default PrivateRoute
