# Code Archaeology Explorer - Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    http://localhost:3000                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP Requests
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ App.jsx                                                   │  │
│  │  - Input form (URL/path)                                 │  │
│  │  - Loading states                                        │  │
│  │  - Museum navigation                                     │  │
│  │  - Exhibit components                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ App.css - Museum Theme                                    │  │
│  │  - Gradient backgrounds                                   │  │
│  │  - Card-based layouts                                     │  │
│  │  - Animations & transitions                               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ POST /api/analyze
                              │ {repo_url or repo_path}
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND API (Flask)                         │
│                    http://localhost:5000                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ app.py - REST API                                         │  │
│  │  - /api/health                                            │  │
│  │  - /api/analyze (main endpoint)                           │  │
│  │  - /api/cleanup                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
           │                               │
           │                               │
           ▼                               ▼
┌──────────────────────┐      ┌──────────────────────────┐
│  git_analyzer.py     │      │  story_generator.py      │
│                      │      │                          │
│  GitArchaeologist    │      │  StoryGenerator          │
│  ├─ find_dead_code() │      │  ├─ generate_story()     │
│  ├─ find_commented() │      │  ├─ format_artifacts()   │
│  ├─ find_todos()     │      │  └─ create_narratives()  │
│  ├─ find_oldest()    │      │                          │
│  ├─ get_timeline()   │      └──────────┬───────────────┘
│  └─ get_hall_shame() │                 │
└──────────┬───────────┘                 │
           │                             │
           │                             │ API Call
           ▼                             ▼
┌──────────────────────┐      ┌─────────────────────────┐
│  GitPython Library   │      │  Anthropic Claude API   │
│                      │      │                         │
│  - Repo()            │      │  Model:                 │
│  - iter_commits()    │      │  claude-3-5-sonnet      │
│  - stats             │      │                         │
│  - tree.traverse()   │      │  Generates:             │
└──────────┬───────────┘      │  - Narratives           │
           │                  │  - Summaries            │
           │                  │  - Descriptions         │
           ▼                  └─────────────────────────┘
┌──────────────────────┐
│  Git Repository      │
│                      │
│  Local path or       │
│  Cloned from GitHub  │
│                      │
│  Analyzes:           │
│  - .git history      │
│  - Source files      │
│  - Commits           │
│  - File structure    │
└──────────────────────┘
```

## Data Flow

### Analysis Request Flow

```
1. User Input
   │
   └─→ Repository URL or Local Path
       │
       ├─→ [If URL] Clone repository (shallow, depth=1)
       │
       └─→ [If Local] Use existing path
           │
           ▼
2. GitArchaeologist.excavate()
   │
   ├─→ find_dead_code()
   │   └─→ Parse AST, find unused functions
   │
   ├─→ find_commented_code()
   │   └─→ Scan for # or // with code patterns
   │
   ├─→ find_todos()
   │   └─→ Search for TODO/FIXME/HACK/XXX
   │
   ├─→ find_oldest_code()
   │   └─→ Get first commit, check surviving files
   │
   ├─→ get_hall_of_shame()
   │   └─→ Find functions > 30 lines
   │
   └─→ get_repository_timeline()
       └─→ Sample commits throughout history
       │
       ▼
3. Artifacts Collected
   │
   └─→ {
         dead_code: [...],
         commented_code: [...],
         todos: [...],
         oldest_code: [...],
         hall_of_shame: [...],
         timeline: [...]
       }
       │
       ▼
4. StoryGenerator.generate_stories()
   │
   ├─→ Format artifacts for prompts
   │
   ├─→ Call Claude API for each category
   │   │
   │   └─→ Anthropic Messages API
   │       └─→ claude-3-5-sonnet-20241022
   │
   └─→ Collect AI-generated narratives
       │
       ▼
5. Response
   │
   └─→ {
         artifacts: { ... },
         stories: { ... },
         metadata: { ... }
       }
       │
       ▼
6. Frontend Display
   │
   ├─→ Summary exhibit (overview + stats)
   │
   ├─→ Dead Code exhibit
   │
   ├─→ Fossilized Code exhibit
   │
   ├─→ TODOs exhibit
   │
   ├─→ Ancient Code exhibit
   │
   ├─→ Hall of Shame exhibit
   │
   ├─→ Heatmap exhibit
   │
   └─→ Timeline exhibit
