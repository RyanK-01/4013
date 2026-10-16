import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import toast from 'react-hot-toast';
import { PageHeader, LoadingSpinner, EmptyState, ApproveRejectButtons, Card, ProgressBar } from '../../components/ui';

export default function PendingCrowd() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user || user.role !== 'admin') { navigate('/'); return; }
    api.get('/admin/crowd-reports', { params: { approved: false } })
      .then((res) => setReports(res.data))
      .catch(() => toast.error('Failed to load'))
      .finally(() => setLoading(false));
  }, [user]);

  const handleDecision = async (id, approved) => {
    const reason = !approved ? prompt('Reason for rejection (optional):') : null;
    try {
      await api.put(`/admin/crowd-reports/${id}/approve`, { approved, reason });
      setReports((r) => r.filter((x) => x.id !== id));
      toast.success(approved ? 'Crowd report approved!' : 'Report rejected');
    } catch {
      toast.error('Action failed');
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-4 pb-4">
      <PageHeader title={`Pending Crowd Reports (${reports.length})`} backTo="/admin" />

      {reports.length === 0 && <EmptyState title="No pending crowd reports" />}

      {reports.map((report) => (
        <Card key={report.id}>
          <div className="flex justify-between items-start mb-2">
            <div>
              <p className="font-semibold text-sm">{report.stall_name || `Stall #${report.stall_id}`}</p>
              <p className="text-xs text-gray-500">By: {report.username || 'Unknown'}</p>
              <p className="text-xs text-gray-400">{new Date(report.created_at).toLocaleString()}</p>
            </div>
            <div className="text-right">
              <p className="text-2xl font-bold">{report.crowd_level}%</p>
              <p className="text-xs text-gray-500">Crowd Level</p>
            </div>
          </div>
          <div className="mb-3">
            <ProgressBar value={report.crowd_level} />
          </div>
          <ApproveRejectButtons
            onApprove={() => handleDecision(report.id, true)}
            onReject={() => handleDecision(report.id, false)}
          />
        </Card>
      ))}
    </div>
  );
}
