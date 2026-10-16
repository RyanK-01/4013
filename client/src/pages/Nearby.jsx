import { useState, useEffect } from 'react';
import { MdMyLocation, MdSearch } from 'react-icons/md';
import api from '../services/api';
import toast from 'react-hot-toast';
import { StallCard, LoadingSpinner, EmptyState } from '../components/ui';

export default function Nearby() {
  const [stalls, setStalls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [location, setLocation] = useState(null);
  const [locationSource, setLocationSource] = useState('');
  const [manualAddress, setManualAddress] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [radius, setRadius] = useState(5);

  const getLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setLocation({ lat: pos.coords.latitude, lng: pos.coords.longitude });
          setLocationSource('GPS');
        },
        () => {
          toast.error('Location access denied. Enter an address below to set your location.');
          setLocation({ lat: 1.3521, lng: 103.8198 });
          setLocationSource('Default (SG centre)');
        }
      );
    } else {
      setLocation({ lat: 1.3521, lng: 103.8198 });
      setLocationSource('Default (SG centre)');
    }
  };

  useEffect(() => {
    getLocation();
  }, []);

  useEffect(() => {
    if (location) fetchNearby();
  }, [location, radius]);

  const fetchNearby = async () => {
    setLoading(true);
    try {
      const res = await api.get('/stalls/nearby', {
        params: { lat: location.lat, lng: location.lng, radius_km: radius },
      });
      setStalls(res.data);
    } catch {
      toast.error('Failed to fetch nearby stalls');
    } finally {
      setLoading(false);
    }
  };

  const searchAddress = async () => {
    if (!manualAddress.trim()) return;
    try {
      const res = await api.get('/geocode/search', { params: { q: manualAddress } });
      setSearchResults(res.data.results || []);
      if (res.data.results?.length === 0) {
        toast.error('No results found. Try a different address.');
      }
    } catch {
      toast.error('Geocoding service unavailable');
    }
  };

  const selectAddress = (result) => {
    setLocation({ lat: result.latitude, lng: result.longitude });
    setLocationSource(`Manual: ${result.address || result.building}`);
    setSearchResults([]);
    setManualAddress('');
    toast.success('Location set!');
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold">Nearby Eateries</h1>
        <button
          onClick={getLocation}
          className="flex items-center gap-1 text-sm text-orange-500 hover:text-orange-600"
        >
          <MdMyLocation /> Use GPS
        </button>
      </div>

      {/* Manual Location (OneMap) */}
      <div className="bg-white rounded-xl p-3 shadow-sm border">
        <p className="text-xs text-gray-500 mb-2">
          Current: <strong>{locationSource || 'detecting...'}</strong>
        </p>
        <div className="flex gap-2">
          <input
            type="text"
            value={manualAddress}
            onChange={(e) => setManualAddress(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && searchAddress()}
            placeholder="Set location manually (e.g. NTU, Clementi, Bugis)"
            className="flex-1 border rounded-lg px-3 py-2 text-sm"
          />
          <button onClick={searchAddress} className="bg-blue-500 text-white px-3 rounded-lg hover:bg-blue-600 transition">
            <MdSearch />
          </button>
        </div>
        {searchResults.length > 0 && (
          <div className="mt-2 border rounded-lg divide-y max-h-40 overflow-y-auto">
            {searchResults.map((r, i) => (
              <button
                key={i}
                onClick={() => selectAddress(r)}
                className="w-full text-left px-3 py-2 text-sm hover:bg-orange-50 transition"
              >
                <p className="font-medium">{r.building || r.address}</p>
                <p className="text-xs text-gray-500">{r.address} {r.postal_code && `(${r.postal_code})`}</p>
              </button>
            ))}
          </div>
        )}
        <p className="text-xs text-gray-400 mt-1">Powered by OneMap (Singapore Land Authority)</p>
      </div>

      <div className="flex gap-2 items-center">
        <label className="text-sm text-gray-600">Radius:</label>
        <select
          value={radius}
          onChange={(e) => setRadius(Number(e.target.value))}
          className="border rounded-lg px-3 py-1.5 text-sm"
        >
          <option value={1}>1 km</option>
          <option value={3}>3 km</option>
          <option value={5}>5 km</option>
          <option value={10}>10 km</option>
          <option value={20}>20 km</option>
          <option value={30}>30 km</option>
        </select>
        <span className="text-xs text-gray-400 ml-auto">{stalls.length} results</span>
      </div>

      {loading && <LoadingSpinner message="Finding nearby stalls..." />}

      {!loading && stalls.length === 0 && (
        <EmptyState
          title="No stalls found nearby"
          subtitle="Try increasing the search radius or changing your location"
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
