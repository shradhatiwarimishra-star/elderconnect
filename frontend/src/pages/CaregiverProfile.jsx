import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'
import ReviewList from '../components/ReviewList'
import { StarIcon, MapPinIcon, CurrencyDollarIcon, CalendarIcon } from '@heroicons/react/24/solid'

const CaregiverProfile = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { isElder, user } = useAuth()
  const [caregiver, setCaregiver] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showBookingForm, setShowBookingForm] = useState(false)
  const [bookingData, setBookingData] = useState({
    service_type: '',
    service_date: '',
    start_time: '09:00',
    duration_hours: 4,
    service_address: '',
    city: '',
    state: '',
    zip_code: '',
    elder_notes: '',
  })

  useEffect(() => {
    fetchCaregiverDetails()
  }, [id])

  const fetchCaregiverDetails = async () => {
    try {
      const response = await api.get(`/elder/caregivers/${id}`)
      setCaregiver(response.data)
    } catch (error) {
      console.error('Failed to fetch caregiver:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleBookingSubmit = async (e) => {
    e.preventDefault()

    try {
      const response = await api.post('/bookings', {
        ...bookingData,
        caregiver_id: parseInt(id),
      })

      alert('Booking created successfully!')
      navigate(`/payment/${response.data.booking.id}`)
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to create booking')
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!caregiver) {
    return (
      <div className="card text-center py-12">
        <p className="text-gray-500">Caregiver not found</p>
      </div>
    )
  }

  const { user: caregiverUser, profile, reviews } = caregiver

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="card mb-8">
        <div className="flex flex-col md:flex-row items-start gap-6">
          {/* Profile Photo */}
          <div className="flex-shrink-0">
            {caregiverUser.profile_photo ? (
              <img
                src={caregiverUser.profile_photo}
                alt={caregiverUser.name}
                className="h-32 w-32 rounded-full object-cover"
              />
            ) : (
              <div className="h-32 w-32 rounded-full bg-primary-100 flex items-center justify-center">
                <span className="text-4xl font-bold text-primary-600">
                  {caregiverUser.name.charAt(0)}
                </span>
              </div>
            )}
          </div>

          {/* Info */}
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl font-bold text-gray-900">{caregiverUser.name}</h1>
              {profile.verified && (
                <span className="badge-success">✓ Verified</span>
              )}
            </div>

            {/* Rating */}
            <div className="flex items-center mb-4">
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <StarIcon
                    key={i}
                    className={`h-6 w-6 ${
                      i < Math.floor(profile.average_rating)
                        ? 'text-yellow-400'
                        : 'text-gray-300'
                    }`}
                  />
                ))}
              </div>
              <span className="ml-2 text-lg text-gray-600">
                {profile.average_rating.toFixed(1)} ({profile.total_bookings} bookings)
              </span>
            </div>

            {/* Details */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {profile.city && (
                <div className="flex items-center text-gray-600">
                  <MapPinIcon className="h-5 w-5 mr-2" />
                  {profile.city}, {profile.state}
                </div>
              )}
              <div className="flex items-center text-gray-600">
                <CurrencyDollarIcon className="h-5 w-5 mr-2" />
                ${profile.rate_per_hour}/hour
              </div>
              <div className="flex items-center text-gray-600">
                <CalendarIcon className="h-5 w-5 mr-2" />
                {profile.experience_years} years experience
              </div>
            </div>

            {/* Services */}
            {profile.services_offered && profile.services_offered.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {profile.services_offered.map((service, index) => (
                  <span key={index} className="badge-info">
                    {service.replace('_', ' ')}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Book Button */}
          {isElder && (
            <div>
              <button
                onClick={() => setShowBookingForm(!showBookingForm)}
                className="btn-primary whitespace-nowrap"
                disabled={user?.kyc_status !== 'verified'}
              >
                {user?.kyc_status !== 'verified' ? 'KYC Required' : 'Book Now'}
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Booking Form */}
      {showBookingForm && isElder && (
        <div className="card mb-8">
          <h2 className="text-2xl font-bold mb-6">Book This Caregiver</h2>
          <form onSubmit={handleBookingSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Service Type *
                </label>
                <select
                  className="input-field"
                  required
                  value={bookingData.service_type}
                  onChange={(e) => setBookingData({...bookingData, service_type: e.target.value})}
                >
                  <option value="">Select service</option>
                  {profile.services_offered.map((service) => (
                    <option key={service} value={service}>
                      {service.replace('_', ' ')}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Date *
                </label>
                <input
                  type="date"
                  className="input-field"
                  required
                  min={new Date().toISOString().split('T')[0]}
                  value={bookingData.service_date}
                  onChange={(e) => setBookingData({...bookingData, service_date: e.target.value})}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Start Time *
                </label>
                <input
                  type="time"
                  className="input-field"
                  required
                  value={bookingData.start_time}
                  onChange={(e) => setBookingData({...bookingData, start_time: e.target.value})}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Duration (hours) *
                </label>
                <input
                  type="number"
                  className="input-field"
                  required
                  min="1"
                  max="24"
                  value={bookingData.duration_hours}
                  onChange={(e) => setBookingData({...bookingData, duration_hours: parseFloat(e.target.value)})}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Service Address *
              </label>
              <input
                type="text"
                className="input-field"
                required
                placeholder="Enter full address"
                value={bookingData.service_address}
                onChange={(e) => setBookingData({...bookingData, service_address: e.target.value})}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  City *
                </label>
                <input
                  type="text"
                  className="input-field"
                  required
                  value={bookingData.city}
                  onChange={(e) => setBookingData({...bookingData, city: e.target.value})}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  State *
                </label>
                <input
                  type="text"
                  className="input-field"
                  required
                  value={bookingData.state}
                  onChange={(e) => setBookingData({...bookingData, state: e.target.value})}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Zip Code *
                </label>
                <input
                  type="text"
                  className="input-field"
                  required
                  value={bookingData.zip_code}
                  onChange={(e) => setBookingData({...bookingData, zip_code: e.target.value})}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Special Instructions
              </label>
              <textarea
                className="input-field"
                rows="3"
                placeholder="Any special requirements or instructions..."
                value={bookingData.elder_notes}
                onChange={(e) => setBookingData({...bookingData, elder_notes: e.target.value})}
              />
            </div>

            <div className="bg-gray-50 p-4 rounded">
              <div className="flex justify-between items-center text-lg font-semibold">
                <span>Total Cost:</span>
                <span>${(profile.rate_per_hour * bookingData.duration_hours).toFixed(2)}</span>
              </div>
            </div>

            <div className="flex gap-3">
              <button type="submit" className="btn-primary">
                Proceed to Payment
              </button>
              <button
                type="button"
                onClick={() => setShowBookingForm(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* About */}
      {profile.bio && (
        <div className="card mb-8">
          <h2 className="text-2xl font-bold mb-4">About</h2>
          <p className="text-gray-700 whitespace-pre-line">{profile.bio}</p>
        </div>
      )}

      {/* Reviews */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-6">
          Reviews ({reviews?.length || 0})
        </h2>
        <ReviewList reviews={reviews || []} />
      </div>
    </div>
  )
}

export default CaregiverProfile
