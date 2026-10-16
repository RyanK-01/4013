import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiBell, FiCheckCircle } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import toast from 'react-hot-toast';
import { LoadingSpinner, EmptyState } from '../components/ui';

export default function Notifications() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) { navigate('/login'); return; }
    api.get('/notifications/')
      .then((res) => setNotifications(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [user]);

  const markRead = async (id) => {
    await api.put(`/notifications/${id}/read`);
    setNotifications((n) => n.map((notif) => notif.id === id ? { ...notif, is_read: true } : notif));
  };

  const markAllRead = async () => {
    await api.put('/notifications/read-all');
    setNotifications((n) => n.map((notif) => ({ ...notif, is_read: true })));
    toast.success('All marked as read');
  };

  if (loading) return <LoadingSpinner />;

  const typeColors = {
    approval: 'border-l-green-500 bg-green-50',
    rejection: 'border-l-red-500 bg-red-50',
    alert: 'border-l-yellow-500 bg-yellow-50',
    promo: 'border-l-purple-500 bg-purple-50',
    info: 'border-l-blue-500 bg-blue-50',
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold">Notifications</h1>
        {notifications.some((n) => !n.is_read) && (
          <button onClick={markAllRead} className="text-sm text-orange-500 hover:underline flex items-center gap-1">
            <FiCheckCircle /> Mark all read
          </button>
        )}
      </div>

      {notifications.length === 0 ? (
        <EmptyState icon={FiBell} title="No notifications yet" />
      ) : (
        <div className="space-y-2">
          {notifications.map((notif) => (
            <div
              key={notif.id}
              onClick={() => !notif.is_read && markRead(notif.id)}
              className={`rounded-xl p-4 border-l-4 cursor-pointer transition ${
                typeColors[notif.notification_type] || typeColors.info
              } ${notif.is_read ? 'opacity-60' : ''}`}
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-sm">{notif.title}</h3>
                  <p className="text-sm text-gray-600 mt-1">{notif.message}</p>
                </div>
                {!notif.is_read && <span className="w-2 h-2 bg-blue-500 rounded-full shrink-0 mt-1" />}
              </div>
              <p className="text-xs text-gray-400 mt-2">{new Date(notif.created_at).toLocaleString()}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
