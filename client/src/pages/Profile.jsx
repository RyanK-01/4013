import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FiHeart, FiAlertCircle, FiMessageSquare, FiLogOut, FiPlus } from 'react-icons/fi';

export default function Profile() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  if (!user) { navigate('/login'); return null; }

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="max-w-lg mx-auto space-y-4 pb-4">
      <div className="bg-white rounded-xl p-6 shadow-sm border text-center">
        <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-3">
          <span className="text-2xl font-bold text-orange-500">{user.username[0].toUpperCase()}</span>
        </div>
        <h2 className="text-lg font-bold">{user.username}</h2>
        <p className="text-sm text-gray-500">{user.email}</p>
        <span className="inline-block mt-2 text-xs bg-orange-100 text-orange-700 px-2 py-0.5 rounded-full font-medium capitalize">
          {user.role}
        </span>
      </div>

      <div className="bg-white rounded-xl shadow-sm border divide-y">
        <Link to="/favourites" className="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition">
          <FiHeart className="text-red-500" />
          <span className="text-sm font-medium">My Favourites</span>
        </Link>
        <Link to="/submit-stall" className="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition">
          <FiPlus className="text-purple-500" />
          <span className="text-sm font-medium">Submit New Stall</span>
        </Link>
        <Link to="/report-bug" className="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition">
          <FiAlertCircle className="text-red-500" />
          <span className="text-sm font-medium">Report Bug</span>
        </Link>
        <Link to="/suggest-feature" className="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition">
          <FiMessageSquare className="text-blue-500" />
          <span className="text-sm font-medium">Suggest Feature</span>
        </Link>
      </div>

      <button
        onClick={handleLogout}
        className="w-full bg-red-50 text-red-600 font-semibold py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-red-100 transition"
      >
        <FiLogOut /> Sign Out
      </button>
    </div>
  );
}
