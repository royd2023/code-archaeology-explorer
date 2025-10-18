import { useState } from 'react'
import './App.css'

function App() {
  const [repoInput, setRepoInput] = useState('')
  const [isLocal, setIsLocal] = useState(false)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [activeExhibit, setActiveExhibit] = useState('summary')
  const [slideDirection, setSlideDirection] = useState('right')

  const exhibits = ['summary', 'dead_code', 'commented_code', 'todos', 'oldest_code', 'hall_of_shame', 'timeline']

  const handleExhibitChange = (newExhibit) => {
    const currentIndex = exhibits.indexOf(activeExhibit)
    const newIndex = exhibits.indexOf(newExhibit)
    setSlideDirection(newIndex > currentIndex ? 'right' : 'left')
    setActiveExhibit(newExhibit)
  }

  const handleAnalyze = async () => {
    if (!repoInput.trim()) {
      setError('Please enter a repository path or URL')
      return
    }

    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const payload = isLocal
        ? { repo_path: repoInput }
        : { repo_url: repoInput }

      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Analysis failed')
      }

      const data = await response.json()
      setResults(data)
      setActiveExhibit('summary')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const renderExhibit = () => {
    if (!results) return null

    const { artifacts, stories } = results

    switch (activeExhibit) {
      case 'summary':
        return (
          <div className="exhibit">
            <h2>🏛️ Excavation Summary</h2>
            <div className="story-text">{stories.excavation_summary}</div>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-number">{artifacts.dead_code.length}</div>
                <div className="stat-label">Dead Functions</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{artifacts.commented_code.length}</div>
                <div className="stat-label">Code Fossils</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{artifacts.todos.length}</div>
                <div className="stat-label">Ancient TODOs</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{artifacts.oldest_code.length}</div>
                <div className="stat-label">Oldest Files</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{artifacts.hall_of_shame.length}</div>
                <div className="stat-label">Complex Beasts</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{artifacts.timeline.length}</div>
                <div className="stat-label">Timeline Events</div>
              </div>
            </div>
          </div>
        )

      case 'dead_code':
        return (
          <div className="exhibit">
            <h2>💀 The Graveyard: Dead Code</h2>
            <div className="story-text">{stories.dead_code_story}</div>
            <div className="artifacts-list">
              {artifacts.dead_code.map((item, idx) => (
                <div key={idx} className="artifact-card">
                  <div className="artifact-title">⚰️ {item.name}</div>
                  <div className="artifact-detail">📁 {item.file}:{item.line}</div>
                  <div className="artifact-tag">{item.type}</div>
                </div>
              ))}
              {artifacts.dead_code.length === 0 && (
                <div className="empty-state">No dead code found! This codebase is well-maintained.</div>
              )}
            </div>
          </div>
        )

      case 'commented_code':
        return (
          <div className="exhibit">
            <h2>🦴 Fossilized Code</h2>
            <div className="story-text">{stories.commented_code_story}</div>
            <div className="artifacts-list">
              {artifacts.commented_code.map((item, idx) => (
                <div key={idx} className="artifact-card">
                  <div className="artifact-detail">📁 {item.file}:{item.line}</div>
                  <code className="artifact-code">{item.code}</code>
                </div>
              ))}
              {artifacts.commented_code.length === 0 && (
                <div className="empty-state">No commented code fossils found!</div>
              )}
            </div>
          </div>
        )

      case 'todos':
        return (
          <div className="exhibit">
            <h2>📜 The Scroll of Broken Promises</h2>
            <div className="story-text">{stories.todos_story}</div>
            <div className="artifacts-list">
              {artifacts.todos.map((item, idx) => (
                <div key={idx} className="artifact-card">
                  <div className="artifact-detail">📁 {item.file}:{item.line}</div>
                  <div className="artifact-text">{item.text}</div>
                </div>
              ))}
              {artifacts.todos.length === 0 && (
                <div className="empty-state">No TODOs found! All promises kept.</div>
              )}
            </div>
          </div>
        )

      case 'oldest_code':
        return (
          <div className="exhibit">
            <h2>🏺 Ancient Relics</h2>
            <div className="story-text">{stories.oldest_code_story}</div>
            <div className="artifacts-list">
              {artifacts.oldest_code.map((item, idx) => (
                <div key={idx} className="artifact-card">
                  <div className="artifact-title">🗿 {item.file}</div>
                  <div className="artifact-detail">
                    📅 First seen: {item.first_commit_date} ({item.age_days} days ago)
                  </div>
                  <div className="artifact-text">"{item.first_commit_message}"</div>
                </div>
              ))}
              {artifacts.oldest_code.length === 0 && (
                <div className="empty-state">No ancient code found.</div>
              )}
            </div>
          </div>
        )

      case 'hall_of_shame':
        return (
          <div className="exhibit">
            <h2>🐉 Hall of Shame: Monstrous Functions</h2>
            <div className="story-text">{stories.hall_of_shame_story}</div>
            <div className="artifacts-list">
              {artifacts.hall_of_shame.map((item, idx) => (
                <div key={idx} className="artifact-card">
                  <div className="artifact-title">👹 {item.name}</div>
                  <div className="artifact-detail">📁 {item.file}:{item.line}</div>
                  <div className="artifact-badge">{item.length} lines of terror</div>
                </div>
              ))}
              {artifacts.hall_of_shame.length === 0 && (
                <div className="empty-state">No monstrous functions found! Clean code champion.</div>
              )}
            </div>
          </div>
        )

      case 'timeline':
        return (
          <div className="exhibit">
            <h2>📅 Archaeological Timeline</h2>
            <div className="timeline">
              {artifacts.timeline.map((event, idx) => (
                <div key={idx} className="timeline-event">
                  <div className="timeline-date">{event.date}</div>
                  <div className="timeline-content">
                    <div className="timeline-message">{event.message}</div>
                    <div className="timeline-meta">
                      👤 {event.author} · 📝 {event.files_changed} files changed
                    </div>
                  </div>
                </div>
              ))}
              {artifacts.timeline.length === 0 && (
                <div className="empty-state">No timeline data available.</div>
              )}
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🏺 Code Archaeology Explorer</h1>
        <p className="tagline">Uncover the fossils hidden in your codebase</p>
      </header>

      <div className="container">
        {!results && (
          <div className="input-section">
            <div className="toggle-group">
              <button
                className={`toggle-btn ${!isLocal ? 'active' : ''}`}
                onClick={() => setIsLocal(false)}
              >
                GitHub URL
              </button>
              <button
                className={`toggle-btn ${isLocal ? 'active' : ''}`}
                onClick={() => setIsLocal(true)}
              >
                Local Path
              </button>
            </div>

            <input
              type="text"
              className="repo-input"
              placeholder={
                isLocal
                  ? 'Enter local repository path (e.g., C:\\projects\\my-repo)'
                  : 'Enter GitHub URL (e.g., https://github.com/user/repo)'
              }
              value={repoInput}
              onChange={(e) => setRepoInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
            />

            <button
              className="analyze-btn"
              onClick={handleAnalyze}
              disabled={loading}
            >
              {loading ? '🔍 Excavating...' : '🏺 Start Excavation'}
            </button>

            {error && <div className="error-message">❌ {error}</div>}
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="loading-spinner"></div>
            <div className="loading-text">
              Digging through ancient code...
              <br />
              <small>This may take a minute for large repositories</small>
            </div>
          </div>
        )}

        {results && (
          <div className="museum">
            <div className="museum-nav">
              <button
                className={`nav-btn ${activeExhibit === 'summary' ? 'active' : ''}`}
                onClick={() => handleExhibitChange('summary')}
              >
                🏛️ Summary
              </button>
              <button
                className={`nav-btn ${activeExhibit === 'dead_code' ? 'active' : ''}`}
                onClick={() => handleExhibitChange('dead_code')}
              >
                💀 Dead Code
              </button>
              <button
                className={`nav-btn ${activeExhibit === 'commented_code' ? 'active' : ''}`}
                onClick={() => handleExhibitChange('commented_code')}
              >
                🦴 Fossils
              </button>
              <button
                className={`nav-btn ${activeExhibit === 'todos' ? 'active' : ''}`}
                onClick={() => handleExhibitChange('todos')}
              >
                📜 TODOs
              </button>
              <button
                className={`nav-btn ${activeExhibit === 'oldest_code' ? 'active' : ''}`}
                onClick={() => handleExhibitChange('oldest_code')}
              >
                🏺 Ancient Code
              </button>
              <button
                className={`nav-btn ${activeExhibit === 'hall_of_shame' ? 'active' : ''}`}
                onClick={() => handleExhibitChange('hall_of_shame')}
              >
                🐉 Hall of Shame
              </button>
              <button
                className={`nav-btn ${activeExhibit === 'timeline' ? 'active' : ''}`}
                onClick={() => handleExhibitChange('timeline')}
              >
                📅 Timeline
              </button>
            </div>

            <div className="museum-content">
              <div key={activeExhibit} className={`exhibit-wrapper slide-${slideDirection}`}>
                {renderExhibit()}
              </div>
            </div>

            <button
              className="new-excavation-btn"
              onClick={() => {
                setResults(null)
                setRepoInput('')
                setError(null)
              }}
            >
              🔄 New Excavation
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
