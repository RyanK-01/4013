import { Link } from 'react-router-dom';
import { MdRestaurant, MdNearMe, MdCategory, MdStar, MdSearch } from 'react-icons/md';
import { FiPlus, FiAlertCircle, FiMessageSquare } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';

const CATEGORIES = [
  { name: 'Chinese Cuisine', emoji: '🥢' },
  { name: 'Malay Cuisine', emoji: '🍛' },
  { name: 'Indian Cuisine', emoji: '🫓' },
  { name: 'Western', emoji: '🍔' },
  { name: 'Seafood', emoji: '🦀' },
  { name: 'Japanese', emoji: '🍣' },
  { name: 'Korean', emoji: '🥘' },
  { name: 'Vegetarian', emoji: '🥗' },
  { name: 'Desserts', emoji: '🍰' },
  { name: 'Drinks', emoji: '🧋' },
];

export default function Home() {
  const { user } = useAuth();

  return (
    <div className="space-y-6 pb-4">
      {/* Hero */}
      <div className="bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">What are you craving?</h1>
        <p className="text-orange-100 mb-4">Find the best hawker food in Singapore</p>
        <div className="flex gap-3">
          <Link
            to="/recommendations"
            className="bg-white text-orange-600 font-semibold px-5 py-2.5 rounded-xl text-sm hover:bg-orange-50 transition flex items-center gap-2"
          >
            <MdRestaurant /> Get Recommendations
          </Link>
          <Link
            to="/search"
            className="bg-white/20 text-white font-semibold px-5 py-2.5 rounded-xl text-sm hover:bg-white/30 transition flex items-center gap-2"
          >
            <MdSearch /> Search
          </Link>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <Link to="/nearby" className="bg-white rounded-xl p-4 shadow-sm border hover:shadow-md transition text-center">
          <MdNearMe className="text-3xl text-blue-500 mx-auto mb-2" />
          <span className="text-sm font-medium">Nearby</span>
        </Link>
        <Link to="/recommendations" className="bg-white rounded-xl p-4 shadow-sm border hover:shadow-md transition text-center">
          <MdStar className="text-3xl text-yellow-500 mx-auto mb-2" />
          <span className="text-sm font-medium">For You</span>
        </Link>
        <Link to="/search" className="bg-white rounded-xl p-4 shadow-sm border hover:shadow-md transition text-center">
          <MdSearch className="text-3xl text-green-500 mx-auto mb-2" />
          <span className="text-sm font-medium">Search</span>
        </Link>
        {user ? (
          <Link to="/submit-stall" className="bg-white rounded-xl p-4 shadow-sm border hover:shadow-md transition text-center">
            <FiPlus className="text-3xl text-purple-500 mx-auto mb-2" />
            <span className="text-sm font-medium">Add Stall</span>
          </Link>
        ) : (
          <Link to="/login" className="bg-white rounded-xl p-4 shadow-sm border hover:shadow-md transition text-center">
            <MdRestaurant className="text-3xl text-purple-500 mx-auto mb-2" />
            <span className="text-sm font-medium">Sign In</span>
          </Link>
        )}
      </div>

      {/* Browse by Category */}
      <div>
        <h2 className="text-lg font-bold mb-3">Browse by Category</h2>
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
          {CATEGORIES.map((cat) => (
            <Link
              key={cat.name}
              to={`/browse/${encodeURIComponent(cat.name)}`}
              className="bg-white rounded-xl p-3 shadow-sm border hover:shadow-md transition flex items-center gap-2"
            >
              <span className="text-2xl">{cat.emoji}</span>
              <span className="text-sm font-medium truncate">{cat.name}</span>
            </Link>
          ))}
        </div>
      </div>

      {/* Feedback */}
      {user && (
        <div>
          <h2 className="text-lg font-bold mb-3">Help Us Improve</h2>
          <div className="flex gap-3">
            <Link to="/report-bug" className="flex-1 bg-white rounded-xl p-4 shadow-sm border hover:shadow-md transition flex items-center gap-3">
              <FiAlertCircle className="text-xl text-red-500" />
              <span className="text-sm font-medium">Report Bug</span>
            </Link>
            <Link to="/suggest-feature" className="flex-1 bg-white rounded-xl p-4 shadow-sm border hover:shadow-md transition flex items-center gap-3">
              <FiMessageSquare className="text-xl text-blue-500" />
              <span className="text-sm font-medium">Suggest Feature</span>
            </Link>
          </div>
        </div>
      )}

      {/* Data Sources */}
      <div className="bg-gray-100 rounded-xl p-3 text-center text-xs text-gray-400">
        Hawker data from <strong>data.gov.sg</strong> (NEA) | Geocoding by <strong>OneMap</strong> (SLA)
      </div>
    </div>
  );
}
