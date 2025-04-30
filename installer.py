import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import platform

class InstallerWizard:
    def __init__(self, master):
        self.master = master
        master.title("Notepad App Installer")

        self.current_step = 0
        self.steps = [
            self.create_welcome_page,
            self.create_license_page,
            self.create_installation_path_page,
            self.create_installation_progress_page,
            self.create_completion_page
        ]

        self.app_name = "SimpleNotepad"
        self.app_version = "1.0"
        self.license_text = """
MIT License

Copyright (c) [Year] [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        self.installation_path = tk.StringVar(value=self.get_default_install_path())
        self.progress = tk.DoubleVar(value=0)
        self.installation_successful = False

        self.content_frame = ttk.Frame(master, padding=10)
        self.content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.button_frame = ttk.Frame(master, padding=10)
        self.button_frame.grid(row=1, column=0, sticky=(tk.E))

        self.prev_button = ttk.Button(self.button_frame, text="< Previous", command=self.prev_step, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(self.button_frame, text="Next >", command=self.next_step)
        self.next_button.pack(side=tk.RIGHT, padx=5)

        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=master.destroy)
        self.cancel_button.pack(side=tk.RIGHT, padx=5)

        self.show_current_step()

    def get_default_install_path(self):
        system = platform.system()
        if system == "Windows":
            return os.path.join(os.environ["ProgramFiles"], self.app_name)
        elif system == "Linux":
            return os.path.join(os.environ["HOME"], ".local", "share", self.app_name)
        elif system == "Darwin":  # macOS
            return os.path.join(os.environ["HOME"], "Applications", self.app_name)
        return "./" + self.app_name  # Default if OS not recognized

    def show_current_step(self):
        self.prev_button.config(state=tk.NORMAL if self.current_step > 0 else tk.DISABLED)
        if self.current_step == len(self.steps) - 1:
            self.next_button.config(text="Finish", command=self.master.destroy)
        elif self.current_step == len(self.steps) - 2:
            self.next_button.config(text="Install", command=self.start_installation)
        else:
            self.next_button.config(text="Next >", command=self.next_step)

        # Clear previous content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.steps[self.current_step](self.content_frame)

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            if self.current_step == 2:  # Validation on installation path page
                path = self.installation_path.get()
                if not path:
                    messagebox.showerror("Error", "Please select an installation path.")
                    return
                if os.path.exists(path) and os.listdir(path):
                    if not messagebox.askyesno("Warning", f"The directory '{path}' is not empty. Continue installation?"):
                        return
            self.current_step += 1
            self.show_current_step()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_current_step()

    def create_welcome_page(self, parent):
        ttk.Label(parent, text=f"Welcome to the {self.app_name} Installer!", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(parent, text=f"This wizard will guide you through the installation of {self.app_name} {self.app_version}.").pack(pady=5)
        ttk.Label(parent, text="Click 'Next' to continue.", justify=tk.LEFT).pack(pady=10, anchor=tk.W)

    def create_license_page(self, parent):
        ttk.Label(parent, text="License Agreement", font=("Arial", 14, "bold")).pack(pady=10, anchor=tk.W)
        license_textbox = tk.Text(parent, height=15, width=60)
        license_textbox.insert(tk.END, self.license_text)
        license_textbox.config(state=tk.DISABLED)
        license_textbox.pack(pady=5)
        self.accept_var = tk.BooleanVar(value=False)
        accept_check = ttk.Checkbutton(parent, text="I accept the terms in the License Agreement", variable=self.accept_var)
        accept_check.pack(pady=10, anchor=tk.W)

        def enable_next():
            self.next_button.config(state=tk.NORMAL if self.accept_var.get() else tk.DISABLED)
        self.accept_var.trace_add("write", lambda *args: enable_next())
        self.next_button.config(state=tk.DISABLED) # Initially disabled

    def create_installation_path_page(self, parent):
        ttk.Label(parent, text="Choose Install Location", font=("Arial", 14, "bold")).pack(pady=10, anchor=tk.W)
        ttk.Label(parent, text="Select the folder where you want to install SimpleNotepad:", justify=tk.LEFT).pack(pady=5, anchor=tk.W)
        path_entry = ttk.Entry(parent, textvariable=self.installation_path, width=50)
        path_entry.pack(pady=5, fill=tk.X)
        browse_button = ttk.Button(parent, text="Browse...", command=self.browse_install_path)
        browse_button.pack(pady=5, anchor=tk.W)

    def browse_install_path(self):
        directory = filedialog.askdirectory(title="Select Installation Folder", initialdir=self.installation_path.get())
        if directory:
            self.installation_path.set(directory)

    def create_installation_progress_page(self, parent):
        ttk.Label(parent, text="Installation Progress", font=("Arial", 14, "bold")).pack(pady=10, anchor=tk.W)
        self.progress_bar = ttk.Progressbar(parent, variable=self.progress, maximum=100, length=300)
        self.progress_bar.pack(pady=20)
        self.progress_label = ttk.Label(parent, text="Preparing...")
        self.progress_label.pack(pady=5)
        self.next_button.config(state=tk.DISABLED)
        self.prev_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)

    def start_installation(self):
        self.current_step += 1
        self.show_current_step()
        self.master.after(100, self.perform_installation)

    def perform_installation(self):
        install_dir = self.installation_path.get()
        os.makedirs(install_dir, exist_ok=True)

        # Simulate copying application files (replace with your actual file operations)
        files_to_copy = ["notepad_app.py", "resources/icon.png", "README.txt"] # Example files
        total_files = len(files_to_copy)

        for i, file in enumerate(files_to_copy):
            source_path = self.find_app_file(file) # Assuming your app files are in the same directory or 'app_files' subfolder
            if source_path:
                destination_path = os.path.join(install_dir, file)
                try:
                    shutil.copy2(source_path, destination_path) # copy2 preserves metadata
                    self.progress.set((i + 1) / total_files * 100)
                    self.progress_label.config(text=f"Copying: {file}")
                    self.master.update()
                except Exception as e:
                    messagebox.showerror("Installation Error", f"Failed to copy '{file}': {e}")
                    self.progress_label.config(text="Installation Failed")
                    return

            else:
                messagebox.showerror("Installation Error", f"Source file '{file}' not found.")
                self.progress_label.config(text="Installation Failed")
                return

        # Create desktop shortcut (platform-specific)
        self.create_desktop_shortcut(install_dir)

        self.installation_successful = True
        self.progress.set(100)
        self.progress_label.config(text="Installation Complete!")
        self.show_current_step() # Update buttons for completion page

    def find_app_file(self, filename):
        # Try current directory, then 'app_files' subdirectory
        if os.path.exists(filename):
            return filename
        app_files_dir = "app_files"
        if os.path.exists(os.path.join(app_files_dir, filename)):
            return os.path.join(app_files_dir, filename)
        return None

    def create_desktop_shortcut(self, install_dir):
        system = platform.system()
        app_path = os.path.join(install_dir, "notepad_app.py") # Adjust if your main script has a different name

        if system == "Windows":
            import winshell
            from win32com.client import Dispatch
            desktop = winshell.desktop()
            path = os.path.join(desktop, f"{self.app_name}.lnk")
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = f"pythonw.exe \"{app_path}\"" # Use pythonw for no console window
            shortcut.WorkingDirectory = install_dir
            # shortcut.IconLocation = os.path.join(install_dir, "resources", "icon.ico"), 0 # If you have an icon
            shortcut.save()
        elif system == "Linux":
            # Create a .desktop file
            desktop_entry = f"""[Desktop Entry]
