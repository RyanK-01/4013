import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import toast from 'react-hot-toast';
import { PageHeader, LoadingSpinner, EmptyState, ApproveRejectButtons, Card } from '../../components/ui';

export default function PendingStalls() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stalls, setStalls] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user || user.role !== 'admin') { navigate('/'); return; }
    api.get('/admin/stalls', { params: { approved: false } })
      .then((res) => setStalls(res.data))
      .catch(() => toast.error('Failed to load'))
      .finally(() => setLoading(false));
  }, [user]);

  const handleDecision = async (id, approved) => {
    const reason = !approved ? prompt('Reason for rejection (optional):') : null;
    try {
      await api.put(`/admin/stalls/${id}/approve`, { approved, reason });
      setStalls((s) => s.filter((x) => x.id !== id));
      toast.success(approved ? 'Stall approved!' : 'Stall rejected');
    } catch {
      toast.error('Action failed');
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-4 pb-4">
      <PageHeader title={`Pending Stall Submissions (${stalls.length})`} backTo="/admin" />

      {stalls.length === 0 && <EmptyState title="No pending submissions" />}

      {stalls.map((stall) => (
        <Card key={stall.id}>
          <h3 className="font-semibold">{stall.name}</h3>
          <p className="text-sm text-gray-500">{stall.address}</p>
          <p className="text-sm text-gray-500">{stall.cuisine_type} | ${stall.price_range_min} - ${stall.price_range_max}</p>
          {stall.description && <p className="text-sm text-gray-600 mt-1">{stall.description}</p>}
          <div className="mt-3">
            <ApproveRejectButtons
              onApprove={() => handleDecision(stall.id, true)}
              onReject={() => handleDecision(stall.id, false)}
            />
          </div>
        </Card>
      ))}
    </div>
  );
}
