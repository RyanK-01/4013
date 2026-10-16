const COLORS = {
  orange: 'bg-orange-100 text-orange-700',
  green: 'bg-green-100 text-green-700',
  blue: 'bg-blue-100 text-blue-700',
  red: 'bg-red-100 text-red-700',
  yellow: 'bg-yellow-100 text-yellow-700',
  purple: 'bg-purple-100 text-purple-700',
  gray: 'bg-gray-100 text-gray-600',
};

/**
 * Coloured pill badge for inline status or category labels.
 * @param {React.ReactNode} children - Badge text content
 * @param {'orange'|'green'|'blue'|'red'|'yellow'|'purple'|'gray'} [color='orange'] - Colour theme
 * @param {string} [className] - Additional CSS classes
 */
export default function Badge({ children, color = 'orange', className = '' }) {
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${COLORS[color] || COLORS.orange} ${className}`}>
      {children}
    </span>
  );
}
