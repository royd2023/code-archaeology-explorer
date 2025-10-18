# Hackathon Demo Guide

## Pre-Demo Checklist

### Before the Presentation:

1. **Test Everything**
   - Run backend: `cd backend && python app.py`
   - Run frontend: `cd frontend && npm run dev`
   - Test with a small repo to ensure everything works

2. **Prepare Demo Repositories**
   - Pick 2-3 interesting repos (mix of your own and open source)
   - Pre-analyze them and take screenshots
   - Have URLs/paths ready to copy-paste

3. **Browser Setup**
   - Open `http://localhost:3000` in a clean browser window
   - Close unnecessary tabs
   - Zoom in so audience can see (125-150%)

4. **Backup Plan**
   - Have screenshots of pre-run analyses
   - Record a backup video of the demo working

## The Pitch (2 minutes)

**Hook:** "Have you ever inherited a codebase and wondered what secrets are hiding in there?"

**Problem:**
- Dead code cluttering repositories
- Forgotten TODOs and technical debt
- No fun way to understand code history
- Code reviews are boring and tedious

**Solution:** "Code Archaeology Explorer turns code analysis into a museum experience!"

**Key Features:**
1. Automatically excavates git repositories
2. Finds "fossils" - dead code, commented code, ancient functions
3. Uses Claude AI to generate entertaining narratives
4. Beautiful museum-style interface

## Live Demo Flow (5-7 minutes)

### Step 1: The Setup (30 seconds)
"Let me show you how it works. I'll analyze [REPO NAME]..."

- Type in repo URL or path
- Click "Start Excavation"
- While it loads: "The tool is cloning the repo, analyzing the git history, scanning for artifacts, and having Claude AI write stories about what it finds"

### Step 2: The Excavation Summary (1 minute)
- "Look at what we uncovered!"
- Point out the numbers in the stat cards
- Read the AI-generated summary aloud (it's funny!)
- "Claude AI wrote this based on analyzing the actual code"

### Step 3: Tour the Exhibits (3-4 minutes)

**Dead Code Hall (1 min):**
- "These are functions that are defined but never called"
- Read Claude's narrative
- Pick one funny example: "This function has been sitting here, lonely and unused..."

**Fossilized Code (45 sec):**
- "Commented-out code that developers couldn't let go"
- Show a couple examples
- "We've all done this - 'just in case we need it later'"

**TODOs Hall (45 sec):**
- "The scroll of broken promises"
- Read Claude's witty take on procrastination
- Show some ancient TODOs

**Ancient Relics (1 min):**
- "Files that have survived since day one of the project"
- Show the oldest file and its age
- "This code is X days old - probably older than some relationships!"

**Hall of Shame (45 sec):**
- "The most complex, longest functions"
- "This 200-line monster has been terrorizing developers..."

**Timeline (optional, 30 sec):**
- Quickly scroll through to show the history

### Step 4: The Tech Stack (1 minute)

"How does it work?"

**Backend:**
- Python + Flask API
- GitPython for repository analysis
- Anthropic Claude API for storytelling

**Frontend:**
- React + Vite
- Clean, museum-themed UI

**Key Innovation:**
- Static analysis finds artifacts
- Claude AI generates contextual, humorous narratives
- Makes code analysis entertaining!

### Step 5: Use Cases (30 seconds)

"This is useful for..."
- Onboarding to new codebases
- Finding technical debt
- Code cleanup sprints
- Teaching code quality
- Making code reviews fun!

## Demo Tips

### DO:
- **Be enthusiastic** about the AI-generated stories
- **Read the narratives aloud** - they're the star of the show
- **Pick repos with interesting findings** - old, messy repos are better than clean ones
- **Laugh at the funny parts** - the humor is intentional
- **Show the contrast** - "look how many TODOs!" vs "this repo is clean!"

### DON'T:
- Rush through the AI stories - they're what makes it unique
- Demo on a repo with zero findings (boring!)
- Get too technical about the code analysis
- Spend too much time on one exhibit
- Forget to mention Claude AI's role

## Good Demo Repositories

### Your Own Projects:
- Early hackathon projects (usually messy!)
- School assignments
- Old personal projects you've abandoned

### Open Source Suggestions:
- Small-medium repos (faster analysis)
- Projects with history (better timeline)
- Active projects (more TODOs)

**Test These:**
- Your own repos from GitHub
- Small Flask/React projects
- Any repo with 100-1000 commits

## Questions You Might Get

**Q: How accurate is the dead code detection?**
A: "It uses basic heuristics - single occurrence of function name. It's not perfect but gives a good signal of potential dead code worth investigating."

**Q: Does it work with languages other than Python?**
A: "The static analysis is more robust for Python, but it finds TODOs, commented code, and git history for any language. We could easily extend it!"

**Q: How long does analysis take?**
A: "Depends on repo size. Small repos: 30 seconds. Medium repos: 1-2 minutes. We clone shallow to speed it up."

**Q: Could this be integrated into CI/CD?**
A: "Absolutely! You could run it weekly and track technical debt over time. Flag when it gets too high."

**Q: What about privacy/security?**
A: "For private repos, it runs locally. The code stays on your machine - only artifact summaries go to Claude API for story generation."

## Backup Talking Points

If you have extra time or questions:

### Future Enhancements:
- Track technical debt trends over time
- Integrate with GitHub Issues
- Gamify cleanup (achievements for removing dead code)
- Team leaderboards
- More languages and frameworks
- Custom analysis rules

### Technical Challenges Solved:
- Parsing multiple languages
- Efficient git history analysis
- Balancing humor with usefulness in AI prompts
- Making the UI feel like a real museum

## The Close

"Code archaeology makes code analysis fun and engaging. Instead of dreading code reviews, you can explore your codebase like a museum. Thanks to Claude AI, every repository tells its own unique story!"

**Call to Action:**
- GitHub repo link (if you publish it)
- Try it on your own repos
- Contribution ideas welcome!

## Time Allocations

**2-Minute Lightning Demo:**
- Hook: 20s
- Quick demo: 1min
- Tech stack: 20s
- Close: 20s

**5-Minute Demo:**
- Pitch: 1min
- Full demo: 3min
- Q&A: 1min

**10-Minute Demo:**
- Pitch: 2min
- Demo: 5min
- Tech deep-dive: 2min
- Q&A: 1min

Good luck! 🏺🎉
