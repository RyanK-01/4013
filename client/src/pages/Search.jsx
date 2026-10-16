import { useState } from 'react';
import { FiSearch } from 'react-icons/fi';
import api from '../services/api';
import { StallCard, LoadingSpinner, EmptyState } from '../components/ui';

export default function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e) => {
    e?.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setSearched(true);
    try {
      const res = await api.get('/stalls/', { params: { search: query } });
      setResults(res.data);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSearch} className="flex gap-2">
        <div className="relative flex-1">
          <FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for food, stalls, cuisines..."
            className="w-full border rounded-xl pl-10 pr-4 py-3 text-sm focus:ring-2 focus:ring-orange-500 focus:border-orange-500 outline-none"
            autoFocus
          />
        </div>
        <button
          type="submit"
          className="bg-orange-500 text-white px-5 rounded-xl font-medium hover:bg-orange-600 transition"
        >
          Search
        </button>
      </form>

      {loading && <LoadingSpinner message="Searching..." />}

      {!loading && searched && results.length === 0 && (
        <EmptyState
          title="No results found"
          subtitle='Try different keywords like "Chicken Rice", "Nasi Lemak", or "Western"'
        />
      )}

      <div className="space-y-3">
        {results.map((stall) => (
          <StallCard key={stall.id} stall={stall} />
        ))}
      </div>
    </div>
  );
}
