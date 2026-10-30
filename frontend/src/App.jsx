import React, { useState } from 'react'
import { fetchRecommendations } from './lib/api'

export default function App() {
  const [query, setQuery] = useState('movies like inception but more emotional')
  const [topK, setTopK] = useState(5)
  const [yearMin, setYearMin] = useState('')
  const [yearMax, setYearMax] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleRun() {
    setError('')
    setLoading(true)
    try {
      const data = await fetchRecommendations({
        query,
        top_k: Number(topK),
        year_min: yearMin ? Number(yearMin) : null,
        year_max: yearMax ? Number(yearMax) : null,
      })
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ maxWidth: 860, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>MovieMuse Recommender</h1>
      <p>Semantic movie recommendations with query parsing, scoring, filtering, and explainable reasons.</p>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        rows={4}
        style={{ width: '100%' }}
        placeholder="Describe what kind of movie you want..."
      />
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.5rem', marginTop: '0.75rem' }}>
        <input type="number" value={topK} onChange={(e) => setTopK(e.target.value)} min={1} max={10} placeholder="Top K" />
        <input type="number" value={yearMin} onChange={(e) => setYearMin(e.target.value)} placeholder="Year min" />
        <input type="number" value={yearMax} onChange={(e) => setYearMax(e.target.value)} placeholder="Year max" />
      </div>
      <button onClick={handleRun} style={{ marginTop: '1rem' }} disabled={loading}>{loading ? 'Ranking...' : 'Get Recommendations'}</button>
      {error ? <pre style={{ color: 'crimson' }}>{error}</pre> : null}
      {result ? (
        <section style={{ marginTop: '1rem' }}>
          <h3>Top {result.top_k} picks</h3>
          {result.recommendations.map((movie) => (
            <article key={movie.title} style={{ border: '1px solid #ddd', borderRadius: 8, padding: '0.75rem', marginBottom: '0.75rem' }}>
              <strong>{movie.title}</strong> ({movie.year})
              <p style={{ margin: '0.35rem 0' }}>Genres: {movie.genres.join(', ')}</p>
              <p style={{ margin: '0.35rem 0' }}>Score: {movie.score}</p>
              <p style={{ margin: '0.35rem 0' }}>Why: {movie.reason}</p>
            </article>
          ))}
        </section>
      ) : null}
    </main>
  )
}
