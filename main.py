# Importing requisite packages
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
import jedi
from googletrans import Translator
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

        # File Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Tab", command=self.add_new_tab)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save File", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Adding theme menu
        theme_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="Themes", menu=theme_menu)
        theme_menu.add_command(label="Light", command=lambda: change_theme("white", "black"))
        theme_menu.add_command(label="Dark", command=lambda: change_theme("black", "white"))
    
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
    
    def apply_syntax_highlighting(text_widget):
            text_widget.tag_config("Keyword", foreground="blue")
            text_widget.tag_config("String", foreground="green")
            text_widget.tag_config("Comment", foreground="gray")
            content = text_widget.get("1.0", tk.END)
            for token, value in lex(content, PythonLexer()):
                if token in Token.Keyword:
                    start, end = locate_in_text(value, text_widget)
                    text_widget.tag_add("Keyword", start, end)
                elif token in Token.String:
                    start, end = locate_in_text(value, text_widget)
                    text_widget.tag_add("String", start, end)

    def autocomplete(event):
        source = text_widget.get("1.0", tk.END)
        script = jedi.Script(source=source, line=event.widget.index("insert").split(".")[0])
        completions = script.complete()
        menu = tk.Menu(text_widget, tearoff=False)
        for completion in completions:
            menu.add_command(label=completion.name, command=lambda c=completion.name: insert_completion(c, event))
            menu.post(event.x_root, event.y_root)
    def open_search_replace():
        dialog = tk.Toplevel(root)
        dialog.title("Search and Replace")
        tk.Label(dialog, text="Find:").grid(row=0, column=0)
        find_entry = tk.Entry(dialog)
        find_entry.grid(row=0, column=1)
        tk.Label(dialog, text="Replace:").grid(row=1, column=0)
        replace_entry = tk.Entry(dialog)
        replace_entry.grid(row=1, column=1)
        tk.Button(dialog, text="Replace All", command=lambda: replace_all(find_entry.get(), replace_entry.get())).grid(row=2, columnspan=2)

    def replace_all(find_text, replace_text):
        content = text_widget.get("1.0", tk.END)
        content = content.replace(find_text, replace_text)
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", content)
    


    def translate_text(language_code):
        content = text_widget.get("1.0", tk.END)
        translated = translator.translate(content, dest=language_code).text
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", translated)

    def optimized_read(file_path):
        with open(file_path, "rb") as file:
            return file.read().decode("utf-8", errors="ignore")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = NoteTakingApp(root)
    root.mainloop()
