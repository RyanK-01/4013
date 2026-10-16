/**
 * Application root – configures client-side routing, auth context, and toast notifications.
 * All routes are nested inside a shared Layout shell with top and bottom navigation bars.
 */
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';
import Layout from './components/Layout';

// User pages
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Search from './pages/Search';
import Nearby from './pages/Nearby';
import BrowseCategory from './pages/BrowseCategory';
import StallDetail from './pages/StallDetail';
import Recommendations from './pages/Recommendations';
import RecommendationFlow from './pages/RecommendationFlow';
import ViewLater from './pages/ViewLater';
import Favourites from './pages/Favourites';
import SubmitStall from './pages/SubmitStall';
import WriteReview from './pages/WriteReview';
import ReportBug from './pages/ReportBug';
import SuggestFeature from './pages/SuggestFeature';
import SubmitCrowdReport from './pages/SubmitCrowdReport';
import Notifications from './pages/Notifications';
import Profile from './pages/Profile';

// Admin pages
import AdminDashboard from './pages/admin/Dashboard';
import AdminStalls from './pages/admin/ManageStalls';
import AdminPendingStalls from './pages/admin/PendingStalls';
import AdminPendingReviews from './pages/admin/PendingReviews';
import AdminPendingCrowd from './pages/admin/PendingCrowd';
import AdminReports from './pages/admin/Reports';
import AdminNotifications from './pages/admin/PushNotifications';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Toaster position="top-center" toastOptions={{ duration: 3000 }} />
        <Routes>
          <Route element={<Layout />}>
            {/* Public */}
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/search" element={<Search />} />
            <Route path="/nearby" element={<Nearby />} />
            <Route path="/browse/:category" element={<BrowseCategory />} />
            <Route path="/stall/:id" element={<StallDetail />} />

            {/* Recommendations */}
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/recommendation-flow" element={<RecommendationFlow />} />
            <Route path="/view-later" element={<ViewLater />} />

            {/* Authenticated */}
            <Route path="/favourites" element={<Favourites />} />
            <Route path="/submit-stall" element={<SubmitStall />} />
            <Route path="/write-review/:stallId" element={<WriteReview />} />
            <Route path="/report-bug" element={<ReportBug />} />
            <Route path="/suggest-feature" element={<SuggestFeature />} />
            <Route path="/submit-crowd/:stallId" element={<SubmitCrowdReport />} />
            <Route path="/notifications" element={<Notifications />} />
            <Route path="/profile" element={<Profile />} />

            {/* Admin */}
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/admin/stalls" element={<AdminStalls />} />
            <Route path="/admin/pending-stalls" element={<AdminPendingStalls />} />
            <Route path="/admin/pending-reviews" element={<AdminPendingReviews />} />
            <Route path="/admin/pending-crowd" element={<AdminPendingCrowd />} />
            <Route path="/admin/reports" element={<AdminReports />} />
            <Route path="/admin/notifications" element={<AdminNotifications />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
