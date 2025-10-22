import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'
import { format } from 'date-fns'
import ReviewList from '../components/ReviewList'

const BookingDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user, isElder, isCaregiver } = useAuth()
  const [booking, setBooking] = useState(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [showReviewForm, setShowReviewForm] = useState(false)
  const [reviewData, setReviewData] = useState({
    rating: 5,
    comment: '',
  })

  useEffect(() => {
    fetchBooking()
  }, [id])

  const fetchBooking = async () => {
    try {
      const response = await api.get(`/bookings/${id}`)
      setBooking(response.data.booking)
    } catch (error) {
      console.error('Failed to fetch booking:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCancelBooking = async () => {
    if (!confirm('Are you sure you want to cancel this booking?')) return

    setActionLoading(true)
    try {
      await api.post(`/bookings/${id}/cancel`, {
        reason: 'Cancelled by user'
      })
      await fetchBooking()
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to cancel booking')
    } finally {
      setActionLoading(false)
    }
  }

  const handleAcceptBooking = async () => {
    setActionLoading(true)
    try {
      await api.post(`/caregiver/bookings/${id}/accept`)
      await fetchBooking()
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to accept booking')
    } finally {
      setActionLoading(false)
    }
  }

  const handleCompleteBooking = async () => {
    setActionLoading(true)
    try {
      await api.post(`/caregiver/bookings/${id}/complete`)
      await fetchBooking()
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to complete booking')
    } finally {
      setActionLoading(false)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      confirmed: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800',
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!booking) {
    return (
      <div className="card text-center py-12">
        <p className="text-gray-500">Booking not found</p>
      </div>
    )
  }

  const canCancel = ['pending', 'confirmed'].includes(booking.status)
  const canAccept = isCaregiver && booking.status === 'pending'
  const canComplete = isCaregiver && booking.status === 'confirmed'
  const canPay = isElder && booking.status === 'pending' && booking.payment?.status === 'pending'

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <Link to="/bookings" className="text-primary-600 hover:text-primary-700 mb-4 inline-block">
          ← Back to Bookings
        </Link>
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900">Booking Details</h1>
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(booking.status)}`}>
            {booking.status}
          </span>
        </div>
      </div>

      {/* Main Info */}
      <div className="card mb-6">
        <h2 className="text-xl font-semibold mb-4">Service Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p className="text-sm text-gray-600">Service Type</p>
            <p className="font-medium capitalize">{booking.service_type.replace('_', ' ')}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Date</p>
            <p className="font-medium">{format(new Date(booking.service_date), 'PPP')}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Time</p>
            <p className="font-medium">{booking.start_time}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Duration</p>
            <p className="font-medium">{booking.duration_hours} hours</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Hourly Rate</p>
            <p className="font-medium">${booking.hourly_rate}/hour</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Total Cost</p>
            <p className="font-medium text-lg">${booking.total_cost}</p>
          </div>
        </div>

        {booking.service_address && (
          <div className="mt-4 pt-4 border-t">
            <p className="text-sm text-gray-600">Service Location</p>
            <p className="font-medium">{booking.service_address}</p>
            <p className="font-medium">{booking.city}, {booking.state} {booking.zip_code}</p>
          </div>
        )}
      </div>

      {/* Participants */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {booking.elder && (
          <div className="card">
            <h3 className="text-lg font-semibold mb-3">Elder</h3>
            <p className="font-medium">{booking.elder.name}</p>
            <p className="text-sm text-gray-600">{booking.elder.email}</p>
            <p className="text-sm text-gray-600">{booking.elder.phone}</p>
          </div>
        )}

        {booking.caregiver && (
          <div className="card">
            <h3 className="text-lg font-semibold mb-3">Caregiver</h3>
            <p className="font-medium">{booking.caregiver.name}</p>
            <p className="text-sm text-gray-600">{booking.caregiver.email}</p>
            <p className="text-sm text-gray-600">{booking.caregiver.phone}</p>
          </div>
        )}
      </div>

      {/* Notes */}
      {(booking.elder_notes || booking.caregiver_notes) && (
        <div className="card mb-6">
          <h3 className="text-lg font-semibold mb-3">Notes</h3>
          {booking.elder_notes && (
            <div className="mb-3">
              <p className="text-sm text-gray-600">Elder's Instructions:</p>
              <p className="text-gray-900">{booking.elder_notes}</p>
            </div>
          )}
          {booking.caregiver_notes && (
            <div>
              <p className="text-sm text-gray-600">Caregiver's Notes:</p>
              <p className="text-gray-900">{booking.caregiver_notes}</p>
            </div>
          )}
        </div>
      )}

      {/* Actions */}
      <div className="card mb-6">
        <h3 className="text-lg font-semibold mb-4">Actions</h3>
        <div className="flex flex-wrap gap-3">
          {canPay && (
            <Link
              to={`/payment/${booking.id}`}
              className="btn-primary"
            >
              Pay Now
            </Link>
          )}
          
          {canAccept && (
            <button
              onClick={handleAcceptBooking}
              disabled={actionLoading}
              className="btn-primary disabled:opacity-50"
            >
              Accept Booking
            </button>
          )}

          {canComplete && (
            <button
              onClick={handleCompleteBooking}
              disabled={actionLoading}
              className="btn-primary disabled:opacity-50"
            >
              Mark as Completed
            </button>
          )}

          {canCancel && (
            <button
              onClick={handleCancelBooking}
              disabled={actionLoading}
              className="btn-danger disabled:opacity-50"
            >
              Cancel Booking
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default BookingDetail
