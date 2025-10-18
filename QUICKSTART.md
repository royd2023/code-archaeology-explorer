# Quick Start Guide

Get the Code Archaeology Explorer running in minutes!

## Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## Setup Steps

### 1. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Start the Backend (Terminal 1)

```bash
cd backend
python app.py
```

The API will start at `http://localhost:5000`

### Start the Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

The web app will start at `http://localhost:5173`

## Usage

1. Open `http://localhost:5173` in your browser
2. Choose between:
   - **GitHub URL**: Enter a public GitHub repo URL (e.g., `https://github.com/user/repo`)
   - **Local Path**: Enter an absolute path to a local git repository
3. Click "Start Excavation"
4. Wait for the analysis to complete (may take 1-2 minutes)
5. Explore the museum exhibits:
   - **Summary**: Overview of all findings
   - **Dead Code**: Unused functions and classes
   - **Fossils**: Commented-out code
   - **TODOs**: Unfulfilled promises
   - **Ancient Code**: Oldest surviving files
   - **Hall of Shame**: Most complex functions
   - **Timeline**: Repository history

## Demo Tips

For your hackathon demo:

1. **Pre-analyze repos**: Run analysis on 2-3 interesting repos beforehand so you have results ready to show
2. **Good demo repos**:
   - Your own projects (relatable)
   - Small-medium open source projects (manageable size)
   - Old repos with history (more interesting artifacts)
3. **Tell the story**: Walk through each exhibit and read Claude's generated narratives
4. **Show the comparison**: Compare a messy old repo vs. a clean new one

## Troubleshooting

**Backend won't start:**
- Make sure you activated the virtual environment
- Check that your ANTHROPIC_API_KEY is set in `.env`
- Verify Python 3.8+ with `python --version`

**Frontend won't start:**
- Delete `node_modules` and run `npm install` again
- Check Node.js version with `node --version` (need 16+)

**Analysis fails:**
- Ensure the path/URL is correct
- For local repos, use absolute paths (e.g., `C:\Users\...\repo` on Windows)
- Check that the directory is actually a git repository
- Some repos may be too large - try smaller ones first

**No API key:**
- Get one at https://console.anthropic.com/
- Make sure it's in the `.env` file as `ANTHROPIC_API_KEY=sk-ant-...`

## Performance Notes

- **First analysis**: Takes longer as dependencies load
- **Large repos**: May take 2-5 minutes to analyze
- **Shallow clones**: GitHub URLs are cloned with depth=1 for speed
- **Cleanup**: The backend cleans up temporary cloned repos on restart

Enjoy your excavation! 🏺
