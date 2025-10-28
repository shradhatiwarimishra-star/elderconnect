import { Link } from 'react-router-dom'
import { StarIcon, MapPinIcon, CurrencyDollarIcon } from '@heroicons/react/24/solid'

const CaregiverCard = ({ caregiver }) => {
  // Handle different API response structures
  const user = caregiver.user || {}
  const profile = caregiver.profile || caregiver || {}

  return (
    <div className="card hover:shadow-xl transition-shadow duration-200">
      <div className="flex items-start space-x-4">
        {/* Profile Photo */}
        <div className="flex-shrink-0">
          {user.profile_photo ? (
            <img
              src={user.profile_photo}
              alt={user.name}
              className="h-20 w-20 rounded-full object-cover"
            />
          ) : (
            <div className="h-20 w-20 rounded-full bg-primary-100 flex items-center justify-center">
              <span className="text-2xl font-bold text-primary-600">
                {user.name.charAt(0)}
              </span>
            </div>
          )}
        </div>

        {/* Caregiver Info */}
        <div className="flex-1">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-semibold text-gray-900">{user.name}</h3>
            {profile?.verified && (
              <span className="badge-success">✓ Verified</span>
            )}
          </div>

          {/* Rating */}
          <div className="flex items-center mt-2">
            <div className="flex items-center">
              {[...Array(5)].map((_, i) => (
                <StarIcon
                  key={i}
                  className={`h-5 w-5 ${
                    i < Math.floor(profile.average_rating)
                      ? 'text-yellow-400'
                      : 'text-gray-300'
                  }`}
                />
              ))}
            </div>
            <span className="ml-2 text-sm text-gray-600">
              {profile.average_rating.toFixed(1)} ({profile.total_bookings} bookings)
            </span>
          </div>

          {/* Bio */}
          {profile.bio && (
            <p className="mt-2 text-sm text-gray-600 line-clamp-2">{profile.bio}</p>
          )}

          {/* Details */}
          <div className="mt-3 flex flex-wrap gap-4">
            {profile?.city && (
              <div className="flex items-center text-sm text-gray-600">
                <MapPinIcon className="h-4 w-4 mr-1" />
                {profile.city}, {profile.state}
              </div>
            )}
            {profile?.rate_per_hour && (
              <div className="flex items-center text-sm text-gray-600">
                <CurrencyDollarIcon className="h-4 w-4 mr-1" />
                ${profile.rate_per_hour}/hour
              </div>
            )}
          </div>

          {/* Services */}
          {profile?.services_offered && (
            <div className="mt-3 flex flex-wrap gap-2">
              {(typeof profile.services_offered === 'string' 
                ? profile.services_offered.split(',') 
                : profile.services_offered
              ).map((service, index) => (
                <span key={index} className="badge-info">
                  {service.replace(/_/g, ' ').trim()}
                </span>
              ))}
            </div>
          )}

          {/* Action Button */}
          <div className="mt-4">
            <Link
              to={`/caregivers/${user.id}`}
              className="btn-primary inline-block"
            >
              View Profile
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CaregiverCard
