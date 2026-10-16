import { useState } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { MdLocationOn, MdCheck, MdClose } from 'react-icons/md';
import toast from 'react-hot-toast';
import { EmptyState, Badge, StarRatingBadge } from '../components/ui';

export default function ViewLater() {
  const location = useLocation();
  const navigate = useNavigate();
  const savedList = location.state?.viewLater || [];
  const [currentIndex, setCurrentIndex] = useState(0);
  const [confirmed, setConfirmed] = useState(null);

  if (savedList.length === 0) {
    return (
      <EmptyState
        title="No saved recommendations"
        actionLabel="Get new recommendations"
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
        </div>
        <div className="bg-white rounded-xl p-5 shadow-sm border">
          <h3 className="text-xl font-bold mb-2">{confirmed.name}</h3>
          <p className="text-sm text-gray-500 flex items-center gap-1"><MdLocationOn /> {confirmed.address}</p>
        </div>
        <div className="flex gap-3">
          <Link to={`/stall/${confirmed.id}`} className="flex-1 bg-orange-500 text-white font-semibold py-3 rounded-xl text-center hover:bg-orange-600 transition">
            View Details
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
      </div>
    );
  }

  if (currentIndex >= savedList.length) {
    toast('All recommendations have been shown and none is confirmed, returning back to the homepage!');
    navigate('/');
    return null;
  }

  const stall = savedList[currentIndex];

  return (
    <div className="max-w-lg mx-auto space-y-4 pb-4">
      <h1 className="text-lg font-bold text-center">Saved Recommendations</h1>
      <div className="text-sm text-gray-500 text-center">
        {currentIndex + 1} of {savedList.length}
      </div>

      <div className="bg-white rounded-2xl shadow-md border p-6 space-y-3">
        <h2 className="text-xl font-bold">{stall.name}</h2>
        <p className="text-sm text-gray-500 flex items-center gap-1">
          <MdLocationOn className="text-gray-400" /> {stall.address}
        </p>
        <div className="flex items-center gap-3">
          {stall.cuisine_type && <Badge color="orange">{stall.cuisine_type}</Badge>}
          {stall.google_rating && <StarRatingBadge rating={stall.google_rating} />}
        </div>
      </div>

      <div className="flex gap-3">
        <button
          onClick={() => setCurrentIndex((i) => i + 1)}
          className="flex-1 bg-red-100 text-red-600 font-semibold py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-red-200 transition"
        >
          <MdClose className="text-xl" /> Reject
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
