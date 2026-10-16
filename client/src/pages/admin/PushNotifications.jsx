import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import toast from 'react-hot-toast';
import { PageHeader, Card, FormInput, FormTextarea, Button, ToggleGroup } from '../../components/ui';

const NOTIFICATION_TYPES = [
  { value: 'alert', label: 'Weather Alert' },
  { value: 'promo', label: 'Stall Promotion' },
  { value: 'maintenance', label: 'Maintenance' },
  { value: 'update', label: 'App Update' },
];

export default function PushNotifications() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [message, setMessage] = useState('');
  const [type, setType] = useState('alert');
  const [loading, setLoading] = useState(false);

  if (!user || user.role !== 'admin') { navigate('/'); return null; }

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title || !message) { toast.error('Title and message required'); return; }
    setLoading(true);
    try {
      await api.post('/admin/notifications/broadcast', {
        title,
        message,
        notification_type: type,
      });
      toast.success('Notification sent to all users!');
      setTitle('');
      setMessage('');
    } catch {
      toast.error('Failed to send notification');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto space-y-4 pb-4">
      <PageHeader title="Push Notification" backTo="/admin" />

      <form onSubmit={handleSubmit} className="space-y-4">
        <Card>
          <label className="block text-sm font-medium mb-2">Notification Type</label>
          <ToggleGroup
            options={NOTIFICATION_TYPES.map(nt => ({ label: nt.label, value: nt.value }))}
            value={type}
            onChange={(val) => setType(val ?? 'alert')}
          />
        </Card>

        <Card className="space-y-3">
          <FormInput
            label="Title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Notification title..."
            required
          />
          <FormTextarea
            label="Message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            rows={4}
            placeholder="Notification message..."
            required
          />
        </Card>

        <Button
          type="submit"
          variant="primary"
          loading={loading}
          loadingText="Sending..."
          fullWidth
          className="py-3"
        >
          Send to All Users
        </Button>
      </form>
    </div>
  );
}
