import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button, Card, ProgressBar } from '../components/ui';
import api from '../services/api';
import toast from 'react-hot-toast';

export default function SubmitCrowdReport() {
  const { stallId } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [crowdLevel, setCrowdLevel] = useState(50);
  const [loading, setLoading] = useState(false);

  if (!user) { navigate('/login'); return null; }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post('/reports/crowd', { stall_id: Number(stallId), crowd_level: crowdLevel });
      toast.success('Crowd report submitted! Pending admin approval.');
      navigate(`/stall/${stallId}`);
    } catch {
      toast.error('Failed to submit crowd report');
    } finally {
      setLoading(false);
    }
  };

  const getLabel = () => {
    if (crowdLevel < 30) return { text: 'Not Crowded', color: 'text-green-600' };
    if (crowdLevel < 60) return { text: 'Moderate', color: 'text-yellow-600' };
    if (crowdLevel < 80) return { text: 'Crowded', color: 'text-orange-600' };
    return { text: 'Very Crowded', color: 'text-red-600' };
  };

  const label = getLabel();

  return (
    <div className="max-w-lg mx-auto pb-4">
      <h1 className="text-xl font-bold mb-4">Submit Crowd Report</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Card className="p-6 text-center space-y-4">
          <p className="text-sm text-gray-600">How crowded is this place right now?</p>

          <div className="text-5xl font-bold">{crowdLevel}%</div>
          <p className={`text-lg font-semibold ${label.color}`}>{label.text}</p>

          <input
            type="range"
            min="0"
            max="100"
            value={crowdLevel}
            onChange={(e) => setCrowdLevel(Number(e.target.value))}
            className="w-full h-3 rounded-full accent-orange-500"
          />

          <div className="flex justify-between text-xs text-gray-400">
            <span>Empty (0%)</span>
            <span>Full (100%)</span>
          </div>

          <ProgressBar value={crowdLevel} height="h-4" />
        </Card>

        <Button type="submit" variant="purple" loading={loading} loadingText="Submitting..." fullWidth>
          Submit Report
        </Button>
        <p className="text-xs text-gray-400 text-center">Reports are moderated before being published.</p>
      </form>
    </div>
  );
}
