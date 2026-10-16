import { Link, useNavigate } from 'react-router-dom';
import { MdArrowBack } from 'react-icons/md';

/**
 * Top-of-page header bar with a back button, title, and optional trailing actions.
 * Falls back to browser history when neither onBack nor backTo is supplied.
 * @param {string} title - Page heading text
 * @param {string} [backTo] - Route path to navigate to on back press
 * @param {Function} [onBack] - Custom back handler (overrides backTo)
 * @param {React.ReactNode} [children] - Trailing elements (e.g. action buttons)
 */
export default function PageHeader({ title, backTo, onBack, children }) {
  const navigate = useNavigate();

  const handleBack = () => {
    if (onBack) onBack();
    else if (backTo) navigate(backTo);
    else navigate(-1);
  };

  return (
    <div className="flex items-center gap-3">
      <button onClick={handleBack} className="text-gray-500 hover:text-gray-700">
        <MdArrowBack className="text-xl" />
      </button>
      <h1 className="text-xl font-bold flex-1">{title}</h1>
      {children}
    </div>
  );
}