```

## Component Breakdown

### Backend Components

#### `app.py` - Flask Application
**Purpose:** REST API server
**Endpoints:**
- `GET /api/health` - Health check
- `POST /api/analyze` - Main analysis endpoint
- `POST /api/cleanup` - Clean temporary repos

**Key Functions:**
- Request validation
- Repository cloning
- Orchestrating analysis
- Error handling

#### `git_analyzer.py` - GitArchaeologist Class
**Purpose:** Extract artifacts from repositories
**Methods:**
- `find_dead_code()` - Detect unused functions
- `find_commented_code()` - Find commented snippets
- `find_todos()` - Scan for TODO comments
- `find_oldest_code()` - Identify ancient files
- `get_hall_of_shame()` - Find complex functions
- `get_repository_timeline()` - Generate history
- `excavate()` - Run all analyses

**Technologies:**
- `git.Repo` - Git operations
- `ast` - Python AST parsing
- `os.walk` - File traversal
- `re` - Pattern matching

#### `story_generator.py` - StoryGenerator Class
**Purpose:** Generate AI narratives
**Methods:**
- `generate_artifact_story()` - Story per category
- `generate_excavation_summary()` - Overall summary
- `_format_*()` - Format data for prompts

**Technologies:**
- `anthropic.Anthropic` - Claude API client
- Prompt engineering
- Response parsing

### Frontend Components

#### `App.jsx` - Main Application
**Purpose:** User interface and state management
**Key Sections:**
- Input form (URL/path toggle)
- Loading animation
- Museum navigation
- Exhibit rendering
- Error handling

**State Management:**
- `repoInput` - User input
- `isLocal` - Path vs URL toggle
- `loading` - Analysis in progress
- `results` - Analysis results
- `error` - Error messages
- `activeExhibit` - Current exhibit

#### `App.css` - Styling
**Purpose:** Museum-themed visual design
**Key Styles:**
- Gradient backgrounds
- Glass-morphism effects
- Card-based layouts
- Hover animations
- Responsive breakpoints

## Technology Stack

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.8+ | Programming language |
| Flask | Web framework |
| GitPython | Git operations |
| Anthropic SDK | Claude API |
| python-dotenv | Environment variables |

### Frontend
| Technology | Purpose |
|------------|---------|
| React 18 | UI framework |
| Vite | Build tool |
| Modern CSS | Styling |

### External Services
| Service | Purpose |
|---------|---------|
| Claude API | AI narrative generation |
| Git | Version control analysis |

## Security Considerations

### API Key Management
- Stored in `.env` file (not committed)
- Loaded via `python-dotenv`
- Never exposed to frontend

### Repository Access
- Read-only operations
- Temporary clones deleted
- No write operations

### Input Validation
- Path existence checks
- Git repository validation
- URL format validation

### CORS Configuration
- Flask-CORS enabled
- Localhost-only in development

## Performance Optimizations

### Backend
- Shallow git clones (`depth=1`)
- Limit artifact results (top 10-20)
- File type filtering
- Early returns on errors

### Frontend
- Lazy rendering of exhibits
- Conditional component mounting
- Optimized CSS animations
- Client-side caching

### AI Integration
- Batch similar requests
- Limit token usage in prompts
- Summary-only, not full code
- Error fallbacks

## Scalability Considerations

### Current Limitations
- Synchronous processing
- Single-threaded analysis
- Memory-bound for large repos

### Future Improvements
- Async/background jobs
- Result caching
- Database for history
- Distributed processing
- Rate limiting
- Authentication

## Development Workflow

```
Developer
   │
   ├─→ Edit backend code
   │   └─→ Flask auto-reloads
   │
   ├─→ Edit frontend code
   │   └─→ Vite HMR (hot reload)
   │
   └─→ Test
       ├─→ python test_analyzer.py
       ├─→ Manual testing via UI
       └─→ Check Claude responses
```

## Deployment Architecture (Future)

```
┌─────────────────────┐
│  Vercel/Netlify     │ ← Frontend (Static)
│  (React Build)      │
└──────────┬──────────┘
           │
           │ API Calls
           ▼
┌─────────────────────┐
│  Heroku/Railway     │ ← Backend (Flask)
│  (Python Server)    │
└──────────┬──────────┘
           │
           ├─→ Claude API
           │
           └─→ GitHub (for cloning)
```

## File Structure

```
code-archaeology-explorer/
├── backend/
│   ├── app.py                 # Flask API
│   ├── git_analyzer.py        # Analysis logic
│   ├── story_generator.py     # AI integration
│   ├── test_analyzer.py       # Testing
│   ├── requirements.txt       # Dependencies
│   ├── .env                   # API keys
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main component
│   │   ├── App.css           # Styles
│   │   ├── main.jsx          # Entry point
│   │   └── index.css         # Global styles
│   ├── index.html            # HTML template
│   ├── package.json          # Dependencies
│   ├── vite.config.js        # Build config
│   └── .gitignore
│
├── README.md                 # Project overview
├── QUICKSTART.md            # Setup guide
├── DEMO_GUIDE.md            # Presentation tips
├── PROJECT_OVERVIEW.md      # Technical details
├── ARCHITECTURE.md          # This file
├── FINAL_CHECKLIST.md       # Pre-demo checklist
├── start.bat                # Windows launcher
└── start.sh                 # Unix launcher
```

---

This architecture provides a clean separation of concerns, scalability potential, and an engaging user experience powered by AI storytelling.
