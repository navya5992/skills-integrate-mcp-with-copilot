#!/usr/bin/env python3
"""
Launcher for Daily To-Do List Desktop Application
"""

import sys
import os
from pathlib import Path

# Add src directory to path so we can import modules
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def main():
    try:
        from todo_desktop_app import main
        main()
    except ImportError as e:
        print(f"Error importing application: {e}")
        print("Make sure you're running this from the project root directory.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()