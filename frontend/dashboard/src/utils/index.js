/**
 * Shared utility functions
 */

/**
 * Format a date string to a readable format
 * @param {string|Date} date - The date to format
 * @returns {string} Formatted date string (e.g., "Jan 15")
 */
export function formatDate(date) {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

/**
 * Convert task status key to human-readable label
 * @param {string} status - Status key (todo, in_progress, done)
 * @returns {string} Human-readable label
 */
export function statusLabel(status) {
  const labels = {
    todo: 'To Do',
    in_progress: 'In Progress',
    done: 'Done'
  }
  return labels[status] || status
}
