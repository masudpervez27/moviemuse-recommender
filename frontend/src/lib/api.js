const API = import.meta.env.VITE_API_URL || ''

const LOG_LEVELS = { debug: 10, info: 20, warn: 30, error: 40 }
const ACTIVE_LEVEL = LOG_LEVELS[(import.meta.env.VITE_LOG_LEVEL || (import.meta.env.DEV ? 'debug' : 'info')).toLowerCase()] || LOG_LEVELS.info

function log(level, message, context) {
  if ((LOG_LEVELS[level] || LOG_LEVELS.info) < ACTIVE_LEVEL) return
  const writer = console[level] || console.log
  if (context === undefined) writer('[MovieMuse Recommender] ' + message)
  else writer('[MovieMuse Recommender] ' + message, context)
}

export async function fetchRecommendations(payload) {
  log('info', 'Calling recommend endpoint')
  const response = await fetch(API + '/api/recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const text = await response.text()
    log('error', 'recommend endpoint failed', { status: response.status, body: text })
    throw new Error(text)
  }

  return response.json()
}
