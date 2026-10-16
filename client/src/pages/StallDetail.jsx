import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { MdLocationOn, MdAccessTime, MdContentCopy, MdDirections } from 'react-icons/md';
import { FiHeart, FiAlertCircle } from 'react-icons/fi';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';
import { LoadingSpinner, PageHeader, Card, Badge, StarRatingBadge, ProgressBar } from '../components/ui';

export default function StallDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stall, setStall] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [isFav, setIsFav] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [stallRes, reviewRes] = await Promise.all([
          api.get(`/stalls/${id}`),
          api.get(`/stalls/${id}/reviews`),
        ]);
        setStall(stallRes.data);
        setReviews(reviewRes.data);
        if (user) {
          const favRes = await api.get(`/stalls/${id}/is-favourite`);
          setIsFav(favRes.data.is_favourite);
        }
      } catch {
        toast.error('Stall not found');
        navigate('/');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const toggleFavourite = async () => {
    if (!user) { navigate('/login'); return; }
    try {
      const res = await api.post(`/stalls/${id}/favourite`);
      setIsFav(res.data.is_favourite);
      toast.success(res.data.is_favourite ? 'Added to favourites!' : 'Removed from favourites');
    } catch {
      toast.error('Failed to update favourite');
    }
  };

  const copyAddress = () => {
    if (stall?.address) {
      navigator.clipboard.writeText(stall.address);
      toast.success('The address has been copied, please go to your navigation app!');
    }
  };

  const openGoogleMaps = () => {
    const url = stall.latitude && stall.longitude
      ? `https://www.google.com/maps/dir/?api=1&destination=${stall.latitude},${stall.longitude}`
      : `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(stall.address)}`;
    window.open(url, '_blank');
  };

  if (loading) return <LoadingSpinner />;
  if (!stall) return null;

  const days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
  const today = days[new Date().getDay()];
  const todayHours = stall.operating_hours?.[today];
  const isOpen = todayHours && todayHours.toLowerCase() !== 'closed';

  return (
    <div className="space-y-5 pb-4">
      <PageHeader title={stall.name} onBack={() => navigate(-1)}>
        <button onClick={toggleFavourite} className={`p-2 rounded-full ${isFav ? 'text-red-500 bg-red-50' : 'text-gray-400 hover:text-red-500'}`}>
          <FiHeart className={`text-xl ${isFav ? 'fill-current' : ''}`} />
        </button>
      </PageHeader>

      <Card className="space-y-3">
        {stall.description && <p className="text-sm text-gray-600">{stall.description}</p>}

        <div className="flex items-start gap-2 text-sm">
          <MdLocationOn className="text-gray-400 mt-0.5 shrink-0" />
          <span>{stall.address}</span>
        </div>

        <div className="flex items-center gap-2 text-sm">
          <MdAccessTime className="text-gray-400" />
          <span className={isOpen ? 'text-green-600 font-medium' : 'text-red-500 font-medium'}>
            {isOpen ? 'Open' : 'Closed'}
          </span>
          {todayHours && <span className="text-gray-500">({todayHours})</span>}
        </div>

        <div className="flex flex-wrap gap-2">
          {stall.cuisine_type && <Badge>{stall.cuisine_type}</Badge>}
          {stall.dietary_tags?.map((t) => (
            <Badge key={t.id} color="green">{t.tag}</Badge>
          ))}
          {stall.indoor_outdoor && <Badge color="blue">{stall.indoor_outdoor}</Badge>}
        </div>

        <div className="flex items-center gap-4">
          {stall.google_rating && (
            <StarRatingBadge rating={stall.google_rating} count={stall.google_review_count} />
          )}
          {stall.price_range_min != null && (
            <span className="text-sm text-gray-600">
              ${stall.price_range_min.toFixed(2)} - ${stall.price_range_max?.toFixed(2)}
            </span>
          )}
        </div>

        {stall.crowd_level != null && (
          <div>
            <ProgressBar value={stall.crowd_level} showLabel />
            <p className="text-xs text-gray-400 mt-1">* Crowd estimate is approximate and may not reflect real-time levels</p>
          </div>
        )}
      </Card>

      {/* Actions */}
      <div className="grid grid-cols-2 gap-3">
        <button onClick={openGoogleMaps} className="bg-blue-500 text-white font-medium py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-blue-600 transition">
          <MdDirections /> Google Maps
        </button>
        <button onClick={copyAddress} className="bg-gray-100 text-gray-700 font-medium py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-gray-200 transition">
          <MdContentCopy /> Copy Address
        </button>
        {user && (
          <>
            <Link to={`/write-review/${id}`} className="bg-orange-500 text-white font-medium py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-orange-600 transition">
              Write Review
            </Link>
            <Link to={`/submit-crowd/${id}`} className="bg-purple-500 text-white font-medium py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-purple-600 transition">
              Report Crowd
            </Link>
          </>
        )}
      </div>

      {/* Menu */}
      {stall.menu_items?.length > 0 && (
        <div>
          <h2 className="text-lg font-bold mb-3">Menu</h2>
          <div className="bg-white rounded-xl shadow-sm border divide-y">
            {stall.menu_items.map((item) => (
              <div key={item.id} className="p-4 flex justify-between items-center">
                <div>
                  <p className="font-medium">{item.name}</p>
                  {item.description && <p className="text-sm text-gray-500">{item.description}</p>}
                </div>
                {item.price != null && (
                  <span className="font-semibold text-orange-600">${item.price.toFixed(2)}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Operating Hours */}
      {stall.operating_hours && (
        <div>
          <h2 className="text-lg font-bold mb-3">Operating Hours</h2>
          <Card>
            {Object.entries(stall.operating_hours).map(([day, hours]) => (
              <div key={day} className={`flex justify-between py-1.5 text-sm ${day === today ? 'font-semibold text-orange-600' : ''}`}>
                <span className="capitalize">{day}</span>
                <span>{hours}</span>
              </div>
            ))}
          </Card>
        </div>
      )}

      {/* Reviews */}
      <div>
        <h2 className="text-lg font-bold mb-3">Reviews ({reviews.length})</h2>
        {reviews.length === 0 ? (
          <Card className="text-center text-gray-500">
            No reviews yet. Be the first to review!
          </Card>
        ) : (
          <div className="space-y-3">
            {reviews.map((review) => (
              <Card key={review.id}>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-sm">{review.username || 'Anonymous'}</span>
                  <StarRatingBadge rating={review.rating} />
                </div>
                {review.comment && <p className="text-sm text-gray-600 mb-2">{review.comment}</p>}
                {review.photo_url && (
                  <img src={review.photo_url} alt="Review" className="w-full max-w-xs rounded-lg" />
                )}
                <p className="text-xs text-gray-400 mt-2">{new Date(review.created_at).toLocaleDateString()}</p>
              </Card>
            ))}
          </div>
        )}
      </div>

      {user && (
        <button
          onClick={() => {
            const issue = prompt('What information is incorrect? (e.g., Wrong hours, Wrong price, Closed permanently)');
            if (issue) {
              api.post('/reports/incorrect-info', { stall_id: Number(id), issue_type: 'User Report', description: issue })
                .then(() => toast.success('Report submitted. Thank you!'))
                .catch(() => toast.error('Failed to submit report'));
            }
          }}
          className="w-full text-sm text-gray-400 hover:text-gray-600 flex items-center justify-center gap-1 py-2"
        >
          <FiAlertCircle /> Report Incorrect Information
        </button>
      )}
    </div>
  );
}
