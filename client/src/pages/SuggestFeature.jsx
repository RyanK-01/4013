import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FormTextarea, Button, Card } from '../components/ui';
import api from '../services/api';
import toast from 'react-hot-toast';

export default function SuggestFeature() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  if (!user) { navigate('/login'); return null; }

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!description.trim()) { toast.error('Please describe your suggestion'); return; }
    setLoading(true);
    try {
      await api.post('/reports/features', { description });
      toast.success('Suggestion submitted. Thank you!');
      navigate('/');
    } catch {
      toast.error('Failed to submit suggestion');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto pb-4">
      <h1 className="text-xl font-bold mb-4">Suggest a Feature</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Card>
          <FormTextarea
            label="Your Suggestion"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={6}
            placeholder="Describe the feature or design change you'd like to see..."
            required
          />
        </Card>
        <Button type="submit" variant="blue" loading={loading} loadingText="Submitting..." fullWidth>
          Submit Suggestion
        </Button>
      </form>
    </div>
  );
}
