import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FormTextarea, Button, Card, ToggleGroup } from '../components/ui';
import api from '../services/api';
import toast from 'react-hot-toast';

const BUG_CATEGORIES = ['UI Bug', 'Data Error', 'Crash', 'Performance Issue', 'Navigation Issue', 'Others'];

export default function ReportBug() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [category, setCategory] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  if (!user) { navigate('/login'); return null; }

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!category || !description) { toast.error('Please fill all fields'); return; }
    setLoading(true);
    try {
      await api.post('/reports/bugs', { category, description });
      toast.success('Bug report submitted. Thank you!');
      navigate('/');
    } catch {
      toast.error('Failed to submit report');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto pb-4">
      <h1 className="text-xl font-bold mb-4">Report a Bug</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Card>
          <label className="block text-sm font-medium mb-2">Bug Category</label>
          <ToggleGroup
            options={BUG_CATEGORIES}
            value={category}
            onChange={setCategory}
            activeColor="bg-red-500 text-white"
          />
        </Card>
        <Card>
          <FormTextarea
            label="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={5}
            placeholder="Describe the bug you encountered..."
            required
          />
        </Card>
        <Button type="submit" variant="danger" loading={loading} loadingText="Submitting..." fullWidth>
          Submit Bug Report
        </Button>
      </form>
    </div>
  );
}
