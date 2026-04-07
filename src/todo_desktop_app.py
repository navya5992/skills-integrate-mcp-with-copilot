#!/usr/bin/env python3
"""
Daily To-Do List Desktop Application

A simple desktop application for managing daily tasks with checkboxes
for marking completion status.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
from pathlib import Path

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily To-Do List")
        self.root.geometry("600x700")
        self.root.resizable(True, True)

        # Set theme colors
        self.colors = {
            'bg': '#f0f0f0',
            'frame_bg': '#ffffff',
            'button_bg': '#4CAF50',
            'button_fg': '#ffffff',
            'completed_bg': '#e8f5e8',
            'pending_bg': '#fff3e0'
        }

        # Apply theme
        self.root.configure(bg=self.colors['bg'])

        # Data storage
        self.tasks = []
        self.data_file = Path.home() / ".daily_todo.json"

        # Create UI
        self.create_widgets()
        self.load_tasks()

        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """Create all UI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="📝 Daily To-Do List",
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # Date display
        self.date_label = ttk.Label(main_frame,
                                   text=f"📅 {datetime.now().strftime('%B %d, %Y')}",
                                   font=("Arial", 12))
        self.date_label.pack(pady=(0, 20))

        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Add New Task", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 20))

        # Task input
        self.task_entry = ttk.Entry(input_frame, font=("Arial", 11))
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        # Add button
        add_button = tk.Button(input_frame, text="➕ Add Task",
                              command=self.add_task,
                              bg=self.colors['button_bg'],
                              fg=self.colors['button_fg'],
                              font=("Arial", 10, "bold"),
                              padx=20)
        add_button.pack(side=tk.RIGHT)

        # Tasks frame
        tasks_frame = ttk.LabelFrame(main_frame, text="Today's Tasks", padding="10")
        tasks_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Tasks container with scrollbar
        self.tasks_canvas = tk.Canvas(tasks_frame, bg=self.colors['frame_bg'])
        scrollbar = ttk.Scrollbar(tasks_frame, orient="vertical", command=self.tasks_canvas.yview)
        self.tasks_scrollable_frame = ttk.Frame(self.tasks_canvas)

        self.tasks_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
        )

        self.tasks_canvas.create_window((0, 0), window=self.tasks_scrollable_frame, anchor="nw")
        self.tasks_canvas.configure(yscrollcommand=scrollbar.set)

        self.tasks_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Stats frame
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 10))

        self.stats_label = ttk.Label(stats_frame,
                                    text="Total: 0 | Completed: 0 | Pending: 0",
                                    font=("Arial", 10))
        self.stats_label.pack(side=tk.LEFT)

        # Clear completed button
        clear_button = tk.Button(stats_frame, text="🗑️ Clear Completed",
                                command=self.clear_completed,
                                bg="#f44336", fg="white",
                                font=("Arial", 9))
        clear_button.pack(side=tk.RIGHT, padx=(10, 0))

        # Save/Load buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        save_button = tk.Button(button_frame, text="💾 Save",
                               command=self.save_tasks,
                               bg="#2196F3", fg="white",
                               font=("Arial", 9))
        save_button.pack(side=tk.LEFT, padx=(0, 10))

        load_button = tk.Button(button_frame, text="📂 Load",
                               command=self.load_tasks_from_file,
                               bg="#FF9800", fg="white",
                               font=("Arial", 9))
        load_button.pack(side=tk.LEFT)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var,
                                           maximum=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))

    def add_task(self):
        """Add a new task"""
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task description!")
            return

        task = {
            'id': len(self.tasks),
            'text': task_text,
            'completed': False,
            'created': datetime.now().isoformat()
        }

        self.tasks.append(task)
        self.task_entry.delete(0, tk.END)
        self.refresh_tasks_display()
        self.update_stats()

    def toggle_task(self, task_id):
        """Toggle task completion status"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                task['updated'] = datetime.now().isoformat()
                break

        self.refresh_tasks_display()
        self.update_stats()

    def delete_task(self, task_id):
        """Delete a task"""
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.refresh_tasks_display()
        self.update_stats()

    def clear_completed(self):
        """Remove all completed tasks"""
        self.tasks = [task for task in self.tasks if not task['completed']]
        self.refresh_tasks_display()
        self.update_stats()

    def refresh_tasks_display(self):
        """Refresh the tasks display"""
        # Clear existing tasks
        for widget in self.tasks_scrollable_frame.winfo_children():
            widget.destroy()

        # Display tasks
        for i, task in enumerate(self.tasks):
            # Task frame
            task_frame = tk.Frame(self.tasks_scrollable_frame,
                                 bg=self.colors['completed_bg'] if task['completed'] else self.colors['pending_bg'],
                                 relief="raised", borderwidth=1)
            task_frame.pack(fill=tk.X, pady=2, padx=5)

            # Checkbox
            var = tk.BooleanVar(value=task['completed'])
            checkbox = tk.Checkbutton(task_frame, variable=var,
                                     command=lambda tid=task['id']: self.toggle_task(tid),
                                     bg=task_frame['bg'])
            checkbox.pack(side=tk.LEFT, padx=(5, 0))

            # Task text
            text_color = "#666666" if task['completed'] else "#000000"
            text_font = ("Arial", 10, "overstrike") if task['completed'] else ("Arial", 10)

            task_label = tk.Label(task_frame, text=task['text'],
                                 bg=task_frame['bg'], fg=text_color,
                                 font=text_font, anchor="w")
            task_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

            # Delete button
            delete_btn = tk.Button(task_frame, text="❌",
                                  command=lambda tid=task['id']: self.delete_task(tid),
                                  bg="#f44336", fg="white",
                                  font=("Arial", 8), width=3)
            delete_btn.pack(side=tk.RIGHT, padx=(0, 5), pady=2)

    def update_stats(self):
        """Update statistics display"""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        pending = total - completed

        self.stats_label.config(text=f"Total: {total} | Completed: {completed} | Pending: {pending}")

        # Update progress bar
        if total > 0:
            progress = (completed / total) * 100
        else:
            progress = 0
        self.progress_var.set(progress)

    def save_tasks(self):
        """Save tasks to default file"""
        try:
            data = {
                'date': datetime.now().date().isoformat(),
                'tasks': self.tasks
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Success", "Tasks saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")

    def load_tasks(self):
        """Load tasks from default file"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r') as f:
                    data = json.load(f)

                # Check if it's today's data
                today = datetime.now().date().isoformat()
                if data.get('date') == today:
                    self.tasks = data.get('tasks', [])
                else:
                    # Clear old tasks for new day
                    self.tasks = []

                self.refresh_tasks_display()
                self.update_stats()
        except Exception as e:
            print(f"Error loading tasks: {e}")

    def load_tasks_from_file(self):
        """Load tasks from user-selected file"""
        file_path = filedialog.askopenfilename(
            title="Select Todo File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.refresh_tasks_display()
                    self.update_stats()
                    messagebox.showinfo("Success", "Tasks loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks: {e}")

    def on_closing(self):
        """Handle window closing"""
        if messagebox.askyesno("Quit", "Do you want to save your tasks before quitting?"):
            self.save_tasks()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()