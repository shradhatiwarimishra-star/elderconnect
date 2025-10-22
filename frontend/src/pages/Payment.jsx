import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../services/api'
import { format } from 'date-fns'
import { CreditCardIcon, CheckCircleIcon } from '@heroicons/react/24/outline'

const Payment = () => {
  const { bookingId } = useParams()
  const navigate = useNavigate()
  const [booking, setBooking] = useState(null)
  const [payment, setPayment] = useState(null)
  const [loading, setLoading] = useState(true)
  const [processing, setProcessing] = useState(false)
  const [success, setSuccess] = useState(false)
  const [paymentMethod, setPaymentMethod] = useState('card')

  useEffect(() => {
    fetchBookingDetails()
  }, [bookingId])

  const fetchBookingDetails = async () => {
    try {
      const response = await api.get(`/bookings/${bookingId}`)
      setBooking(response.data.booking)
      setPayment(response.data.booking.payment)
    } catch (error) {
      console.error('Failed to fetch booking:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePayment = async (e) => {
    e.preventDefault()
    setProcessing(true)

    try {
      // Mock payment processing
      // In production, you would integrate with Stripe here
      const response = await api.post('/payments/process', {
        booking_id: bookingId,
        payment_method: paymentMethod,
      })

      setSuccess(true)
      
      // Redirect to booking detail after 2 seconds
      setTimeout(() => {
        navigate(`/bookings/${bookingId}`)
      }, 2000)
    } catch (error) {
      alert(error.response?.data?.error || 'Payment failed')
      setProcessing(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!booking || !payment) {
    return (
      <div className="card text-center py-12">
        <p className="text-gray-500">Booking not found</p>
      </div>
    )
  }

  if (payment.status === 'completed') {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="card text-center py-12">
          <CheckCircleIcon className="h-16 w-16 text-green-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Payment Completed</h2>
          <p className="text-gray-600 mb-6">This booking has already been paid for.</p>
          <button
            onClick={() => navigate(`/bookings/${bookingId}`)}
            className="btn-primary"
          >
            View Booking Details
          </button>
        </div>
      </div>
    )
  }

  if (success) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="card text-center py-12">
          <CheckCircleIcon className="h-16 w-16 text-green-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Payment Successful!</h2>
          <p className="text-gray-600 mb-6">Your booking has been confirmed.</p>
          <p className="text-sm text-gray-500">Redirecting to booking details...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Complete Payment</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Booking Summary */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Booking Summary</h2>
          
          <div className="space-y-3">
            <div>
              <p className="text-sm text-gray-600">Service</p>
              <p className="font-medium capitalize">{booking.service_type.replace('_', ' ')}</p>
            </div>
            
            <div>
              <p className="text-sm text-gray-600">Date & Time</p>
              <p className="font-medium">
                {format(new Date(booking.service_date), 'PPP')} at {booking.start_time}
              </p>
            </div>
            
            <div>
              <p className="text-sm text-gray-600">Duration</p>
              <p className="font-medium">{booking.duration_hours} hours</p>
            </div>
            
            <div>
              <p className="text-sm text-gray-600">Caregiver</p>
              <p className="font-medium">{booking.caregiver?.name}</p>
            </div>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-200">
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-600">Rate per hour</span>
              <span className="font-medium">${booking.hourly_rate}</span>
            </div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-600">Duration</span>
              <span className="font-medium">{booking.duration_hours} hours</span>
            </div>
            <div className="flex justify-between items-center text-lg font-bold pt-2 border-t">
              <span>Total</span>
              <span>${booking.total_cost}</span>
            </div>
          </div>
        </div>

        {/* Payment Form */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Payment Details</h2>

          <form onSubmit={handlePayment}>
            {/* Payment Method Selection */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Payment Method
              </label>
              <div className="space-y-3">
                <label className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition ${
                  paymentMethod === 'card' ? 'border-primary-600 bg-primary-50' : 'border-gray-300'
                }`}>
                  <input
                    type="radio"
                    name="payment_method"
                    value="card"
                    checked={paymentMethod === 'card'}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                    className="mr-3"
                  />
                  <CreditCardIcon className="h-6 w-6 mr-2" />
                  <span className="font-medium">Credit/Debit Card</span>
                </label>
                
                <label className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition ${
                  paymentMethod === 'bank_transfer' ? 'border-primary-600 bg-primary-50' : 'border-gray-300'
                }`}>
                  <input
                    type="radio"
                    name="payment_method"
                    value="bank_transfer"
                    checked={paymentMethod === 'bank_transfer'}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                    className="mr-3"
                  />
                  <span className="font-medium">Bank Transfer</span>
                </label>
              </div>
            </div>

            {/* Mock Card Details (for demo purposes) */}
            {paymentMethod === 'card' && (
              <div className="space-y-4 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Card Number
                  </label>
                  <input
                    type="text"
                    className="input-field"
                    placeholder="1234 5678 9012 3456"
                    required
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Expiry Date
                    </label>
                    <input
                      type="text"
                      className="input-field"
                      placeholder="MM/YY"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      CVV
                    </label>
                    <input
                      type="text"
                      className="input-field"
                      placeholder="123"
                      required
                    />
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Cardholder Name
                  </label>
                  <input
                    type="text"
                    className="input-field"
                    placeholder="John Doe"
                    required
                  />
                </div>
              </div>
            )}

            {/* Demo Notice */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <p className="text-sm text-blue-800">
                <strong>Demo Mode:</strong> This is a mock payment system. No actual charges will be made.
                In production, this would integrate with Stripe or another payment gateway.
              </p>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={processing}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {processing ? 'Processing...' : `Pay $${booking.total_cost}`}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Payment
