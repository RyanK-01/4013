import { MdCheck, MdClose } from 'react-icons/md';

/**
 * Side-by-side Approve / Reject action buttons for admin moderation workflows.
 * @param {Function} onApprove - Callback when the approve button is clicked
 * @param {Function} onReject - Callback when the reject button is clicked
 */
export default function ApproveRejectButtons({ onApprove, onReject }) {
  return (
    <div className="flex gap-2">
      <button
        onClick={onApprove}
        className="flex-1 bg-green-500 text-white py-2 rounded-lg text-sm font-medium flex items-center justify-center gap-1 hover:bg-green-600 transition"
      >
        <MdCheck /> Approve
      </button>
      <button
        onClick={onReject}
        className="flex-1 bg-red-100 text-red-600 py-2 rounded-lg text-sm font-medium flex items-center justify-center gap-1 hover:bg-red-200 transition"
      >
        <MdClose /> Reject
      </button>
    </div>
  );
}
