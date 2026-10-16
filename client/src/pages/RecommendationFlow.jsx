import { useState } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { MdStar, MdLocationOn, MdCheck, MdClose, MdBookmark } from 'react-icons/md';
import toast from 'react-hot-toast';
import { EmptyState, Badge, StarRatingBadge } from '../components/ui';

export default function RecommendationFlow() {
  const location = useLocation();
  const navigate = useNavigate();
  const recommendations = location.state?.recommendations || [];
  const [currentIndex, setCurrentIndex] = useState(0);
  const [viewLater, setViewLater] = useState([]);
  const [confirmed, setConfirmed] = useState(null);

  if (recommendations.length === 0) {
    return (
      <EmptyState
        title="No recommendations available"
        actionLabel="Set up filters first"
        actionTo="/recommendations"
      />
    );
  }

  if (confirmed) {
    return (
      <div className="max-w-lg mx-auto space-y-4 pb-4">
        <div className="bg-green-50 border border-green-200 rounded-xl p-6 text-center">
          <MdCheck className="text-4xl text-green-500 mx-auto mb-2" />
          <h2 className="text-lg font-bold text-green-800">Great choice!</h2>
          <p className="text-sm text-green-600 mt-1">You selected:</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-sm border">
          <h3 className="text-xl font-bold mb-2">{confirmed.name}</h3>
          <p className="text-sm text-gray-500 flex items-center gap-1 mb-3">
            <MdLocationOn /> {confirmed.address}
          </p>
          {confirmed.google_rating && (
            <div className="flex items-center gap-1 mb-3">
              <MdStar className="text-yellow-500" />
              <span className="font-semibold">{confirmed.google_rating}</span>
            </div>
          )}
        </div>
        <div className="flex gap-3">
          <Link
            to={`/stall/${confirmed.id}`}
            className="flex-1 bg-orange-500 text-white font-semibold py-3 rounded-xl text-center hover:bg-orange-600 transition"
          >
            View Full Details
          </Link>
          <button
            onClick={() => {
              const url = confirmed.latitude && confirmed.longitude
                ? `https://www.google.com/maps/dir/?api=1&destination=${confirmed.latitude},${confirmed.longitude}`
                : `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(confirmed.address)}`;
              window.open(url, '_blank');
            }}
            className="flex-1 bg-blue-500 text-white font-semibold py-3 rounded-xl hover:bg-blue-600 transition"
          >
            Open in Maps
          </button>
        </div>
        <button onClick={() => navigate('/')} className="w-full text-sm text-gray-500 hover:text-gray-700 py-2">
          Return to Home
        </button>
      </div>
    );
  }

  // If we've gone through all, show view-later stack
  if (currentIndex >= recommendations.length) {
    if (viewLater.length === 0) {
      toast('All recommendations have been shown and none is confirmed, returning back to the homepage!');
      navigate('/');
      return null;
    }
    navigate('/view-later', { state: { viewLater } });
    return null;
  }

  const stall = recommendations[currentIndex];

  return (
    <div className="max-w-lg mx-auto space-y-4 pb-4">
      <div className="text-sm text-gray-500 text-center">
        Recommendation {currentIndex + 1} of {recommendations.length}
      </div>

      {/* Stall Card */}
      <div className="bg-white rounded-2xl shadow-md border p-6 space-y-3">
        <h2 className="text-xl font-bold">{stall.name}</h2>
        {stall.description && <p className="text-sm text-gray-600">{stall.description}</p>}
        <p className="text-sm text-gray-500 flex items-center gap-1">
          <MdLocationOn className="text-gray-400" /> {stall.address}
        </p>
        <div className="flex items-center gap-3">
          {stall.cuisine_type && <Badge color="orange">{stall.cuisine_type}</Badge>}
          {stall.google_rating && <StarRatingBadge rating={stall.google_rating} />}
          {stall.price_range_min != null && (
            <span className="text-sm text-gray-600">${stall.price_range_min?.toFixed(2)} - ${stall.price_range_max?.toFixed(2)}</span>
          )}
        </div>
        {stall.distance != null && (
          <p className="text-sm text-blue-600">{stall.distance} km away</p>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button
          onClick={() => {
            setCurrentIndex((i) => i + 1);
          }}
          className="flex-1 bg-red-100 text-red-600 font-semibold py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-red-200 transition"
        >
          <MdClose className="text-xl" /> Reject
        </button>
        <button
          onClick={() => {
            setViewLater((v) => [...v, stall]);
            setCurrentIndex((i) => i + 1);
            toast('Saved for later!', { icon: '🔖' });
          }}
          className="flex-1 bg-blue-100 text-blue-600 font-semibold py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-blue-200 transition"
        >
          <MdBookmark className="text-xl" /> View Later
        </button>
        <button
          onClick={() => setConfirmed(stall)}
          className="flex-1 bg-green-500 text-white font-semibold py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-green-600 transition"
        >
          <MdCheck className="text-xl" /> Confirm
        </button>
      </div>
    </div>
  );
}