Name={self.app_name}
Comment=A simple notepad application
Exec=python3 "{app_path}"
Icon={os.path.join(install_dir, "resources", "icon.png")}
Terminal=false
Type=Application
Categories=Utility;TextEditor;
"""
            desktop_file_path = os.path.join(os.environ["HOME"], ".local", "share", "applications", f"{self.app_name}.desktop")
            os.makedirs(os.path.dirname(desktop_file_path), exist_ok=True)
            with open(desktop_file_path, "w") as f:
                f.write(desktop_entry)
            # Make it executable
            os.chmod(desktop_file_path, 0o755)
        elif system == "Darwin": # macOS
            # Creating a proper .app bundle is more involved, this is a basic approach
            app_link_path = os.path.join(os.environ["HOME"], "Applications", f"{self.app_name}.app")
            script_content = f"""#!/usr/bin/env python3
import subprocess
subprocess.run(["python3", "{app_path}"])
"""
            os.makedirs(app_link_path, exist_ok=True)
            with open(os.path.join(app_link_path, "Contents", "MacOS", self.app_name), "w") as f:
                f.write(script_content)
            os.chmod(os.path.join(app_link_path, "Contents", "MacOS", self.app_name), 0o755)
            # You'd typically create a proper Info.plist and structure for a real .app

    def create_completion_page(self, parent):
        ttk.Label(parent, text="Installation Complete!", font=("Arial", 16, "bold")).pack(pady=10)
        if self.installation_successful:
            ttk.Label(parent, text=f"{self.app_name} has been successfully installed to:", justify=tk.LEFT).pack(pady=5, anchor=tk.W)
            ttk.Label(parent, text=self.installation_path.get(), font=("Arial", 10)).pack(pady=2, anchor=tk.W)
            ttk.Label(parent, text="Click 'Finish' to close the installer.", justify=tk.LEFT).pack(pady=10, anchor=tk.W)
        else:
            ttk.Label(parent, text="Installation Failed.", font=("Arial", 12, "bold"), foreground="red").pack(pady=5)
            ttk.Label(parent, text="Please check the error messages during installation.", justify=tk.LEFT).pack(pady=5, anchor=tk.W)
            self.next_button.config(text="Close", command=self.master.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    installer = InstallerWizard(root)
    root.mainloop()

# Create dummy files and folders for testing
if not os.path.exists("app_files"):
    os.makedirs("app_files")
with open("app_files/notepad_app.py", "w") as f:
    f.write("# Dummy notepad app")
with open("app_files/README.txt", "w") as f:
    f.write("Read me for SimpleNotepad")
if not os.path.exists("app_files/resources"):
    os.makedirs("app_files/resources")
with open("app_files/resources/icon.png", "w") as f:
    f.write("") # Empty icon file