import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import toast from 'react-hot-toast';
import { MdDelete } from 'react-icons/md';
import { PageHeader, LoadingSpinner } from '../../components/ui';

export default function ManageStalls() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stalls, setStalls] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user || user.role !== 'admin') { navigate('/'); return; }
    fetchStalls();
  }, [user]);

  const fetchStalls = async () => {
    try {
      const res = await api.get('/admin/stalls', { params: { approved: true } });
      setStalls(res.data);
    } catch {
      toast.error('Failed to load stalls');
    } finally {
      setLoading(false);
    }
  };

  const deleteStall = async (id, name) => {
    if (!confirm(`Delete "${name}"? This cannot be undone.`)) return;
    try {
      await api.delete(`/admin/stalls/${id}`);
      setStalls((s) => s.filter((x) => x.id !== id));
      toast.success('Stall deleted');
    } catch {
      toast.error('Failed to delete');
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-4 pb-4">
      <PageHeader title={`Manage Stalls (${stalls.length})`} backTo="/admin" />

      <div className="space-y-2">
        {stalls.map((stall) => (
          <div key={stall.id} className="bg-white rounded-xl p-4 shadow-sm border flex justify-between items-center">
            <div>
              <Link to={`/stall/${stall.id}`} className="font-semibold text-sm hover:text-orange-500">{stall.name}</Link>
              <p className="text-xs text-gray-500">{stall.cuisine_type} | {stall.address?.slice(0, 60)}</p>
            </div>
            <button onClick={() => deleteStall(stall.id, stall.name)} className="text-red-400 hover:text-red-600 p-2">
              <MdDelete className="text-xl" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
