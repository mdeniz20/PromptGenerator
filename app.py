from calendar import c
from ctypes import alignment
import tkinter as tk
from tkinter import ttk
from turtle import up, update, width
import pyperclip
import subprocess
import pickle
import os
import sys

from topics import Topics


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
    update_label.config(text="Checking for updates...", fg="#A97229")
    app.update()
    try:
        subprocess.run(["git", "fetch"], check=True)
        status = subprocess.check_output(["git", "status"]).decode("utf-8")
        if "Your branch is behind" in status:
            set_update_label(True)
        else:
            set_update_label(False)
    except Exception as e:
        print(f"Update check failed: {e}")
    app.after(60*1000, check_for_updates) # Check for updates every 60 seconds


# Apply updates
def apply_updates():
    try:
        # Reset local changes
        subprocess.run(["git", "reset", "--hard"], check=True)
        # Force pull from the remote repository
        subprocess.run(["git", "pull", "origin", "main", "--force"], check=True)
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

def set_update_label(is_update_available):
    if is_update_available:
        update_button.config(bg="green", state="normal", text="Update")
        update_label.config(text="Update available", fg="green")
    else:
        update_button.config(bg="gray", state="disabled", text="Up to date")
        update_label.config(text="No updates available.", fg="gray")

current_dir = os.path.dirname(os.path.abspath(__file__))
topics_file = os.path.join(current_dir, "topics.txt")

# Load cached data
cache = load_cache()

# Initialize the main application window
app = tk.Tk()
app.title("Prompt Generator by Mahmut Ibrahim Deniz")

# Concept Input
tk.Label(app, text="Problem Concept").grid(row=0, column=0, padx=10, pady=5, sticky="w")
concept_input = tk.Entry(app, width=30)
concept_input.grid(row=0, column=1, columnspan=4, padx=10, pady=5, sticky="w")
concept_input.insert(0, cache["concept"])

#Topics
topics = Topics(topics_file)

# Selection Buttons
tk.Label(app, text="Select Items").grid(row=1, column=0, padx=10, pady=5, sticky="w")
items = topics.get_topics_list()
selected_vars = [tk.BooleanVar(value=item in cache["selected_items"]) for item in items]
width = 0
clm = 1
for i, item in enumerate(items):
    check_button = tk.Checkbutton(app, variable=selected_vars[i], text=item)
    check_button.grid(padx=5, pady=5, sticky="w")
    check_button.update()
    width += check_button.winfo_width()
    c_row = 1 + width // 275
    c_clm = 1 + i // c_row
    print(c_row, c_clm)
    check_button.grid(row =c_row, column = c_clm )
end_row = width // 4 + 1
 
# Difficulty Level
tk.Label(app, text="Select Difficulty").grid(row=end_row+1, column=0, padx=10, pady=5, sticky="w")
difficulty_levels = ["Very Easy", "Easy", "Medium", "Hard", "Very Hard"]
difficulty_combobox = ttk.Combobox(app, values=difficulty_levels, state="readonly", width=15)
difficulty_combobox.grid(row=end_row + 1, column=1, columnspan=4,  padx=10, pady=5, sticky="w")
difficulty_combobox.set(cache["difficulty"])

# Generate Button
generate_button = tk.Button(app, text="Generate Prompt Ilhan", command=generate_prompt)
generate_button.grid(row=end_row + 2, column=0, columnspan=2, pady=10)

# Update Button
update_button = tk.Button(app, text="Update", state="disabled", bg="green", command=apply_updates, width=7)
update_button.grid(row=0, column=5, padx=10, pady=5)

update_label = tk.Label(app, text="", fg="gray", width=20)
update_label.grid(row=0, column=5, rowspan=2,padx=10, pady=(20, 5))


# Check for updates at startup
check_for_updates()

# Start the application
app.mainloop()

