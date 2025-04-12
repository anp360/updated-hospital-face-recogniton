import tkinter as tk
from tkinter import messagebox
import json
from admin_panel import open_admin_panel

CREDENTIALS_PATH = "admin_credentials.json"

def verify_credentials(username, password):
    try:
        with open(CREDENTIALS_PATH, 'r') as file:
            admins = json.load(file)
            for admin in admins:
                if admin['username'] == username and admin['password'] == password:
                    return True
        return False
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read credentials: {e}")
        return False

def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if verify_credentials(username, password):
        login_window.destroy()
        open_admin_panel()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# GUI setup
login_window = tk.Tk()
login_window.title("Admin Login")
login_window.geometry("300x200")

tk.Label(login_window, text="Username:", font=("Arial", 12)).pack(pady=5)
username_entry = tk.Entry(login_window, font=("Arial", 12))
username_entry.pack()

tk.Label(login_window, text="Password:", font=("Arial", 12)).pack(pady=5)
password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
password_entry.pack()

tk.Button(login_window, text="Login", font=("Arial", 12), command=login).pack(pady=15)

login_window.mainloop()
