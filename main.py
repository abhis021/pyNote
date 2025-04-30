import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class NoteTakingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Taking App")
        self.create_widgets()
    
    def create_widgets(self):
        # Tabbed editing
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both")
        self.add_new_tab()

        # Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Tab", command=self.add_new_tab)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save File", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
    
    def add_new_tab(self):
        frame = tk.Frame(self.notebook)
        frame.pack(fill="both", expand=True)
        text_area = tk.Text(frame, wrap="word", undo=True)
        text_area.pack(fill="both", expand=True)
        self.notebook.add(frame, text=f"Tab {len(self.notebook.tabs()) + 1}")
    
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            text_area = self.get_current_text_widget()
            text_area.delete(1.0, tk.END)
            text_area.insert(1.0, content)
    
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                text_area = self.get_current_text_widget()
                content = text_area.get(1.0, tk.END)
                file.write(content.strip())
    
    def get_current_text_widget(self):
        current_tab = self.notebook.select()
        current_frame = self.notebook.nametowidget(current_tab)
        return current_frame.winfo_children()[0]  # The first widget in the frame is the text widget

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteTakingApp(root)
    root.mainloop()
