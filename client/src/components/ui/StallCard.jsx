import { Link } from 'react-router-dom';
import { MdLocationOn } from 'react-icons/md';
import Badge from './Badge';
import { StarRatingBadge } from './StarRating';

/**
 * Linked card summarising a hawker stall (name, location, cuisine, price, rating).
 * Navigates to the stall detail page on click.
 * @param {object} stall - Stall data object (id, name, address, cuisine_type, price_range_*, google_rating, distance)
 * @param {React.ReactNode} [extra] - Optional extra content rendered inside the metadata row
 */
export default function StallCard({ stall, extra }) {
  return (
    <Link
      to={`/stall/${stall.id}`}
      className="block bg-white rounded-xl p-4 shadow-sm border hover:shadow-md transition"
    >
      <div className="flex justify-between items-start">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-base">{stall.name}</h3>
          <p className="text-sm text-gray-500 mt-0.5 flex items-center gap-1">
            <MdLocationOn className="text-gray-400 shrink-0" />
            <span className="truncate">{stall.address}</span>
          </p>
          <div className="flex items-center gap-3 mt-2 flex-wrap">
            {stall.cuisine_type && <Badge>{stall.cuisine_type}</Badge>}
            {stall.price_range_min != null && (
              <span className="text-xs text-gray-500">
                ${stall.price_range_min?.toFixed(2)} – ${stall.price_range_max?.toFixed(2)}
              </span>
            )}
            {stall.distance != null && (
              <span className="text-xs text-blue-600 font-medium">{stall.distance} km away</span>
            )}
            {extra}
          </div>
        </div>
        <StarRatingBadge rating={stall.google_rating} />
      </div>
    </Link>
  );
}
