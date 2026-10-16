/**
 * Reusable text input with integrated label styling.
 * @param {string} [label] - Label text displayed above the input
 * @param {string} [className] - Additional CSS classes
 * @param {object} props - Standard HTML input attributes (type, value, onChange, etc.)
 */
export function FormInput({ label, className = '', ...props }) {
  return (
    <div>
      {label && <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>}
      <input
        className={`w-full border rounded-lg px-3 py-2.5 text-sm focus:ring-2 focus:ring-orange-500 focus:border-orange-500 outline-none ${className}`}
        {...props}
      />
    </div>
  );
}

/**
 * Reusable textarea with integrated label styling.
 * @param {string} [label] - Label text displayed above the textarea
 * @param {string} [className] - Additional CSS classes
 * @param {object} props - Standard HTML textarea attributes (rows, value, onChange, etc.)
 */
export function FormTextarea({ label, className = '', ...props }) {
  return (
    <div>
      {label && <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>}
      <textarea
        className={`w-full border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-orange-500 focus:border-orange-500 outline-none ${className}`}
        {...props}
      />
    </div>
  );
}
