import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import toast from 'react-hot-toast';
import { PageHeader, LoadingSpinner, EmptyState, ApproveRejectButtons, Card, StarRatingBadge } from '../../components/ui';

export default function PendingReviews() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user || user.role !== 'admin') { navigate('/'); return; }
    api.get('/admin/reviews', { params: { approved: false } })
      .then((res) => setReviews(res.data))
      .catch(() => toast.error('Failed to load'))
      .finally(() => setLoading(false));
  }, [user]);

  const handleDecision = async (id, approved) => {
    const reason = !approved ? prompt('Reason for rejection (optional):') : null;
    try {
      await api.put(`/admin/reviews/${id}/approve`, { approved, reason });
      setReviews((r) => r.filter((x) => x.id !== id));
      toast.success(approved ? 'Review approved!' : 'Review rejected');
    } catch {
      toast.error('Action failed');
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-4 pb-4">
      <PageHeader title={`Pending Reviews (${reviews.length})`} backTo="/admin" />

      {reviews.length === 0 && <EmptyState title="No pending reviews" />}

      {reviews.map((review) => (
        <Card key={review.id}>
          <div className="flex justify-between items-start mb-2">
            <div>
              <p className="font-semibold text-sm">Stall: {review.stall_name || `#${review.stall_id}`}</p>
              <p className="text-xs text-gray-500">By: {review.username || 'Unknown'}</p>
            </div>
            <StarRatingBadge rating={review.rating} />
          </div>
          {review.comment && <p className="text-sm text-gray-600 mb-2">{review.comment}</p>}
          {review.photo_url && (
            <img src={review.photo_url} alt="Review" className="rounded-lg max-h-40 mb-3 object-cover" />
          )}
          <ApproveRejectButtons
            onApprove={() => handleDecision(review.id, true)}
            onReject={() => handleDecision(review.id, false)}
          />
        </Card>
      ))}
    </div>
  );
}
