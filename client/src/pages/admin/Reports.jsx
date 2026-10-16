import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import toast from 'react-hot-toast';
import { PageHeader, LoadingSpinner, Badge, Card } from '../../components/ui';

export default function Reports() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [tab, setTab] = useState('bugs');
  const [bugReports, setBugReports] = useState([]);
  const [features, setFeatures] = useState([]);
  const [infoReports, setInfoReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user || user.role !== 'admin') { navigate('/'); return; }
    Promise.all([
      api.get('/admin/bug-reports'),
      api.get('/admin/feature-suggestions'),
      api.get('/admin/incorrect-info-reports'),
    ]).then(([bugs, feats, info]) => {
      setBugReports(bugs.data);
      setFeatures(feats.data);
      setInfoReports(info.data);
    }).catch(() => toast.error('Failed to load'))
      .finally(() => setLoading(false));
  }, [user]);

  const updateBugStatus = async (id, status) => {
    try {
      await api.put(`/admin/bug-reports/${id}/status`, { status });
      setBugReports((r) => r.map((x) => x.id === id ? { ...x, status } : x));
      toast.success(`Status updated to ${status}`);
    } catch { toast.error('Failed'); }
  };

  const updateInfoStatus = async (id, status) => {
    try {
      await api.put(`/admin/incorrect-info-reports/${id}/status`, { status });
      setInfoReports((r) => r.map((x) => x.id === id ? { ...x, status } : x));
      toast.success(`Status updated to ${status}`);
    } catch { toast.error('Failed'); }
  };

  if (loading) return <LoadingSpinner />;

  const statusColor = (status) =>
    status === 'pending' ? 'yellow' : status === 'resolved' ? 'green' : 'gray';

  const tabClass = (t) => `px-4 py-2 rounded-lg text-sm font-medium transition ${tab === t ? 'bg-orange-500 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`;

  return (
    <div className="space-y-4 pb-4">
      <PageHeader title="User Reports & Feedback" backTo="/admin" />

      <div className="flex gap-2">
        <button onClick={() => setTab('bugs')} className={tabClass('bugs')}>Bugs ({bugReports.length})</button>
        <button onClick={() => setTab('features')} className={tabClass('features')}>Features ({features.length})</button>
        <button onClick={() => setTab('info')} className={tabClass('info')}>Info Reports ({infoReports.length})</button>
      </div>

      {tab === 'bugs' && (
        <div className="space-y-2">
          {bugReports.length === 0 && <p className="text-gray-500 text-center py-8">No bug reports</p>}
          {bugReports.map((r) => (
            <Card key={r.id}>
              <div className="flex justify-between items-start mb-2">
                <div>
                  <Badge color="red">{r.category}</Badge>
                  <p className="text-xs text-gray-500 mt-1">By: {r.username} | {new Date(r.created_at).toLocaleDateString()}</p>
                </div>
                <Badge color={statusColor(r.status)}>{r.status}</Badge>
              </div>
              <p className="text-sm text-gray-700">{r.description}</p>
              {r.status === 'pending' && (
                <div className="flex gap-2 mt-2">
                  <button onClick={() => updateBugStatus(r.id, 'reviewed')} className="text-xs bg-blue-100 text-blue-600 px-3 py-1 rounded-lg hover:bg-blue-200">Mark Reviewed</button>
                  <button onClick={() => updateBugStatus(r.id, 'resolved')} className="text-xs bg-green-100 text-green-600 px-3 py-1 rounded-lg hover:bg-green-200">Mark Resolved</button>
                </div>
              )}
            </Card>
          ))}
        </div>
      )}

      {tab === 'features' && (
        <div className="space-y-2">
          {features.length === 0 && <p className="text-gray-500 text-center py-8">No feature suggestions</p>}
          {features.map((f) => (
            <Card key={f.id}>
              <div className="flex justify-between items-start mb-2">
                <p className="text-xs text-gray-500">By: {f.username} | {new Date(f.created_at).toLocaleDateString()}</p>
                <Badge color={statusColor(f.status)}>{f.status}</Badge>
              </div>
              <p className="text-sm text-gray-700">{f.description}</p>
            </Card>
          ))}
        </div>
      )}

      {tab === 'info' && (
        <div className="space-y-2">
          {infoReports.length === 0 && <p className="text-gray-500 text-center py-8">No incorrect info reports</p>}
          {infoReports.map((r) => (
            <Card key={r.id}>
              <div className="flex justify-between items-start mb-2">
                <div>
                  <Badge color="orange">{r.issue_type}</Badge>
                  <p className="text-xs text-gray-500 mt-1">Stall #{r.stall_id} | By: {r.username}</p>
                </div>
                <Badge color={statusColor(r.status)}>{r.status}</Badge>
              </div>
              <p className="text-sm text-gray-700">{r.description}</p>
              {r.status === 'pending' && (
                <div className="flex gap-2 mt-2">
                  <button onClick={() => updateInfoStatus(r.id, 'reviewed')} className="text-xs bg-blue-100 text-blue-600 px-3 py-1 rounded-lg hover:bg-blue-200">Reviewed</button>
                  <button onClick={() => updateInfoStatus(r.id, 'resolved')} className="text-xs bg-green-100 text-green-600 px-3 py-1 rounded-lg hover:bg-green-200">Resolved</button>
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
