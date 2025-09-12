# password_generator.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import secrets
import string

def build_charset(use_lower, use_upper, use_digits, use_symbols):
    charset_parts = []
    if use_lower:
        charset_parts.append(string.ascii_lowercase)
    if use_upper:
        charset_parts.append(string.ascii_uppercase)
    if use_digits:
        charset_parts.append(string.digits)
    if use_symbols:
        charset_parts.append("!@#$%^&*()-_=+[]{};:,.<>/?|~")
    return charset_parts

def generate_password_single(length, charset_parts):
    if not charset_parts:
        raise ValueError("No character set selected")
    if len(charset_parts) == 1:
        return ''.join(secrets.choice(charset_parts[0]) for _ in range(length))
    if length < len(charset_parts):
        union = ''.join(charset_parts)
        return ''.join(secrets.choice(union) for _ in range(length))
    password_chars = [secrets.choice(part) for part in charset_parts]
    union = ''.join(charset_parts)
    for _ in range(length - len(password_chars)):
        password_chars.append(secrets.choice(union))
    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)

def generate_passwords():
    try:
        length = int(length_var.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid length")
        return
    use_lower = lower_var.get()
    use_upper = upper_var.get()
    use_digits = digits_var.get()
    use_symbols = symbols_var.get()
    try:
        count = int(count_var.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid quantity")
        return
    charset_parts = build_charset(use_lower, use_upper, use_digits, use_symbols)
    if not charset_parts:
        messagebox.showwarning("Warning", "Select at least one character type.")
        return
    if length <= 0:
        messagebox.showwarning("Warning", "Length must be greater than 0.")
        return
    if count <= 0:
        messagebox.showwarning("Warning", "Quantity must be greater than 0.")
        return
    if count > 500:
        if not messagebox.askyesno("Confirm", "You requested more than 500 passwords. Continue?"):
            return
    listbox_passwords.delete(0, tk.END)
    for _ in range(count):
        pwd = generate_password_single(length, charset_parts)
        listbox_passwords.insert(tk.END, pwd)

def copy_selected():
    selection = listbox_passwords.curselection()
    if not selection:
        messagebox.showinfo("Info", "Select one password from the list to copy.")
        return
    pwd = listbox_passwords.get(selection[0])
    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Copied", "Password copied to clipboard.")

def copy_all():
    items = listbox_passwords.get(0, tk.END)
    if not items:
        messagebox.showinfo("Info", "No passwords to copy.")
        return
    text = "\n".join(items)
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Copied", "All passwords copied to clipboard.")

def save_to_file():
    items = listbox_passwords.get(0, tk.END)
    if not items:
        messagebox.showinfo("Info", "No passwords to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files","*.txt"),("All files","*.*")])
    if not file_path:
        return
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for p in items:
                f.write(p + "\n")
        messagebox.showinfo("Saved", f"Passwords saved to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")

def select_all_listbox(event=None):
    listbox_passwords.select_set(0, tk.END)

root = tk.Tk()
root.title("Password Generator")
root.geometry("680x420")
root.resizable(False, False)
padding = {"padx": 8, "pady": 6}

main = ttk.Frame(root)
main.pack(fill=tk.BOTH, expand=True, **padding)

options_frame = ttk.LabelFrame(main, text="Options")
options_frame.grid(row=0, column=0, sticky="nw", **padding)

ttk.Label(options_frame, text="Length:").grid(row=0, column=0, sticky="w")
length_var = tk.StringVar(value="12")
length_spin = ttk.Spinbox(options_frame, from_=4, to=128, textvariable=length_var, width=6)
length_spin.grid(row=0, column=1, sticky="w")

lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)

ttk.Checkbutton(options_frame, text="Lowercase letters", variable=lower_var).grid(row=1, column=0, columnspan=2, sticky="w")
ttk.Checkbutton(options_frame, text="Uppercase letters", variable=upper_var).grid(row=2, column=0, columnspan=2, sticky="w")
ttk.Checkbutton(options_frame, text="Digits (0-9)", variable=digits_var).grid(row=3, column=0, columnspan=2, sticky="w")
ttk.Checkbutton(options_frame, text="Symbols", variable=symbols_var).grid(row=4, column=0, columnspan=2, sticky="w")

ttk.Label(options_frame, text="Number of passwords:").grid(row=5, column=0, sticky="w", pady=(8,0))
count_var = tk.StringVar(value="10")
count_spin = ttk.Spinbox(options_frame, from_=1, to=500, textvariable=count_var, width=6)
count_spin.grid(row=5, column=1, sticky="w", pady=(8,0))

buttons_frame = ttk.Frame(main)
buttons_frame.grid(row=1, column=0, sticky="w", **padding)

generate_btn = ttk.Button(buttons_frame, text="Generate", command=generate_passwords)
generate_btn.grid(row=0, column=0, padx=4)
copy_btn = ttk.Button(buttons_frame, text="Copy selected", command=copy_selected)
copy_btn.grid(row=0, column=1, padx=4)
copy_all_btn = ttk.Button(buttons_frame, text="Copy all", command=copy_all)
copy_all_btn.grid(row=0, column=2, padx=4)
save_btn = ttk.Button(buttons_frame, text="Save to file", command=save_to_file)
save_btn.grid(row=0, column=3, padx=4)

list_frame = ttk.LabelFrame(main, text="Generated passwords")
list_frame.grid(row=0, column=1, rowspan=3, sticky="nsew", **padding)
main.columnconfigure(1, weight=1)
main.rowconfigure(2, weight=1)

listbox_passwords = tk.Listbox(list_frame, width=40, height=18, selectmode=tk.SINGLE)
listbox_passwords.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6,0), pady=6)

scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox_passwords.yview)
scrollbar.pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=6)
listbox_passwords.config(yscrollcommand=scrollbar.set)

root.bind("<Control-a>", select_all_listbox)

footer = ttk.Label(root, text="Tip: choose at least one character type. Length ≥12 is recommended for strong passwords.", anchor="center")
footer.pack(side=tk.BOTTOM, fill=tk.X, pady=(0,8))

root.mainloop()
