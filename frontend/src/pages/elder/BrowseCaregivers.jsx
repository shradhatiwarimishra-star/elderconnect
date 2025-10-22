import { useState, useEffect } from 'react'
import api from '../../services/api'
import CaregiverCard from '../../components/CaregiverCard'
import { MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline'

const BrowseCaregivers = () => {
  const [caregivers, setCaregiv ers] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    service: '',
    city: '',
    min_rating: '',
    max_rate: '',
    sort: 'rating',
  })

  useEffect(() => {
    fetchCaregivers()
  }, [filters])

  const fetchCaregivers = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      Object.keys(filters).forEach(key => {
        if (filters[key]) {
          params.append(key, filters[key])
        }
      })

      const response = await api.get(`/elder/caregivers?${params}`)
      setCaregiv ers(response.data.caregivers)
    } catch (error) {
      console.error('Failed to fetch caregivers:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    setFilters({ ...filters, [key]: value })
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Find Caregivers</h1>
        <p className="mt-2 text-gray-600">Browse verified caregivers in your area</p>
      </div>

      {/* Filters */}
      <div className="card mb-8">
        <div className="flex items-center mb-4">
          <FunnelIcon className="h-5 w-5 mr-2 text-gray-600" />
          <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {/* Service Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Service Type
            </label>
            <select
              className="input-field"
              value={filters.service}
              onChange={(e) => handleFilterChange('service', e.target.value)}
            >
              <option value="">All Services</option>
              <option value="in_home_care">In-Home Care</option>
              <option value="hospital_visits">Hospital Visits</option>
              <option value="bank_visits">Bank Visits</option>
              <option value="social_outings">Social Outings</option>
              <option value="medical_assistance">Medical Assistance</option>
            </select>
          </div>

          {/* City */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              City
            </label>
            <input
              type="text"
              className="input-field"
              placeholder="Enter city"
              value={filters.city}
              onChange={(e) => handleFilterChange('city', e.target.value)}
            />
          </div>

          {/* Min Rating */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Min Rating
            </label>
            <select
              className="input-field"
              value={filters.min_rating}
              onChange={(e) => handleFilterChange('min_rating', e.target.value)}
            >
              <option value="">Any Rating</option>
              <option value="4">4+ Stars</option>
              <option value="4.5">4.5+ Stars</option>
            </select>
          </div>

          {/* Max Rate */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Max Rate ($/hr)
            </label>
            <input
              type="number"
              className="input-field"
              placeholder="Max rate"
              value={filters.max_rate}
              onChange={(e) => handleFilterChange('max_rate', e.target.value)}
            />
          </div>

          {/* Sort */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Sort By
            </label>
            <select
              className="input-field"
              value={filters.sort}
              onChange={(e) => handleFilterChange('sort', e.target.value)}
            >
              <option value="rating">Highest Rated</option>
              <option value="rate">Lowest Rate</option>
            </select>
          </div>
        </div>

        <button
          onClick={() => setFilters({
            service: '',
            city: '',
            min_rating: '',
            max_rate: '',
            sort: 'rating',
          })}
          className="mt-4 text-sm text-primary-600 hover:text-primary-700"
        >
          Clear Filters
        </button>
      </div>

      {/* Results */}
      <div>
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : caregivers.length > 0 ? (
          <>
            <p className="mb-4 text-gray-600">
              Found {caregivers.length} caregiver{caregivers.length !== 1 ? 's' : ''}
            </p>
            <div className="grid grid-cols-1 gap-6">
              {caregivers.map((caregiver) => (
                <CaregiverCard key={caregiver.user.id} caregiver={caregiver} />
              ))}
            </div>
          </>
        ) : (
          <div className="card text-center py-12">
            <MagnifyingGlassIcon className="h-12 w-12 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-500">No caregivers found matching your criteria</p>
            <p className="text-sm text-gray-400 mt-2">Try adjusting your filters</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default BrowseCaregivers
