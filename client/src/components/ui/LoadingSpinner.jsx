/**
 * Centered loading placeholder displayed while data is being fetched.
 * @param {string} [message='Loading...'] - Text shown to the user during loading
 */
export default function LoadingSpinner({ message = 'Loading...' }) {
  return (
    <div className="text-center py-12 text-gray-500">{message}</div>
  );
}
