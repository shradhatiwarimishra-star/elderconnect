import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import api from '../../services/api'
import BookingCard from '../../components/BookingCard'
import { 
  UserGroupIcon, 
  CalendarIcon, 
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'

const ElderDashboard = () => {
  const { user, profile } = useAuth()
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    upcoming: 0,
    completed: 0,
    total: 0,
  })

  useEffect(() => {
    fetchBookings()
  }, [])

  const fetchBookings = async () => {
    try {
      const response = await api.get('/bookings')
      const allBookings = response.data.bookings

      setBookings(allBookings.slice(0, 5)) // Recent 5 bookings

      // Calculate stats
      setStats({
        total: allBookings.length,
        upcoming: allBookings.filter(b => 
          b.status === 'confirmed' && new Date(b.service_date) >= new Date()
        ).length,
        completed: allBookings.filter(b => b.status === 'completed').length,
      })
    } catch (error) {
      console.error('Failed to fetch bookings:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Welcome back, {user?.name}!</h1>
        <p className="mt-2 text-gray-600">Manage your care services and bookings</p>
      </div>

      {/* KYC Alert */}
      {user?.kyc_status !== 'verified' && (
        <div className="mb-6 bg-yellow-50 border-l-4 border-yellow-400 p-4">
          <div className="flex">
            <ExclamationTriangleIcon className="h-6 w-6 text-yellow-400" />
            <div className="ml-3">
              <p className="text-sm text-yellow-700">
                <strong>KYC Verification Required</strong> - Please complete your KYC verification to book services.
                <Link to="/profile" className="font-medium underline ml-2">
                  Complete Now
                </Link>
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CalendarIcon className="h-12 w-12 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Upcoming Bookings</p>
              <p className="text-2xl font-bold text-gray-900">{stats.upcoming}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CheckCircleIcon className="h-12 w-12 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Completed</p>
              <p className="text-2xl font-bold text-gray-900">{stats.completed}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <UserGroupIcon className="h-12 w-12 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Bookings</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mb-8 grid grid-cols-1 md:grid-cols-2 gap-4">
        <Link to="/caregivers" className="card hover:shadow-lg transition-shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Find Caregivers</h3>
          <p className="text-gray-600 mb-4">Browse and book trusted caregivers in your area</p>
          <span className="text-primary-600 font-medium">Browse Now →</span>
        </Link>

        <Link to="/bookings" className="card hover:shadow-lg transition-shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">My Bookings</h3>
          <p className="text-gray-600 mb-4">View and manage all your bookings</p>
          <span className="text-primary-600 font-medium">View All →</span>
        </Link>
      </div>

      {/* Recent Bookings */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Recent Bookings</h2>
          {bookings.length > 0 && (
            <Link to="/bookings" className="text-primary-600 hover:text-primary-700 font-medium">
              View All
            </Link>
          )}
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : bookings.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {bookings.map((booking) => (
              <BookingCard key={booking.id} booking={booking} userRole="elder" />
            ))}
          </div>
        ) : (
          <div className="card text-center py-12">
            <p className="text-gray-500">No bookings yet. Start by finding a caregiver!</p>
            <Link to="/caregivers" className="btn-primary inline-block mt-4">
              Find Caregivers
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}

export default ElderDashboard
