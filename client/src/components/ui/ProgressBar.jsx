/**
 * Colour-coded progress bar used to visualise crowd levels.
 * Colour shifts from green → yellow → orange → red as value increases.
 * @param {number} value - Percentage value (0–100)
 * @param {string} [height='h-3'] - Tailwind height class for the bar
 * @param {boolean} [showLabel=false] - Display a "Crowd Level" label with the percentage
 */
export default function ProgressBar({ value, height = 'h-3', showLabel = false }) {
  const color =
    value < 30 ? 'bg-green-500' :
    value < 60 ? 'bg-yellow-500' :
    value < 80 ? 'bg-orange-500' : 'bg-red-500';

  return (
    <div>
      {showLabel && (
        <div className="flex items-center justify-between text-sm mb-1">
          <span className="text-gray-600">Crowd Level</span>
          <span className="font-medium">{value}%</span>
        </div>
      )}
      <div className={`w-full bg-gray-200 rounded-full ${height} overflow-hidden`}>
        <div
          className={`${height} rounded-full transition-all ${color}`}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}
