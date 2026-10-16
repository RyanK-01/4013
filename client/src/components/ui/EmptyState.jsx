import { Link } from 'react-router-dom';

/**
 * Placeholder shown when a list or view has no content.
 * Optionally includes a call-to-action link.
 * @param {React.ComponentType} [icon] - Icon component rendered above the title
 * @param {string} title - Primary empty-state message
 * @param {string} [subtitle] - Secondary descriptive text
 * @param {string} [actionLabel] - Text for the optional CTA link
 * @param {string} [actionTo] - Route path for the optional CTA link
 */
export default function EmptyState({ icon: Icon, title, subtitle, actionLabel, actionTo }) {
  return (
    <div className="text-center py-12">
      {Icon && <Icon className="text-4xl mx-auto mb-2 text-gray-300" />}
      <p className="text-gray-500 text-lg mb-2">{title}</p>
      {subtitle && <p className="text-gray-400 text-sm">{subtitle}</p>}
      {actionLabel && actionTo && (
        <Link to={actionTo} className="text-orange-500 hover:underline text-sm mt-2 inline-block">
          {actionLabel}
        </Link>
      )}
    </div>
  );
}
