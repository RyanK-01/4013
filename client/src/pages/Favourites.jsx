import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { StallCard, LoadingSpinner, EmptyState } from '../components/ui';

export default function Favourites() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [favourites, setFavourites] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) { navigate('/login'); return; }
    api.get('/favourites/')
      .then((res) => setFavourites(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [user]);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold">My Favourites</h1>
      {favourites.length === 0 ? (
        <EmptyState
          title="No favourites yet"
          actionLabel="Browse stalls to add favourites"
          actionTo="/search"
        />
      ) : (
        <div className="space-y-3">
          {favourites.map((stall) => (
            <StallCard key={stall.id} stall={stall} />
          ))}
        </div>
      )}
    </div>
  );
}
