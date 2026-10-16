import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { StarRatingInput, FormTextarea, Button, Card } from '../components/ui';
import api from '../services/api';
import toast from 'react-hot-toast';

export default function WriteReview() {
  const { stallId } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState('');
  const [photo, setPhoto] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  if (!user) { navigate('/login'); return null; }

  const handlePhoto = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPhoto(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!rating) { toast.error('Please select a rating'); return; }
    if (!photo) { toast.error('A photo is required for reviews'); return; }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('stall_id', stallId);
      formData.append('rating', rating);
      formData.append('comment', comment);
      formData.append('photo', photo);

      await api.post('/reviews/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      toast.success('Review submitted! Pending admin approval.');
      navigate(`/stall/${stallId}`);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to submit review');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto pb-4">
      <h1 className="text-xl font-bold mb-4">Write Review</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Card>
          <label className="block text-sm font-medium mb-2">Rating</label>
          <StarRatingInput value={rating} onChange={setRating} />
        </Card>

        <Card>
          <FormTextarea
            label="Comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            rows={4}
            placeholder="Share your experience..."
          />
        </Card>

        <Card>
          <label className="block text-sm font-medium mb-2">Photo (Required)</label>
          <input type="file" accept="image/*" onChange={handlePhoto} className="text-sm" />
          {preview && (
            <img src={preview} alt="Preview" className="mt-3 rounded-lg max-w-xs max-h-48 object-cover" />
          )}
        </Card>

        <Button type="submit" loading={loading} loadingText="Submitting..." fullWidth>
          Submit Review
        </Button>
        <p className="text-xs text-gray-400 text-center">Reviews are moderated before being published.</p>
      </form>
    </div>
  );
}
