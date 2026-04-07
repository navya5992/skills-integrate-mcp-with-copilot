# Daily To-Do List Desktop Application

A simple and elegant desktop application for managing your daily tasks with checkboxes for tracking completion.

## Features

- ✅ **Add Tasks**: Quickly add new tasks for the day
- ☑️ **Check Completion**: Mark tasks as completed with checkboxes
- 💾 **Auto-Save**: Automatically saves tasks to your home directory
- 📊 **Progress Tracking**: Visual progress bar showing completion status
- 🗑️ **Clear Completed**: Remove completed tasks with one click
- 📂 **Import/Export**: Load and save task lists from/to JSON files
- 🎨 **Modern UI**: Clean, intuitive interface with color-coded tasks

## Screenshots

The application features:
- Task input field with add button
- Scrollable task list with checkboxes
- Statistics display (Total/Completed/Pending)
- Progress bar
- Save/Load functionality

## Installation

### Prerequisites
- Python 3.6 or higher (Tkinter is included by default)

### Running the Application

1. **From project root:**
   ```bash
   python run_todo_app.py
   ```

2. **Direct execution:**
   ```bash
   python src/todo_desktop_app.py
   ```

## Usage

### Adding Tasks
1. Type your task in the input field
2. Click "➕ Add Task" or press Enter
3. Tasks appear in the list below

### Completing Tasks
- Click the checkbox next to any task to mark it complete
- Completed tasks are visually distinguished with strikethrough text and green background

### Managing Tasks
- **Delete Task**: Click the ❌ button next to any task
- **Clear Completed**: Click "🗑️ Clear Completed" to remove all finished tasks
- **Save Tasks**: Click "💾 Save" to manually save current tasks
- **Load Tasks**: Click "📂 Load" to import tasks from a JSON file

### Data Storage
- Tasks are automatically saved to `~/.daily_todo.json`
- Each day starts fresh (old tasks are cleared)
- Manual save/load available for backup and transfer

## File Structure

```
src/
├── todo_desktop_app.py    # Main application
├── memory_game/          # (existing memory game code)
└── ...

run_todo_app.py           # Launcher script
```

## Technical Details

- **GUI Framework**: Tkinter (built-in Python library)
- **Data Storage**: JSON format
- **Persistence**: Automatic save on window close
- **Cross-platform**: Works on Windows, macOS, and Linux

## Keyboard Shortcuts

- **Enter**: Add new task (when typing in input field)
- **Ctrl+S**: Save tasks (not implemented yet)
- **Ctrl+Q**: Quit application

## Future Enhancements

- [ ] Task categories/tags
- [ ] Due dates and reminders
- [ ] Task prioritization
- [ ] Dark mode theme
- [ ] Cloud synchronization
- [ ] Task templates
- [ ] Statistics and analytics

## Troubleshooting

### Application won't start
- Ensure Python 3.6+ is installed
- Check that Tkinter is available: `python -c "import tkinter"`

### Tasks not saving
- Check write permissions in home directory
- Look for error messages in console

### UI looks strange
- Try different system themes
- Ensure proper display scaling settings

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is part of the Memory Match Arena codebase.