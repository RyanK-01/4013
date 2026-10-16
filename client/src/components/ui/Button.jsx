/** @type {Record<string, string>} Tailwind class presets for each visual variant. */
const VARIANTS = {
  primary: 'bg-orange-500 text-white hover:bg-orange-600',
  secondary: 'bg-gray-100 text-gray-700 hover:bg-gray-200',
  danger: 'bg-red-500 text-white hover:bg-red-600',
  dangerLight: 'bg-red-100 text-red-600 hover:bg-red-200',
  success: 'bg-green-500 text-white hover:bg-green-600',
  blue: 'bg-blue-500 text-white hover:bg-blue-600',
  purple: 'bg-purple-500 text-white hover:bg-purple-600',
};

/**
 * Multi-variant button with built-in loading state.
 * @param {React.ReactNode} children - Button content
 * @param {'primary'|'secondary'|'danger'|'dangerLight'|'success'|'blue'|'purple'} [variant='primary'] - Visual style preset
 * @param {boolean} [loading=false] - Disables the button and shows loading text
 * @param {string} [loadingText] - Custom text shown while loading (defaults to "Loading...")
 * @param {boolean} [fullWidth=false] - Stretch to fill container width
 * @param {string} [className] - Additional CSS classes
 * @param {object} props - Remaining HTML button attributes
 */
export default function Button({
  children,
  variant = 'primary',
  loading = false,
  loadingText,
  fullWidth = false,
  className = '',
  ...props
}) {
  return (
    <button
      disabled={loading || props.disabled}
      className={`font-semibold py-2.5 rounded-xl transition disabled:opacity-50 flex items-center justify-center gap-2 ${
        VARIANTS[variant] || VARIANTS.primary
      } ${fullWidth ? 'w-full' : ''} ${className}`}
      {...props}
    >
      {loading ? (loadingText || 'Loading...') : children}
    </button>
  );
}
