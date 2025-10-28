import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import api from '../../services/api'
import BookingCard from '../../components/BookingCard'
import {
  CalendarIcon,
  CheckCircleIcon,
  CurrencyDollarIcon,
  ExclamationTriangleIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

const CaregiverDashboard = () => {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState(null)
  const [bookings, setBookings] = useState([])

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [dashboardRes, bookingsRes] = await Promise.all([
        api.get('/caregiver/dashboard'),
        api.get('/caregiver/bookings?upcoming=true')
      ])

      setStats(dashboardRes.data.statistics)
      setBookings(bookingsRes.data.bookings.slice(0, 5))
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Caregiver Dashboard</h1>
        <p className="mt-2 text-gray-600">Manage your bookings and availability</p>
      </div>

      {/* KYC Alert */}
      {user?.kyc_status !== 'verified' && (
        <div className="mb-6 bg-yellow-50 border-l-4 border-yellow-400 p-4">
          <div className="flex">
            <ExclamationTriangleIcon className="h-6 w-6 text-yellow-400" />
            <div className="ml-3">
              <p className="text-sm text-yellow-700">
                <strong>KYC Verification Required</strong> - Please complete your KYC verification to receive bookings.
                <Link to="/profile" className="font-medium underline ml-2">
                  Complete Now
                </Link>
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Stats Grid */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ClockIcon className="h-12 w-12 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Upcoming</p>
                <p className="text-2xl font-bold text-gray-900">{stats.upcoming_bookings}</p>
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
                <p className="text-2xl font-bold text-gray-900">{stats.completed_bookings}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CalendarIcon className="h-12 w-12 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Bookings</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total_bookings}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CurrencyDollarIcon className="h-12 w-12 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Earnings</p>
                <p className="text-2xl font-bold text-gray-900">${stats.total_earnings}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="mb-8 grid grid-cols-1 md:grid-cols-2 gap-4">
        <Link to="/profile" className="card hover:shadow-lg transition-shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Update Profile</h3>
          <p className="text-gray-600 mb-4">Manage your services, rates, and availability</p>
          <span className="text-primary-600 font-medium">Edit Profile →</span>
        </Link>

        <Link to="/bookings" className="card hover:shadow-lg transition-shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">All Bookings</h3>
          <p className="text-gray-600 mb-4">View and manage all your bookings</p>
          <span className="text-primary-600 font-medium">View All →</span>
        </Link>
      </div>

      {/* Upcoming Bookings */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Upcoming Bookings</h2>
          {bookings.length > 0 && (
            <Link to="/bookings" className="text-primary-600 hover:text-primary-700 font-medium">
              View All
            </Link>
          )}
        </div>

        {bookings.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {bookings.map((booking) => (
              <BookingCard key={booking.id} booking={booking} userRole="caregiver" />
            ))}
          </div>
        ) : (
          <div className="card text-center py-12">
            <p className="text-gray-500">No upcoming bookings</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default CaregiverDashboard
