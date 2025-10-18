# Code Archaeology Explorer

For Claude Builder Club @ OSU Challenge

An interactive tool that analyzes git repositories to uncover "fossils" - dead code, abandoned features, and forgotten TODOs - and presents them as a museum exhibit with AI-generated narratives.

## Features

- **Dig Site Analysis**: Excavate git history to find interesting artifacts
- **Museum Exhibits**: Categorized displays of code fossils
- **Story Generation**: Claude AI narrates the history of your codebase
- **Timeline Visualization**: See how your code evolved over time

## Setup
```bash
git clone https://github.com/royd2023/code-archaeology-explorer.git
```

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your ANTHROPIC_API_KEY
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Start the backend server
2. Start the frontend dev server
3. Enter a git repository path or URL
4. Explore your code archaeology findings!
