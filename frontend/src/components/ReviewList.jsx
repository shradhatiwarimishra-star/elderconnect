import { format } from 'date-fns'
import { StarIcon } from '@heroicons/react/24/solid'

const ReviewList = ({ reviews }) => {
  if (!reviews || reviews.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No reviews yet
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {reviews.map((review) => (
        <div key={review.id} className="card">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              {/* Rating */}
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <StarIcon
                    key={i}
                    className={`h-5 w-5 ${
                      i < review.rating ? 'text-yellow-400' : 'text-gray-300'
                    }`}
                  />
                ))}
                <span className="ml-2 text-sm text-gray-600">
                  {review.rating} out of 5
                </span>
              </div>

              {/* Reviewer */}
              {review.reviewer && (
                <p className="mt-2 text-sm font-medium text-gray-900">
                  {review.reviewer.name}
                </p>
              )}

              {/* Comment */}
              {review.comment && (
                <p className="mt-2 text-gray-700">{review.comment}</p>
              )}

              {/* Detailed Ratings */}
              {(review.professionalism_rating || review.punctuality_rating || review.quality_rating) && (
                <div className="mt-3 flex gap-4 text-sm text-gray-600">
                  {review.professionalism_rating && (
                    <span>Professionalism: {review.professionalism_rating}/5</span>
                  )}
                  {review.punctuality_rating && (
                    <span>Punctuality: {review.punctuality_rating}/5</span>
                  )}
                  {review.quality_rating && (
                    <span>Quality: {review.quality_rating}/5</span>
                  )}
                </div>
              )}

              {/* Date */}
              <p className="mt-2 text-xs text-gray-500">
                {format(new Date(review.created_at), 'PPP')}
              </p>

              {/* Verified Badge */}
              {review.is_verified && (
                <span className="inline-block mt-2 badge-success">
                  ✓ Verified Booking
                </span>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default ReviewList
