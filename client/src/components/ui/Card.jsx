/**
 * Generic content container with rounded corners, shadow, and border.
 * @param {React.ReactNode} children - Card content
 * @param {string} [className] - Additional CSS classes
 * @param {object} props - Remaining HTML div attributes
 */
export default function Card({ children, className = '', ...props }) {
  return (
    <div className={`bg-white rounded-xl p-4 shadow-sm border ${className}`} {...props}>
      {children}
    </div>
  );
}
