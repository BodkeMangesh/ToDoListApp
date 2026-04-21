import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

FILE_NAME = "tasks.json"

# ---------------- DATA ----------------
tasks = []

def load_tasks():
    global tasks
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            tasks = json.load(f)
    refresh_list()

def save_tasks():
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f)

# ---------------- UI FUNCTIONS ----------------
def refresh_list(filtered=None):
    listbox.delete(0, tk.END)
    data = filtered if filtered is not None else tasks

    for i, task in enumerate(data, start=1):
        status = "✔" if task["done"] else "❌"
        time = task["time"]
        listbox.insert(tk.END, f"{i}. {task['name']} [{status}] ({time})")

def add_task():
    name = entry.get().strip()
    if name == "":
        messagebox.showwarning("Warning", "Enter a task")
        return

    task = {
        "name": name,
        "done": False,
        "time": datetime.now().strftime("%d-%m-%Y %H:%M")
    }

    tasks.append(task)
    entry.delete(0, tk.END)
    refresh_list()
    save_tasks()

def remove_task():
    try:
        index = listbox.curselection()[0]
        if messagebox.askyesno("Confirm", "Delete this task?"):
            tasks.pop(index)
            refresh_list()
            save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task")

def update_task():
    try:
        index = listbox.curselection()[0]
        new_name = entry.get().strip()

        if new_name == "":
            messagebox.showwarning("Warning", "Enter new task name")
            return

        tasks[index]["name"] = new_name
        entry.delete(0, tk.END)
        refresh_list()
        save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task")

def mark_done():
    try:
        index = listbox.curselection()[0]
        tasks[index]["done"] = True
        refresh_list()
        save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task")

def search_task():
    query = entry.get().lower()
    filtered = [t for t in tasks if query in t["name"].lower()]
    refresh_list(filtered)

def clear_all():
    if messagebox.askyesno("Confirm", "Delete ALL tasks?"):
        tasks.clear()
        refresh_list()
        save_tasks()

# ---------------- UI SETUP ----------------
root = tk.Tk()
root.title("Task Manager Pro")
root.geometry("500x500")
root.configure(bg="#2c3e50")

tk.Label(root, text="Task Manager", font=("Arial", 18, "bold"),
         bg="#2c3e50", fg="white").pack(pady=10)

entry = tk.Entry(root, width=35, font=("Arial", 12))
entry.pack(pady=10)

listbox = tk.Listbox(root, width=55, height=12, font=("Arial", 11))
listbox.pack(pady=10)

# Buttons Frame
frame = tk.Frame(root, bg="#2c3e50")
frame.pack()

tk.Button(frame, text="Add", width=10, command=add_task).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame, text="Update", width=10, command=update_task).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Delete", width=10, command=remove_task).grid(row=0, column=2, padx=5)

tk.Button(frame, text="Done", width=10, command=mark_done).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame, text="Search", width=10, command=search_task).grid(row=1, column=1, padx=5)
tk.Button(frame, text="Clear All", width=10, command=clear_all).grid(row=1, column=2, padx=5)

# Load tasks on start
load_tasks()

root.mainloop()