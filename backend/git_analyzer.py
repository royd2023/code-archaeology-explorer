import os
import re
from datetime import datetime
from git import Repo
from collections import defaultdict
import ast


class GitArchaeologist:
    """Analyzes git repositories to find code artifacts and fossils."""

    def __init__(self, repo_path):
        self.repo = Repo(repo_path)
        self.repo_path = repo_path

    def find_dead_code(self):
        """Find functions/classes that are defined but never called."""
        dead_code = []

        # For simplicity, we'll look at Python files
        for root, dirs, files in os.walk(self.repo_path):
            # Skip .git directory
            if '.git' in root:
                continue

            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()

                        # Find function and class definitions
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                func_name = node.name
                                # Simple heuristic: if function name appears only once, might be dead
                                if content.count(func_name) == 1 and not func_name.startswith('_'):
                                    dead_code.append({
                                        'type': 'function',
                                        'name': func_name,
                                        'file': file_path.replace(self.repo_path, '').replace('\\', '/'),
                                        'line': node.lineno
                                    })
                    except:
                        pass

        return dead_code[:10]  # Return top 10

    def find_commented_code(self):
        """Find commented-out code that's been there for a while."""
        commented_fossils = []

        for root, dirs, files in os.walk(self.repo_path):
            if '.git' in root:
                continue

            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()

                        # Look for lines with commented code (heuristic: contains =, (, {, etc.)
                        for i, line in enumerate(lines, 1):
                            stripped = line.strip()
                            if stripped.startswith('#') or stripped.startswith('//'):
                                # Check if it looks like code (has =, (, etc.)
                                if any(char in stripped for char in ['=', '(', '{', 'def ', 'function ', 'class ']):
                                    commented_fossils.append({
                                        'file': file_path.replace(self.repo_path, '').replace('\\', '/'),
                                        'line': i,
                                        'code': stripped[:100]  # Truncate long lines
                                    })
                    except:
                        pass

        return commented_fossils[:15]  # Return top 15

    def find_todos(self):
        """Find TODO comments throughout the codebase."""
        todos = []

        for root, dirs, files in os.walk(self.repo_path):
            if '.git' in root:
                continue

            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()

                        for i, line in enumerate(lines, 1):
                            if re.search(r'TODO|FIXME|HACK|XXX', line, re.IGNORECASE):
                                todos.append({
                                    'file': file_path.replace(self.repo_path, '').replace('\\', '/'),
                                    'line': i,
                                    'text': line.strip()[:150]
                                })
                    except:
                        pass

        return todos[:20]  # Return top 20

    def find_oldest_code(self):
        """Find the oldest lines of code still in the repository."""
        oldest_files = []

        try:
            # Get all commits
            commits = list(self.repo.iter_commits())
            if not commits:
                return []

            # Get files from the first commit
            first_commit = commits[-1]

            for item in first_commit.tree.traverse():
                if item.type == 'blob':
                    # Check if this file still exists
                    file_path = item.path
                    full_path = os.path.join(self.repo_path, file_path)

                    if os.path.exists(full_path):
                        oldest_files.append({
                            'file': file_path,
                            'first_commit_date': datetime.fromtimestamp(first_commit.committed_date).strftime('%Y-%m-%d'),
                            'first_commit_message': first_commit.message.strip()[:100],
                            'age_days': (datetime.now() - datetime.fromtimestamp(first_commit.committed_date)).days
                        })

            # Sort by age
            oldest_files.sort(key=lambda x: x['age_days'], reverse=True)
            return oldest_files[:10]
        except:
            return []

    def get_repository_timeline(self):
        """Get a timeline of major events in the repository."""
        timeline = []

        try:
            commits = list(self.repo.iter_commits())

            # Sample commits throughout history
            step = max(len(commits) // 20, 1)  # Get ~20 samples

            for commit in commits[::step]:
                timeline.append({
                    'date': datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d'),
                    'message': commit.message.strip()[:100],
                    'author': commit.author.name,
                    'files_changed': len(commit.stats.files)
                })

            return timeline
        except:
            return []

    def get_hall_of_shame(self):
        """Find the most complex/longest functions."""
        hall_of_shame = []

        for root, dirs, files in os.walk(self.repo_path):
            if '.git' in root:
                continue

            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            lines = content.split('\n')

                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                # Calculate function length
                                func_start = node.lineno
                                func_end = node.end_lineno if hasattr(node, 'end_lineno') else func_start
                                length = func_end - func_start

                                if length > 30:  # Functions longer than 30 lines
                                    hall_of_shame.append({
                                        'type': 'long_function',
                                        'name': node.name,
                                        'file': file_path.replace(self.repo_path, '').replace('\\', '/'),
                                        'line': node.lineno,
                                        'length': length
                                    })
                    except:
                        pass

        # Sort by length
        hall_of_shame.sort(key=lambda x: x['length'], reverse=True)
        return hall_of_shame[:10]

    def excavate(self):
        """Run full archaeological dig and return all artifacts."""
        print("Starting archaeological excavation...")

        artifacts = {
            'dead_code': self.find_dead_code(),
            'commented_code': self.find_commented_code(),
            'todos': self.find_todos(),
            'oldest_code': self.find_oldest_code(),
            'timeline': self.get_repository_timeline(),
            'hall_of_shame': self.get_hall_of_shame()
        }

        print(f"Excavation complete! Found {sum(len(v) if isinstance(v, list) else 0 for v in artifacts.values())} artifacts")

        return artifacts
