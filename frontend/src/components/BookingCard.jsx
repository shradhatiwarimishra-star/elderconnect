import { Link } from 'react-router-dom'
import { format } from 'date-fns'
import { CalendarIcon, ClockIcon, CurrencyDollarIcon } from '@heroicons/react/24/outline'

const BookingCard = ({ booking, userRole }) => {
  const getStatusBadge = (status) => {
    const badges = {
      pending: 'badge-warning',
      confirmed: 'badge-info',
      completed: 'badge-success',
      cancelled: 'badge-danger',
    }
    return badges[status] || 'badge'
  }

  const otherUser = userRole === 'elder' ? booking.caregiver : booking.elder

  return (
    <div className="card hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">
            {userRole === 'elder' ? 'Caregiver' : 'Elder'}: {otherUser?.name}
          </h3>
          <p className="text-sm text-gray-600">{booking.service_type.replace('_', ' ')}</p>
        </div>
        <span className={getStatusBadge(booking.status)}>
          {booking.status}
        </span>
      </div>

      <div className="space-y-2">
        <div className="flex items-center text-sm text-gray-600">
          <CalendarIcon className="h-5 w-5 mr-2" />
          {format(new Date(booking.service_date), 'PPP')}
        </div>
        
        <div className="flex items-center text-sm text-gray-600">
          <ClockIcon className="h-5 w-5 mr-2" />
          {booking.start_time} ({booking.duration_hours} hours)
        </div>
        
        <div className="flex items-center text-sm text-gray-600">
          <CurrencyDollarIcon className="h-5 w-5 mr-2" />
          ${booking.total_cost}
        </div>
      </div>

      {booking.service_address && (
        <div className="mt-3 text-sm text-gray-600">
          <p className="font-medium">Location:</p>
          <p>{booking.service_address}</p>
          <p>{booking.city}, {booking.state} {booking.zip_code}</p>
        </div>
      )}

      <div className="mt-4 pt-4 border-t border-gray-200">
        <Link
          to={`/bookings/${booking.id}`}
          className="text-primary-600 hover:text-primary-700 font-medium text-sm"
        >
          View Details →
        </Link>
      </div>
    </div>
  )
}

export default BookingCard
