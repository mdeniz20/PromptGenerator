import tkinter as tk
from tkinter import ttk
import pyperclip
import subprocess
import pickle
import os
import sys


# Function to load cached data
def load_cache():
    if os.path.exists("cache.pkl"):
        with open("cache.pkl", "rb") as file:
            return pickle.load(file)
    return {"concept": "", "selected_items": [], "difficulty": "Medium"}


# Function to save cached data
def save_cache(data):
    with open("cache.pkl", "wb") as file:
        pickle.dump(data, file)


# Check for updates
def check_for_updates():
    update_button.config(bg='green', state='normal')
    return
    try:
        subprocess.run(["git", "fetch"], check=True)
        status = subprocess.check_output(["git", "status"]).decode("utf-8")
        if "Your branch is behind" in status:
            update_button.config(bg="green", state="normal")
    except Exception as e:
        print(f"Update check failed: {e}")


# Apply updates
def apply_updates():
    try:
        subprocess.run(["git", "pull"], check=True)
        python = sys.executable
        os.execl(python, python, *sys.argv)
    except Exception as e:
        print(f"Update failed: {e}")


# Generate and copy prompt
def generate_prompt():
    concept = concept_input.get()
    selected_items = [item for item, var in zip(items, selected_vars) if var.get()]
    difficulty = difficulty_combobox.get()
    prompt = f"Concept: {concept}\nSelected Items: {', '.join(selected_items)}\nDifficulty: {difficulty}"
    pyperclip.copy(prompt)
    save_cache({"concept": concept, "selected_items": selected_items, "difficulty": difficulty})


# Load cached data
cache = load_cache()

# Initialize the main application window
app = tk.Tk()
app.title("Prompt Generator")

# Concept Input
tk.Label(app, text="Problem Concept").grid(row=0, column=0, padx=10, pady=5, sticky="w")
concept_input = tk.Entry(app, width=40)
concept_input.grid(row=0, column=1, padx=10, pady=5)
concept_input.insert(0, cache["concept"])

# Selection Buttons
tk.Label(app, text="Select Items").grid(row=1, column=0, padx=10, pady=5, sticky="w")
items = [f"item{i}" for i in range(1, 8)]
selected_vars = [tk.BooleanVar(value=item in cache["selected_items"]) for item in items]
for i, item in enumerate(items):
    tk.Checkbutton(app, text=item, variable=selected_vars[i]).grid(row=1, column=1 + i, padx=5, pady=5)

# Difficulty Level
tk.Label(app, text="Difficulty").grid(row=2, column=0, padx=10, pady=5, sticky="w")
difficulty_levels = ["Very Easy", "Easy", "Medium", "Hard", "Very Hard"]
difficulty_combobox = ttk.Combobox(app, values=difficulty_levels, state="readonly", width=15)
difficulty_combobox.grid(row=2, column=1, padx=10, pady=5)
difficulty_combobox.set(cache["difficulty"])

# Generate Button
generate_button = tk.Button(app, text="Generate Prompt", command=generate_prompt)
generate_button.grid(row=3, column=0, columnspan=2, pady=10)

# Update Button
update_button = tk.Button(app, text="Update", state="disabled", bg="gray", command=apply_updates)
update_button.grid(row=0, column=2, padx=10, pady=5)

# Check for updates at startup
check_for_updates()

# Start the application
app.mainloop()

