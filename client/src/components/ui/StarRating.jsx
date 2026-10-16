import { MdStar, MdStarBorder } from 'react-icons/md';

/**
 * Read-only star rating badge displaying a numeric score with an optional review count.
 * @param {number} rating - Numeric rating value (e.g. 4.5)
 * @param {number} [count] - Number of reviews (shown in parentheses)
 */
export function StarRatingBadge({ rating, count }) {
  if (!rating) return null;
  return (
    <div className="flex items-center gap-1 bg-yellow-50 px-2 py-1 rounded-lg">
      <MdStar className="text-yellow-500" />
      <span className="text-sm font-semibold">{rating}</span>
      {count != null && <span className="text-xs text-gray-400">({count})</span>}
    </div>
  );
}

/**
 * Interactive 1–5 star picker for submitting ratings.
 * @param {number} value - Currently selected star count (1–5)
 * @param {Function} onChange - Callback invoked with the new star value on click
 * @param {string} [size='text-3xl'] - Tailwind text-size class controlling star icon size
 */
export function StarRatingInput({ value, onChange, size = 'text-3xl' }) {
  return (
    <div className="flex gap-1">
      {[1, 2, 3, 4, 5].map((star) => (
        <button type="button" key={star} onClick={() => onChange(star)}>
          {star <= value
            ? <MdStar className={`${size} text-yellow-500`} />
            : <MdStarBorder className={`${size} text-gray-300`} />}
        </button>
      ))}
    </div>
  );
}
