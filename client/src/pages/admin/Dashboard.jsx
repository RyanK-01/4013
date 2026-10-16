import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import toast from 'react-hot-toast';
import { MdRestaurant, MdRateReview, MdPeople, MdBugReport, MdNotifications, MdPending, MdSync } from 'react-icons/md';

export default function AdminDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [syncing, setSyncing] = useState(false);

  useEffect(() => {
    if (!user || user.role !== 'admin') { navigate('/'); return; }
    api.get('/admin/stats').then((res) => setStats(res.data)).catch(() => {});
  }, [user]);

  const syncGovData = async () => {
    setSyncing(true);
    try {
      const res = await api.post('/admin/sync-gov-data');
      toast.success(`Sync complete! ${res.data.new_centres_added} new centres added (${res.data.already_existed} already existed)`);
      // Refresh stats
      api.get('/admin/stats').then((res) => setStats(res.data));
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Sync failed');
    } finally {
      setSyncing(false);
    }
  };

  if (!stats) return <div className="text-center py-12 text-gray-500">Loading...</div>;

  const cards = [
    { label: 'Total Stalls', value: stats.total_stalls, icon: MdRestaurant, color: 'bg-orange-500', link: '/admin/stalls' },
    { label: 'Pending Stalls', value: stats.pending_stalls, icon: MdPending, color: 'bg-yellow-500', link: '/admin/pending-stalls' },
    { label: 'Pending Reviews', value: stats.pending_reviews, icon: MdRateReview, color: 'bg-blue-500', link: '/admin/pending-reviews' },
    { label: 'Pending Crowd Reports', value: stats.pending_crowd_reports, icon: MdPeople, color: 'bg-purple-500', link: '/admin/pending-crowd' },
    { label: 'Bug Reports', value: stats.bug_reports_pending, icon: MdBugReport, color: 'bg-red-500', link: '/admin/reports' },
    { label: 'Total Users', value: stats.total_users, icon: MdPeople, color: 'bg-green-500', link: null },
  ];

  return (
    <div className="space-y-6 pb-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Admin Dashboard</h1>
        <Link to="/admin/notifications" className="bg-orange-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-orange-600 transition flex items-center gap-1">
          <MdNotifications /> Push Notification
        </Link>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
        {cards.map((card) => {
          const Icon = card.icon;
          const Wrapper = card.link ? Link : 'div';
          return (
            <Wrapper
              key={card.label}
              to={card.link || '#'}
              className="bg-white rounded-xl p-4 shadow-sm border hover:shadow-md transition"
            >
              <div className={`${card.color} w-10 h-10 rounded-lg flex items-center justify-center mb-3`}>
                <Icon className="text-white text-xl" />
              </div>
              <p className="text-2xl font-bold">{card.value}</p>
              <p className="text-sm text-gray-500">{card.label}</p>
            </Wrapper>
          );
        })}
      </div>

      {/* Government Data Sync */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-4 shadow-sm border border-blue-200">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-semibold text-blue-900">Government Data (data.gov.sg)</h2>
            <p className="text-sm text-blue-600 mt-0.5">NEA Hawker Centre data – 107 centres with coordinates</p>
          </div>
          <button
            onClick={syncGovData}
            disabled={syncing}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition disabled:opacity-50 flex items-center gap-1"
          >
            <MdSync className={syncing ? 'animate-spin' : ''} />
            {syncing ? 'Syncing...' : 'Sync Now'}
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h2 className="font-semibold mb-3">Quick Links</h2>
        <div className="grid grid-cols-2 gap-2">
          <Link to="/admin/stalls" className="text-sm text-orange-600 hover:underline">Manage Stalls</Link>
          <Link to="/admin/pending-stalls" className="text-sm text-orange-600 hover:underline">Pending Stalls ({stats.pending_stalls})</Link>
          <Link to="/admin/pending-reviews" className="text-sm text-orange-600 hover:underline">Pending Reviews ({stats.pending_reviews})</Link>
          <Link to="/admin/pending-crowd" className="text-sm text-orange-600 hover:underline">Pending Crowd ({stats.pending_crowd_reports})</Link>
          <Link to="/admin/reports" className="text-sm text-orange-600 hover:underline">User Reports</Link>
          <Link to="/admin/notifications" className="text-sm text-orange-600 hover:underline">Send Notifications</Link>
        </div>
      </div>
    </div>
  );
}
