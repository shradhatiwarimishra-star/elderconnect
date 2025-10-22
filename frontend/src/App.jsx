import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import PrivateRoute from './components/PrivateRoute'
import Layout from './components/Layout'

// Pages
import Login from './pages/Login'
import Register from './pages/Register'
import ElderDashboard from './pages/elder/Dashboard'
import CaregiverDashboard from './pages/caregiver/Dashboard'
import BrowseCaregivers from './pages/elder/BrowseCaregivers'
import CaregiverProfile from './pages/CaregiverProfile'
import Profile from './pages/Profile'
import Bookings from './pages/Bookings'
import BookingDetail from './pages/BookingDetail'
import Payment from './pages/Payment'

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Protected Routes */}
          <Route element={<PrivateRoute><Layout /></PrivateRoute>}>
            {/* Elder Routes */}
            <Route path="/elder/dashboard" element={<PrivateRoute role="elder"><ElderDashboard /></PrivateRoute>} />
            <Route path="/caregivers" element={<PrivateRoute role="elder"><BrowseCaregivers /></PrivateRoute>} />
            
            {/* Caregiver Routes */}
            <Route path="/caregiver/dashboard" element={<PrivateRoute role="caregiver"><CaregiverDashboard /></PrivateRoute>} />
            
            {/* Common Routes */}
            <Route path="/caregivers/:id" element={<CaregiverProfile />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/bookings" element={<Bookings />} />
            <Route path="/bookings/:id" element={<BookingDetail />} />
            <Route path="/payment/:bookingId" element={<Payment />} />
          </Route>
          
          {/* Default redirect */}
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </AuthProvider>
    </Router>
  )
}

export default App
