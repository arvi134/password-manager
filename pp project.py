
import tkinter as tk
from tkinter import messagebox
import random
import string
import json
from cryptography.fernet import Fernet
import os

# ---------- Encryption Key Management ----------
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists("secret.key"):
        generate_key()
    return open("secret.key", "rb").read()

key = load_key()
fernet = Fernet(key)

# ---------- Password Functions ----------
def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def save_password(service, password):
    encrypted = fernet.encrypt(password.encode()).decode()
    data = {}

    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)

    data[service] = encrypted

    with open("passwords.json", "w") as file:
        json.dump(data, file, indent=4)

def retrieve_password(service):
    if not os.path.exists("passwords.json"):
        return "No data found."

    with open("passwords.json", "r") as file:
        data = json.load(file)

    if service in data:
        encrypted = data[service].encode()
        return fernet.decrypt(encrypted).decode()
    else:
        return "Service not found."

# ---------- GUI Setup ----------
def generate_and_save():
    service = entry_service.get().strip()
    if not service:
        messagebox.showwarning("Warning", "Service name cannot be empty.")
        return

    password = generate_password()
    save_password(service, password)
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    messagebox.showinfo("Success", f"Password saved for {service}.")

def get_password():
    service = entry_service.get().strip()
    if not service:
        messagebox.showwarning("Warning", "Enter a service name.")
        return

    password = retrieve_password(service)
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)

# Create GUI window
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x200")

# Service label & entry
tk.Label(root, text="Service Name:").pack(pady=5)
entry_service = tk.Entry(root, width=40)
entry_service.pack()

# Password label & entry
tk.Label(root, text="Password:").pack(pady=5)
entry_password = tk.Entry(root, width=40)
entry_password.pack()

# Buttons
tk.Button(root, text="Generate & Save Password", command=generate_and_save).pack(pady=10)
tk.Button(root, text="Retrieve Password", command=get_password).pack()

# Run app
root.mainloop()
