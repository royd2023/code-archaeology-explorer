import anthropic
import os
from dotenv import load_dotenv

load_dotenv()


class StoryGenerator:
    """Uses Claude to generate entertaining narratives about code artifacts."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    def generate_artifact_story(self, artifact_type, artifacts):
        """Generate a story for a specific type of artifact."""

        if not artifacts:
            return "No artifacts found in this category."

        # Create the prompt for the specific artifact type
        if artifact_type == 'dead_code':
            prompt = f"""You are a humorous code archaeologist. Analyze these potentially unused functions and write a short, entertaining narrative about them (2-3 sentences per item). Make it funny but informative.

Dead/Unused Functions Found:
{self._format_dead_code(artifacts)}

Write a brief story about these forgotten functions. Use phrases like "last seen", "abandoned", "lonely function", etc. Keep it light and entertaining."""

        elif artifact_type == 'commented_code':
            prompt = f"""You are a code archaeologist examining fossilized code. These are commented-out code snippets found in the codebase. Write a short, funny narrative (2-3 sentences total) about why developers might have left these commented remnants behind.

Commented Code Fossils:
{self._format_commented_code(artifacts)}

Make it entertaining and relatable to developers."""

        elif artifact_type == 'todos':
            prompt = f"""You are a code archaeologist examining ancient TODO comments. Write a humorous narrative (2-3 sentences total) about these unfulfilled promises.

TODO Comments Found:
{self._format_todos(artifacts)}

Be witty about procrastination and abandoned intentions."""

        elif artifact_type == 'oldest_code':
            prompt = f"""You are a code archaeologist examining the oldest surviving code. Write an epic, reverent narrative (3-4 sentences) about these ancient relics that have survived since the beginning.

Oldest Code Still Alive:
{self._format_oldest_code(artifacts)}

Make it sound like discovering ancient ruins."""

        elif artifact_type == 'hall_of_shame':
            prompt = f"""You are a code archaeologist examining monstrous functions. Write a dramatic, funny narrative (2-3 sentences) about these behemoths.

Longest/Most Complex Functions:
{self._format_hall_of_shame(artifacts)}

Be dramatic and entertaining about their size and complexity."""

        else:
            prompt = "Describe these code artifacts."

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return message.content[0].text
        except Exception as e:
            print(f"Error generating story: {e}")
            return f"The ancient texts are too weathered to read... ({str(e)})"

    def generate_excavation_summary(self, artifacts):
        """Generate an overall summary of the excavation."""

        summary_prompt = f"""You are a code archaeologist presenting your findings. Write an engaging 3-4 sentence summary of this code excavation, highlighting the most interesting discoveries.

Excavation Summary:
- Dead/Unused Functions: {len(artifacts.get('dead_code', []))} found
- Commented Code Fossils: {len(artifacts.get('commented_code', []))} found
- Unfulfilled TODOs: {len(artifacts.get('todos', []))} found
- Ancient Code (oldest files): {len(artifacts.get('oldest_code', []))} found
- Hall of Shame (complex functions): {len(artifacts.get('hall_of_shame', []))} found
- Timeline Events: {len(artifacts.get('timeline', []))} sampled

Write an exciting opening to the museum exhibit. Make it sound like an archaeological discovery."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=300,
                messages=[
                    {"role": "user", "content": summary_prompt}
                ]
            )

            return message.content[0].text
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Welcome to the Code Archaeology Museum. Explore the artifacts of code past..."

    def _format_dead_code(self, artifacts):
        """Format dead code for the prompt."""
        lines = []
        for item in artifacts[:5]:  # Limit to 5 items for token efficiency
            lines.append(f"- Function '{item['name']}' in {item['file']} (line {item['line']})")
        return '\n'.join(lines)

    def _format_commented_code(self, artifacts):
        """Format commented code for the prompt."""
        lines = []
        for item in artifacts[:5]:
            lines.append(f"- {item['file']}: {item['code'][:80]}")
        return '\n'.join(lines)

    def _format_todos(self, artifacts):
        """Format TODOs for the prompt."""
        lines = []
        for item in artifacts[:5]:
            lines.append(f"- {item['text'][:100]}")
        return '\n'.join(lines)

    def _format_oldest_code(self, artifacts):
        """Format oldest code for the prompt."""
        lines = []
        for item in artifacts[:5]:
            lines.append(f"- {item['file']} (from {item['first_commit_date']}, {item['age_days']} days old)")
        return '\n'.join(lines)

    def _format_hall_of_shame(self, artifacts):
        """Format hall of shame for the prompt."""
        lines = []
        for item in artifacts[:5]:
            lines.append(f"- Function '{item['name']}' in {item['file']} ({item['length']} lines long)")
        return '\n'.join(lines)
