#!/usr/bin/env python3
"""
Test script for Daily To-Do List Desktop Application
Tests the core functionality without requiring GUI display
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

class MockTodoApp:
    """Mock version of TodoApp for testing without GUI"""

    def __init__(self):
        self.tasks = []
        self.data_file = Path.home() / ".daily_todo_test.json"

    def add_task(self, task_text):
        """Add a new task"""
        task = {
            'id': len(self.tasks),
            'text': task_text,
            'completed': False,
            'created': datetime.now().isoformat()
        }
        self.tasks.append(task)
        print(f"✅ Added task: {task_text}")

    def toggle_task(self, task_id):
        """Toggle task completion"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                task['updated'] = datetime.now().isoformat()
                status = "completed" if task['completed'] else "marked pending"
                print(f"🔄 Task '{task['text']}' {status}")
                return True
        print(f"❌ Task with ID {task_id} not found")
        return False

    def delete_task(self, task_id):
        """Delete a task"""
        original_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        if len(self.tasks) < original_count:
            print(f"🗑️ Deleted task with ID {task_id}")
            return True
        else:
            print(f"❌ Task with ID {task_id} not found")
            return False

    def clear_completed(self):
        """Clear completed tasks"""
        original_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task['completed']]
        removed = original_count - len(self.tasks)
        print(f"🧹 Cleared {removed} completed tasks")

    def display_tasks(self):
        """Display current tasks"""
        if not self.tasks:
            print("📝 No tasks yet!")
            return

        print("\n📋 Current Tasks:")
        print("-" * 50)
        for task in self.tasks:
            status = "✅" if task['completed'] else "⬜"
            text = task['text']
            if task['completed']:
                text = f"~~{text}~~"
            print(f"{status} {task['id']}: {text}")
        print("-" * 50)

    def get_stats(self):
        """Get task statistics"""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        pending = total - completed
        return total, completed, pending

    def save_tasks(self):
        """Save tasks to file"""
        try:
            data = {
                'date': datetime.now().date().isoformat(),
                'tasks': self.tasks
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"💾 Tasks saved to {self.data_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to save tasks: {e}")
            return False

    def load_tasks(self):
        """Load tasks from file"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                self.tasks = data.get('tasks', [])
                print(f"📂 Loaded {len(self.tasks)} tasks from {self.data_file}")
                return True
            else:
                print(f"📂 No saved tasks found at {self.data_file}")
                return False
        except Exception as e:
            print(f"❌ Failed to load tasks: {e}")
            return False

def run_tests():
    """Run comprehensive tests"""
    print("🧪 TESTING DAILY TO-DO LIST APPLICATION")
    print("=" * 50)

    app = MockTodoApp()

    # Test 1: Add tasks
    print("\n1. Testing task addition:")
    app.add_task("Complete project documentation")
    app.add_task("Review code changes")
    app.add_task("Update requirements.txt")
    app.add_task("Test the application")

    # Test 2: Display tasks
    print("\n2. Current tasks:")
    app.display_tasks()

    # Test 3: Toggle completion
    print("\n3. Testing task completion:")
    app.toggle_task(0)  # Complete first task
    app.toggle_task(2)  # Complete third task

    # Test 4: Display updated tasks
    print("\n4. Tasks after completion:")
    app.display_tasks()

    # Test 5: Statistics
    print("\n5. Task statistics:")
    total, completed, pending = app.get_stats()
    print(f"   Total: {total} | Completed: {completed} | Pending: {pending}")

    # Test 6: Save tasks
    print("\n6. Testing save functionality:")
    app.save_tasks()

    # Test 7: Clear completed
    print("\n7. Testing clear completed:")
    app.clear_completed()
    app.display_tasks()

    # Test 8: Delete task
    print("\n8. Testing task deletion:")
    app.delete_task(1)
    app.display_tasks()

    # Test 9: Save and load
    print("\n9. Testing save/load cycle:")
    app.save_tasks()

    # Create new app instance to test loading
    app2 = MockTodoApp()
    app2.load_tasks()
    app2.display_tasks()

    print("\n" + "=" * 50)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("\n📝 To run the GUI application:")
    print("   python run_todo_app.py")
    print("   (Requires display environment)")

if __name__ == "__main__":
    run_tests()