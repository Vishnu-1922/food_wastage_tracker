import tkinter as tk
from tkinter import messagebox
import json
import re
import random

# Load existing waste data if available
try:
    with open("food_waste.json", "r") as file:
        food_waste_data = json.load(file)
except FileNotFoundError:
    food_waste_data = {}

# Food-specific messages
food_messages = {
    "rice": "Cook less next time to avoid leftovers.",
    "fruits": "Use ripe fruits for smoothies or desserts.",
    "vegetables": "Plan meals to use up veggies before they spoil.",
    "meat": "Freeze meat to keep it fresh for longer.",
    "milk": "Buy smaller quantities or check expiration dates."
}

# Motivational messages
motivational_messages = [
    "Every small step counts! Keep it up!",
    "Great job tracking! You're making a difference!",
    "Reducing waste means saving the planet. Well done!",
    "Your efforts matter! Let's keep going!"
]

def save_data():
    with open("food_waste.json", "w") as file:
        json.dump(food_waste_data, file, indent=4)

def log_waste():
    item = item_entry.get().strip().lower()
    quantity = quantity_entry.get().strip()
    if item and quantity:
        if item in food_waste_data:
            food_waste_data[item].append(quantity)
        else:
            food_waste_data[item] = [quantity]
        save_data()
        message = food_messages.get(item, random.choice(motivational_messages))
        messagebox.showinfo("Logged", f"Logged {quantity} of {item} discarded.\n{message}")
        item_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter both item and quantity.")

def show_report():
    if not food_waste_data:
        messagebox.showinfo("Report", "No food waste recorded yet.")
        return
    total_waste = sum(
        float(re.search(r"[0-9.]+", q).group()) 
        for quantities in food_waste_data.values() 
        for q in quantities if re.search(r"[0-9.]+", q)
    )
    message = random.choice(motivational_messages)
    report_text = f"\n--- Food Waste Report ---\nTotal Food Waste: {total_waste} units\n{message}"
    messagebox.showinfo("Waste Report", report_text)
    food_waste_data.clear()

# GUI Setup
root = tk.Tk()
root.title("Food Waste Tracker")
root.geometry("350x300")
root.resizable(False, False)

tk.Label(root, text="Food Waste Tracker", font=("Arial", 16, "bold")).pack(pady=10)
tk.Label(root, text="Food Item:", font=("Arial", 10)).pack()
item_entry = tk.Entry(root, font=("Arial", 10))
item_entry.pack(pady=5)
tk.Label(root, text="Quantity (in units):", font=("Arial", 10)).pack()
quantity_entry = tk.Entry(root, font=("Arial", 10))
quantity_entry.pack(pady=5)

tk.Button(root, text="Log Waste", command=log_waste, font=("Arial", 10), bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(root, text="Show Report", command=show_report, font=("Arial", 10), bg="#2196F3", fg="white").pack(pady=5)
tk.Button(root, text="Exit", command=root.quit, font=("Arial", 10), bg="#f44336", fg="white").pack(pady=5)

root.mainloop()

