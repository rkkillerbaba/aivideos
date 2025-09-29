import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import importlib.util

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr

def clone_roop():
    output = run_command("git clone https://github.com/FurkanGozukara/rop_fixed roop")
    messagebox.showinfo("Clone Output", output)

def clone_basicsr():
    output = run_command("cd roop && git clone https://github.com/FurkanGozukara/BasicSR")
    messagebox.showinfo("Clone Output", output)

def install_requirements():
    output = run_command("cd roop && pip install -r a.txt")
    messagebox.showinfo("Install Output", output)

def uninstall_basicsr():
    output = run_command("pip uninstall basicsr --yes")
    messagebox.showinfo("Uninstall Output", output)

def install_basicsr_editable():
    output = run_command("cd roop/BasicSR && pip install -e .")
    messagebox.showinfo("Install Output", output)

def patch_opennsfw2():
    module_name = "opennsfw2._inference"
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None or spec.origin is None:
            messagebox.showerror("Patch Error", f"Could not find the module '{module_name}'. Is opennsfw2 installed?")
        else:
            file_path = spec.origin
            with open(file_path, 'r') as f:
                lines = f.readlines()
            patched = False
            with open(file_path, 'w') as f:
                for line in lines:
                    if "cv2.destroyAllWindows()" in line:
                        f.write("#" + line)
                        patched = True
                    else:
                        f.write(line)
            if patched:
                messagebox.showinfo("Patch", "Patch applied successfully!")
            else:
                messagebox.showwarning("Patch", "The line 'cv2.destroyAllWindows()' was not found. The file may already be patched or has changed.")
    except Exception as e:
        messagebox.showerror("Patch Error", f"An error occurred: {e}\nPlease ensure the 'opennsfw2' library is installed correctly.")

root = tk.Tk()
root.title("AI Tools GUI")

# Buttons for each step
tk.Button(root, text="Clone roop", command=clone_roop).pack(fill='x')
tk.Button(root, text="Clone BasicSR", command=clone_basicsr).pack(fill='x')
tk.Button(root, text="Install Requirements", command=install_requirements).pack(fill='x')
tk.Button(root, text="Uninstall basicsr", command=uninstall_basicsr).pack(fill='x')
tk.Button(root, text="Install BasicSR Editable", command=install_basicsr_editable).pack(fill='x')
tk.Button(root, text="Patch opennsfw2", command=patch_opennsfw2).pack(fill='x')

root.mainloop()
