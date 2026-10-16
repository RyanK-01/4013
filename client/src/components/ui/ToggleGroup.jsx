/**
 * Pill-button group for single or multi-select filtering.
 * Supports both string options and {label, value} objects.
 * @param {Array<string|{label: string, value: string}>} options - Selectable items
 * @param {string|string[]} value - Currently selected value(s)
 * @param {Function} onChange - Called with the updated selection on toggle
 * @param {boolean} [multiple=false] - Allow multiple concurrent selections
 * @param {string} [activeColor] - Tailwind classes for selected state
 * @param {string} [inactiveColor] - Tailwind classes for unselected state
 * @param {string} [className] - Additional CSS classes for the container
 */
export default function ToggleGroup({
  options,
  value,
  onChange,
  multiple = false,
  activeColor = 'bg-orange-500 text-white',
  inactiveColor = 'bg-gray-100 text-gray-700 hover:bg-gray-200',
  className = '',
}) {
  const isActive = (opt) =>
    multiple ? (value || []).includes(opt) : value === opt;

  const handleClick = (opt) => {
    if (multiple) {
      const arr = value || [];
      onChange(arr.includes(opt) ? arr.filter((x) => x !== opt) : [...arr, opt]);
    } else {
      onChange(value === opt ? null : opt);
    }
  };

  return (
    <div className={`flex flex-wrap gap-2 ${className}`}>
      {options.map((opt) => {
        const label = typeof opt === 'string' ? opt : opt.label;
        const key = typeof opt === 'string' ? opt : opt.value;
        return (
          <button
            type="button"
            key={key}
            onClick={() => handleClick(key)}
            className={`px-3 py-1.5 rounded-full text-sm font-medium transition ${
              isActive(key) ? activeColor : inactiveColor
            }`}
          >
            {label}
          </button>
        );
      })}
    </div>
  );
}
