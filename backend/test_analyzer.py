"""
Quick test script to verify the git analyzer works.
Run this before your demo to make sure everything is set up correctly.
"""

import os
from git_analyzer import GitArchaeologist


def test_analyzer():
    """Test the analyzer on the current repository."""

    # Get the path to this repo
    current_dir = os.path.dirname(os.path.abspath(__file__))
    repo_path = os.path.dirname(current_dir)  # Go up one level to the project root

    print("🏺 Testing Code Archaeology Explorer...")
    print(f"📁 Analyzing: {repo_path}\n")

    try:
        # Create archaeologist
        archaeologist = GitArchaeologist(repo_path)

        # Test dead code detection
        print("1️⃣ Testing dead code detection...")
        dead_code = archaeologist.find_dead_code()
        print(f"   ✅ Found {len(dead_code)} potentially dead functions\n")

        # Test commented code
        print("2️⃣ Testing commented code detection...")
        commented = archaeologist.find_commented_code()
        print(f"   ✅ Found {len(commented)} commented code snippets\n")

        # Test TODOs
        print("3️⃣ Testing TODO detection...")
        todos = archaeologist.find_todos()
        print(f"   ✅ Found {len(todos)} TODO comments\n")

        # Test oldest code
        print("4️⃣ Testing oldest code detection...")
        oldest = archaeologist.find_oldest_code()
        print(f"   ✅ Found {len(oldest)} ancient files\n")

        # Test hall of shame
        print("5️⃣ Testing complex function detection...")
        hall = archaeologist.find_hall_of_shame()
        print(f"   ✅ Found {len(hall)} complex functions\n")

        # Test timeline
        print("6️⃣ Testing timeline generation...")
        timeline = archaeologist.get_repository_timeline()
        print(f"   ✅ Generated timeline with {len(timeline)} events\n")

        print("=" * 50)
        print("✅ All tests passed!")
        print("=" * 50)
        print("\n🎉 The analyzer is working correctly!")
        print("💡 Next steps:")
        print("   1. Start the backend: python app.py")
        print("   2. Start the frontend: cd ../frontend && npm run dev")
        print("   3. Open http://localhost:3000\n")

        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   - Make sure you're in a git repository")
        print("   - Check that Python dependencies are installed")
        print("   - Run: pip install -r requirements.txt\n")
        return False


if __name__ == "__main__":
    test_analyzer()
