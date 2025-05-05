import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from pygments.token import Token
import os

# Requires: pip install pygments

class TabEditor(ttk.Frame):
    def __init__(self, master, language='python'):
        super().__init__(master)
        self.language = language

        self.text = tk.Text(self, wrap='none', undo=True)
        self.vsb = ttk.Scrollbar(self, orient='vertical', command=self.text.yview)
        self.hsb = ttk.Scrollbar(self, orient='horizontal', command=self.text.xview)

        self.text.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.text.pack(fill='both', expand=True, side='left')
        self.vsb.pack(fill='y', side='right')
        self.hsb.pack(fill='x', side='bottom')

        self.text.bind('<KeyRelease>', self.on_key_release)
        self.file_path = None

    def on_key_release(self, event=None):
        self.highlight_syntax()

    def highlight_syntax(self):
        code = self.text.get('1.0', 'end-1c')
        lexer = get_lexer_by_name(self.language)
        for tag in self.text.tag_names():
            self.text.tag_delete(tag)
        
        for token, content in lex(code, lexer):
            tag_name = str(token)
            self.text.tag_configure(tag_name, foreground='blue')
            start_index = self.text.search(content, '1.0', stopindex='end', count=tk.IntVar())
            if start_index:
                end_index = f"{start_index}+{len(content)}c"
                self.text.tag_add(tag_name, start_index, end_index)

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Taking App")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_tab)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.search_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Search", menu=self.search_menu)
        self.search_menu.add_command(label="Find", command=self.find_text)
        self.search_menu.add_command(label="Replace", command=self.replace_text)

        self.new_tab()

    def new_tab(self):
        tab = TabEditor(self.notebook)
        self.notebook.add(tab, text="Untitled")
        self.notebook.select(tab)

    def open_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            tab = TabEditor(self.notebook)
            tab.text.insert('1.0', content)
            tab.file_path = filepath
            self.notebook.add(tab, text=os.path.basename(filepath))
            self.notebook.select(tab)

    def save_file(self):
        tab = self.get_current_tab()
        if not tab:
            return
        if tab.file_path is None:
            filepath = filedialog.asksaveasfilename(defaultextension=".txt")
            if filepath:
                tab.file_path = filepath
            else:
                return
        with open(tab.file_path, 'w', encoding='utf-8') as file:
            file.write(tab.text.get('1.0', 'end-1c'))
        self.notebook.tab(tab, text=os.path.basename(tab.file_path))

    def get_current_tab(self):
        widget = self.notebook.nametowidget(self.notebook.select())
        return widget if isinstance(widget, TabEditor) else None

    def find_text(self):
        def search():
            self.text.tag_remove('found', '1.0', tk.END)
            term = entry.get()
            if term:
                start_pos = '1.0'
                while True:
                    start_pos = self.text.search(term, start_pos, stopindex=tk.END)
                    if not start_pos:
                        break
                    end_pos = f"{start_pos}+{len(term)}c"
                    self.text.tag_add('found', start_pos, end_pos)
                    self.text.tag_config('found', background='yellow')
                    start_pos = end_pos

        self.text = self.get_current_tab().text
        win = tk.Toplevel()
        win.title("Find")
        tk.Label(win, text="Find: ").pack(side='left')
        entry = tk.Entry(win)
        entry.pack(side='left', fill='both', expand=True)
        tk.Button(win, text="Search", command=search).pack(side='left')

    def replace_text(self):
        def replace():
            self.text.tag_remove('found', '1.0', tk.END)
            find_term = entry_find.get()
            replace_term = entry_replace.get()
            content = self.text.get('1.0', tk.END)
            content = content.replace(find_term, replace_term)
            self.text.delete('1.0', tk.END)
            self.text.insert('1.0', content)

        self.text = self.get_current_tab().text
        win = tk.Toplevel()
        win.title("Replace")
        tk.Label(win, text="Find: ").pack()
        entry_find = tk.Entry(win)
        entry_find.pack(fill='both', expand=True)
        tk.Label(win, text="Replace: ").pack()
        entry_replace = tk.Entry(win)
        entry_replace.pack(fill='both', expand=True)
        tk.Button(win, text="Replace All", command=replace).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
