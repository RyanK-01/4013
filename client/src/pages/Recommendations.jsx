import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import api from '../services/api';
import { Card, ToggleGroup, Button } from '../components/ui';

const DIETARY_RESTRICTIONS = ['Halal', 'No seafood', 'No nuts', 'Vegetarian', 'No beef'];
const CUISINE_OPTIONS = ['Chinese Cuisine', 'Malay Cuisine', 'Seafood', 'Western', 'Indian Cuisine'];

export default function Recommendations() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1); // 1: filters, 2: confirm
  const [filters, setFilters] = useState({
    budget_type: null,
    budget_exact: '',
    budget_min: '',
    budget_max: '',
    dietary_restrictions: [],
    dietary_requirements: [],
    dietary_other: '',
    proximity_type: null,
    latitude: null,
    longitude: null,
    max_distance_km: 5,
    use_popularity: false,
    use_favourites: false,
    recommendation_mode: 'combined',
  });

  const useCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setFilters((f) => ({
            ...f,
            proximity_type: 'current',
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
          }));
          toast.success('Location detected!');
        },
        () => toast.error('Could not get location')
      );
    }
  };

  const handleConfirm = async () => {
    if (filters.budget_type === 'exact' && !filters.budget_exact) {
      toast.error('Please enter a budget amount'); return;
    }
    if (filters.budget_type === 'range' && (!filters.budget_min || !filters.budget_max)) {
      toast.error('Please enter both min and max budget'); return;
    }
    if (filters.budget_type === 'range' && Number(filters.budget_min) > Number(filters.budget_max)) {
      toast.error('Minimum budget cannot be greater than maximum'); return;
    }

    try {
      const payload = {
        ...filters,
        budget_exact: filters.budget_exact ? Number(filters.budget_exact) : null,
        budget_min: filters.budget_min ? Number(filters.budget_min) : null,
        budget_max: filters.budget_max ? Number(filters.budget_max) : null,
        max_distance_km: filters.proximity_type ? Number(filters.max_distance_km) : null,
      };
      const res = await api.post('/recommendations/', payload);

      if (res.data.length === 0) {
        toast.error('No matches found. Try adjusting your filters.');
        return;
      }

      navigate('/recommendation-flow', { state: { recommendations: res.data, filters: payload } });
    } catch {
      toast.error('Failed to generate recommendations');
    }
  };

  return (
    <div className="max-w-lg mx-auto space-y-6 pb-4">
      <h1 className="text-xl font-bold">
        {step === 1 ? 'Select Your Filters' : 'Confirm Your Selections'}
      </h1>

      {step === 1 && (
        <div className="space-y-5">
          {/* Budget */}
          <Card>
            <h3 className="font-semibold mb-3">Budget</h3>
            <ToggleGroup
              options={[{ label: 'Exact Value', value: 'exact' }, { label: 'Range', value: 'range' }]}
              value={filters.budget_type}
              onChange={(v) => setFilters((f) => ({ ...f, budget_type: v }))}
              className="mb-3"
            />
            {filters.budget_type === 'exact' && (
              <input
                type="number"
                placeholder="Enter budget ($)"
                value={filters.budget_exact}
                onChange={(e) => setFilters((f) => ({ ...f, budget_exact: e.target.value }))}
                className="w-full border rounded-lg px-3 py-2 text-sm"
                min="0"
                step="0.5"
              />
            )}
            {filters.budget_type === 'range' && (
              <div className="flex gap-2">
                <input
                  type="number"
                  placeholder="Min ($)"
                  value={filters.budget_min}
                  onChange={(e) => setFilters((f) => ({ ...f, budget_min: e.target.value }))}
                  className="flex-1 border rounded-lg px-3 py-2 text-sm"
                  min="0"
                  step="0.5"
                />
                <input
                  type="number"
                  placeholder="Max ($)"
                  value={filters.budget_max}
                  onChange={(e) => setFilters((f) => ({ ...f, budget_max: e.target.value }))}
                  className="flex-1 border rounded-lg px-3 py-2 text-sm"
                  min="0"
                  step="0.5"
                />
              </div>
            )}
          </Card>

          {/* Dietary Restrictions */}
          <Card>
            <h3 className="font-semibold mb-3">Dietary Restrictions</h3>
            <ToggleGroup
              multiple
              options={DIETARY_RESTRICTIONS}
              value={filters.dietary_restrictions}
              onChange={(v) => setFilters((f) => ({ ...f, dietary_restrictions: v }))}
              activeColor="bg-red-500 text-white"
            />
          </Card>

          {/* Cuisine Preferences */}
          <Card>
            <h3 className="font-semibold mb-3">Cuisine Preferences</h3>
            <ToggleGroup
              multiple
              options={CUISINE_OPTIONS}
              value={filters.dietary_requirements}
              onChange={(v) => setFilters((f) => ({ ...f, dietary_requirements: v }))}
              className="mb-3"
            />
            <input
              type="text"
              placeholder="Other cuisine (type here)"
              value={filters.dietary_other}
              onChange={(e) => setFilters((f) => ({ ...f, dietary_other: e.target.value }))}
              className="w-full border rounded-lg px-3 py-2 text-sm"
            />
          </Card>

          {/* Proximity — complex inline geocoding logic kept as-is */}
          <Card>
            <h3 className="font-semibold mb-3">Proximity</h3>
            <div className="flex gap-2 mb-3">
              <button
                onClick={useCurrentLocation}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  filters.proximity_type === 'current' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Use GPS Location
              </button>
              <button
                onClick={() => setFilters((f) => ({ ...f, proximity_type: f.proximity_type === 'selected' ? null : 'selected' }))}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  filters.proximity_type === 'selected' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Set Location
              </button>
            </div>
            {filters.proximity_type === 'selected' && (
              <div className="mb-3">
                <input
                  type="text"
                  placeholder="Search address (e.g. NTU, Clementi, Bugis)"
                  className="w-full border rounded-lg px-3 py-2 text-sm mb-1"
                  onKeyDown={async (e) => {
                    if (e.key === 'Enter' && e.target.value.trim()) {
                      try {
                        const res = await api.get('/geocode/search', { params: { q: e.target.value } });
                        const results = res.data.results || [];
                        if (results.length > 0) {
                          setFilters((f) => ({ ...f, latitude: results[0].latitude, longitude: results[0].longitude }));
                          toast.success(`Location set: ${results[0].building || results[0].address}`);
                        } else {
                          toast.error('No results found');
                        }
                      } catch { toast.error('Geocoding unavailable'); }
                    }
                  }}
                />
                <p className="text-xs text-gray-400">Press Enter to search (OneMap)</p>
              </div>
            )}
            {filters.proximity_type && (
              <div className="flex items-center gap-2">
                <label className="text-sm text-gray-600">Max distance:</label>
                <select
                  value={filters.max_distance_km}
                  onChange={(e) => setFilters((f) => ({ ...f, max_distance_km: Number(e.target.value) }))}
                  className="border rounded-lg px-3 py-1.5 text-sm"
                >
                  <option value={1}>1 km</option>
                  <option value={3}>3 km</option>
                  <option value={5}>5 km</option>
                  <option value={10}>10 km</option>
                  <option value={20}>20 km</option>
                  <option value={30}>30 km</option>
                </select>
              </div>
            )}
          </Card>

          {/* Popularity & Favourites — checkboxes kept as-is */}
          <Card className="space-y-3">
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={filters.use_popularity}
                onChange={(e) => setFilters((f) => ({ ...f, use_popularity: e.target.checked }))}
                className="w-5 h-5 text-orange-500 rounded"
              />
              <span className="text-sm font-medium">Sort by Popularity (Google Reviews)</span>
            </label>
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={filters.use_favourites}
                onChange={(e) => setFilters((f) => ({ ...f, use_favourites: e.target.checked }))}
                className="w-5 h-5 text-orange-500 rounded"
              />
              <span className="text-sm font-medium">Prioritize My Favourites</span>
            </label>
          </Card>

          {/* Recommendation Mode */}
          <Card>
            <h3 className="font-semibold mb-3">Recommendation Mode</h3>
            <ToggleGroup
              options={[{ label: 'Combined', value: 'combined' }, { label: 'Per Filter', value: 'individual' }]}
              value={filters.recommendation_mode}
              onChange={(v) => { if (v) setFilters((f) => ({ ...f, recommendation_mode: v })); }}
            />
          </Card>

          <Button variant="primary" fullWidth onClick={() => setStep(2)}>
            Review Filters
          </Button>
        </div>
      )}

      {step === 2 && (
        <div className="space-y-4">
          <Card className="space-y-2 text-sm">
            <h3 className="font-semibold text-base mb-3">Filter Summary</h3>
            {filters.budget_type && (
              <p><strong>Budget:</strong> {filters.budget_type === 'exact' ? `$${filters.budget_exact}` : `$${filters.budget_min} - $${filters.budget_max}`}</p>
            )}
            {filters.dietary_restrictions.length > 0 && (
              <p><strong>Restrictions:</strong> {filters.dietary_restrictions.join(', ')}</p>
            )}
            {filters.dietary_requirements.length > 0 && (
              <p><strong>Cuisine:</strong> {filters.dietary_requirements.join(', ')}{filters.dietary_other ? `, ${filters.dietary_other}` : ''}</p>
            )}
            {filters.proximity_type && (
              <p><strong>Proximity:</strong> Within {filters.max_distance_km} km of current location</p>
            )}
            <p><strong>Popularity:</strong> {filters.use_popularity ? 'Yes' : 'No'}</p>
            <p><strong>Favourites:</strong> {filters.use_favourites ? 'Prioritized' : 'No'}</p>
            <p><strong>Mode:</strong> {filters.recommendation_mode === 'combined' ? 'Combined results' : 'Per-filter results'}</p>
          </Card>

          <div className="flex gap-3">
            <Button variant="secondary" className="flex-1" onClick={() => setStep(1)}>
              Edit Filters
            </Button>
            <Button variant="primary" className="flex-1" onClick={handleConfirm}>
              Get Recommendations
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
