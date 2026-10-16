import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useState, useEffect } from 'react';
import { FiHome, FiSearch, FiHeart, FiUser, FiBell, FiSettings, FiLogOut, FiMenu, FiX } from 'react-icons/fi';
import { MdRestaurant } from 'react-icons/md';
import api from '../services/api';

/**
 * App shell providing sticky top header, mobile hamburger menu, and bottom tab navigation.
 * Renders child routes via <Outlet /> and fetches the unread notification count for logged-in users.
 */
export default function Layout() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [unreadCount, setUnreadCount] = useState(0);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    if (user) {
      api.get('/notifications/unread-count').then(res => setUnreadCount(res.data.count)).catch(() => {});
    }
  }, [user, location.pathname]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path || (path === '/admin' && location.pathname.startsWith('/admin'));
  const navClass = (path) =>
    `flex flex-col items-center gap-0.5 text-xs transition-colors ${isActive(path) ? 'text-orange-500' : 'text-gray-500 hover:text-gray-700'}`;

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Top Nav */}
      <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-orange-500 font-bold text-lg">
            <MdRestaurant className="text-2xl" />
            <span>HawkerLah!</span>
          </Link>
          <div className="flex items-center gap-3">
            {user && (
              <Link to="/notifications" className="relative p-2 text-gray-600 hover:text-gray-900">
                <FiBell className="text-xl" />
                {unreadCount > 0 && (
                  <span className="absolute -top-0.5 -right-0.5 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {unreadCount > 9 ? '9+' : unreadCount}
                  </span>
                )}
              </Link>
            )}
            {user?.role === 'admin' && (
              <Link to="/admin" className="text-sm font-medium text-orange-600 hover:text-orange-700 px-2 py-1 bg-orange-50 rounded-md">
                Admin
              </Link>
            )}
            <button onClick={() => setMenuOpen(!menuOpen)} className="p-2 text-gray-600 hover:text-gray-900 md:hidden">
              {menuOpen ? <FiX className="text-xl" /> : <FiMenu className="text-xl" />}
            </button>
          </div>
        </div>
        {/* Mobile menu */}
        {menuOpen && (
          <div className="md:hidden bg-white border-t px-4 py-3 space-y-2">
            {user ? (
              <>
                <div className="text-sm text-gray-500 pb-2 border-b">Signed in as <strong>{user.username}</strong></div>
                <Link to="/favourites" className="block py-2 text-sm" onClick={() => setMenuOpen(false)}>Favourites</Link>
                <Link to="/report-bug" className="block py-2 text-sm" onClick={() => setMenuOpen(false)}>Report Bug</Link>
                <Link to="/suggest-feature" className="block py-2 text-sm" onClick={() => setMenuOpen(false)}>Suggest Feature</Link>
                <button onClick={handleLogout} className="block py-2 text-sm text-red-500">Logout</button>
              </>
            ) : (
              <>
                <Link to="/login" className="block py-2 text-sm" onClick={() => setMenuOpen(false)}>Login</Link>
                <Link to="/register" className="block py-2 text-sm" onClick={() => setMenuOpen(false)}>Register</Link>
              </>
            )}
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-5xl w-full mx-auto px-4 py-4">
        <Outlet />
      </main>

      {/* Bottom Nav (mobile-style) */}
      <nav className="bg-white border-t border-gray-200 sticky bottom-0 z-50">
        <div className="max-w-5xl mx-auto px-4 py-2 flex justify-around">
          <Link to="/" className={navClass('/')}>
            <FiHome className="text-xl" />
            <span>Home</span>
          </Link>
          <Link to="/search" className={navClass('/search')}>
            <FiSearch className="text-xl" />
            <span>Search</span>
          </Link>
          <Link to="/recommendations" className={navClass('/recommendations')}>
            <MdRestaurant className="text-xl" />
            <span>Recommend</span>
          </Link>
          <Link to="/favourites" className={navClass('/favourites')}>
            <FiHeart className="text-xl" />
            <span>Favourites</span>
          </Link>
          <Link to={user ? '/profile' : '/login'} className={navClass(user ? '/profile' : '/login')}>
            <FiUser className="text-xl" />
            <span>{user ? 'Profile' : 'Login'}</span>
          </Link>
          {user?.role === 'admin' && (
            <Link to="/admin" className={navClass('/admin')}>
              <FiSettings className="text-xl" />
              <span>Admin</span>
            </Link>
          )}
        </div>
      </nav>
    </div>
  );
}
