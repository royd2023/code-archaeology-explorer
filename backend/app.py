from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import shutil
import traceback
from git import Repo
from git_analyzer import GitArchaeologist
from story_generator import StoryGenerator

app = Flask(__name__)
CORS(app)

# Directory to store temporary cloned repos
TEMP_REPOS_DIR = os.path.join(os.path.dirname(__file__), 'temp_repos')
os.makedirs(TEMP_REPOS_DIR, exist_ok=True)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'Code Archaeology Explorer API is running'})


@app.route('/api/analyze', methods=['POST'])
def analyze_repository():
    """
    Analyze a git repository and return artifacts with AI-generated stories.

    Expected JSON body:
    {
        "repo_path": "/path/to/repo" OR "repo_url": "https://github.com/user/repo"
    }
    """
    temp_dir = None  # Track temp directory for cleanup

    try:
        data = request.json
        repo_path = data.get('repo_path')
        repo_url = data.get('repo_url')

        if not repo_path and not repo_url:
            return jsonify({'error': 'Either repo_path or repo_url is required'}), 400

        # If URL provided, clone it
        if repo_url:
            print(f"Cloning repository from {repo_url}...")
            # Create a unique temp directory for this repo
            temp_dir = tempfile.mkdtemp(dir=TEMP_REPOS_DIR)
            try:
                # Full clone to get history (needed for timeline/oldest code analysis)
                print("This may take a minute for large repositories...")
                Repo.clone_from(repo_url, temp_dir)
                repo_path = temp_dir
                print(f"Repository cloned to {temp_dir}")
            except Exception as e:
                shutil.rmtree(temp_dir, ignore_errors=True)
                return jsonify({'error': f'Failed to clone repository: {str(e)}'}), 400

        # Validate path exists
        if not os.path.exists(repo_path):
            return jsonify({'error': f'Repository path does not exist: {repo_path}'}), 400

        # Check if it's a git repository
        try:
            test_repo = Repo(repo_path)
        except Exception as e:
            return jsonify({'error': f'Not a valid git repository: {str(e)}'}), 400

        print(f"Starting excavation of {repo_path}...")

        # Run archaeological analysis
        archaeologist = GitArchaeologist(repo_path)
        artifacts = archaeologist.excavate()

        # Generate AI stories
        print("Generating AI narratives...")
        story_gen = StoryGenerator()

        # Generate stories for each artifact type
        stories = {
            'excavation_summary': story_gen.generate_excavation_summary(artifacts),
            'dead_code_story': story_gen.generate_artifact_story('dead_code', artifacts['dead_code']),
            'commented_code_story': story_gen.generate_artifact_story('commented_code', artifacts['commented_code']),
            'todos_story': story_gen.generate_artifact_story('todos', artifacts['todos']),
            'oldest_code_story': story_gen.generate_artifact_story('oldest_code', artifacts['oldest_code']),
            'hall_of_shame_story': story_gen.generate_artifact_story('hall_of_shame', artifacts['hall_of_shame']),
            'complexity_heatmap_story': story_gen.generate_artifact_story('complexity_heatmap', artifacts['complexity_heatmap'])
        }

        # Combine artifacts and stories
        result = {
            'artifacts': artifacts,
            'stories': stories,
            'metadata': {
                'repo_path': repo_path,
                'total_artifacts': sum(len(v) if isinstance(v, list) else 0 for v in artifacts.values())
            }
        }

        print("Analysis complete!")

        # Clean up temp directory if it was created
        if temp_dir and os.path.exists(temp_dir):
            print(f"Cleaning up temporary repository at {temp_dir}...")
            shutil.rmtree(temp_dir, ignore_errors=True)
            print("Cleanup complete!")

        return jsonify(result)

    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        traceback.print_exc()

        # Clean up temp directory even on error
        if temp_dir and os.path.exists(temp_dir):
            print(f"Cleaning up temporary repository at {temp_dir}...")
            shutil.rmtree(temp_dir, ignore_errors=True)

        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@app.route('/api/cleanup', methods=['POST'])
def cleanup_temp_repos():
    """Clean up temporary cloned repositories."""
    try:
        if os.path.exists(TEMP_REPOS_DIR):
            shutil.rmtree(TEMP_REPOS_DIR)
            os.makedirs(TEMP_REPOS_DIR)
        return jsonify({'message': 'Temporary repositories cleaned up'})
    except Exception as e:
        return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500


if __name__ == '__main__':
    print("Starting Code Archaeology Explorer API...")
    print("API running at http://localhost:5000")
    print("Ready to excavate repositories!")
    app.run(debug=True, port=5000)
