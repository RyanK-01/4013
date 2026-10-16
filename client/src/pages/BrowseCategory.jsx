import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import { StallCard, LoadingSpinner, EmptyState, PageHeader } from '../components/ui';

export default function BrowseCategory() {
  const { category } = useParams();
  const [stalls, setStalls] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCategory = async () => {
      setLoading(true);
      try {
        let lat, lng;
        if (navigator.geolocation) {
          const pos = await new Promise((resolve, reject) =>
            navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 5000 })
          ).catch(() => null);
          if (pos) {
            lat = pos.coords.latitude;
            lng = pos.coords.longitude;
          }
        }
        const params = { limit: 10 };
        if (lat && lng) {
          params.lat = lat;
          params.lng = lng;
        }
        const res = await api.get(`/stalls/browse/${encodeURIComponent(category)}`, { params });
        setStalls(res.data);
      } catch {
        setStalls([]);
      } finally {
        setLoading(false);
      }
    };
    fetchCategory();
  }, [category]);

  return (
    <div className="space-y-4">
      <PageHeader title={decodeURIComponent(category)} backTo="/" />

      {loading && <LoadingSpinner />}

      {!loading && stalls.length === 0 && (
        <EmptyState
          title="No stalls found in this category"
          actionLabel="Browse other categories"
          actionTo="/"
        />
      )}

      <div className="space-y-3">
        {stalls.map((stall) => (
          <StallCard key={stall.id} stall={stall} />
        ))}
      </div>
    </div>
  );
}
