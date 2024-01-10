import os
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, simpledialog, END

class CloseableTab(ttk.Frame):
    def __init__(self, notebook, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.notebook = notebook
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="", padding=(2, 0))
        self.label.pack(side="left")

        self.close_button = ttk.Button(self, text="x", command=self.close_tab, width=2)
        self.close_button.pack(side="left", padx=(0, 5))

    def close_tab(self):
        confirm_close = messagebox.askyesno("Close Tab", "Do you want to close this tab?")
        if confirm_close:
            self.notebook.forget(self)

class NoteSpace(ttk.Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self, text="Notes", font=('helvetica', 12))
        label.pack(pady=10)

        self.note_text = tk.Text(self, wrap=tk.WORD, height=20, width=40)  # Adjusted height
        self.note_text.pack(padx=10, pady=10, fill="both", expand=True)

class smIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("smIDE 1.3")
        self.root.geometry("1250x750")
        self.root.option_add('*Font', 'helvetica 11')

        self.create_menu()
        self.create_notebook()
        self.create_toolbar()
        self.create_note_space()

        self.tab_counts = {}
        self.current_extension = ""
        self.current_tab = None
        self.current_file_path = None  # Keep track of the currently opened file

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        menu_bar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menu_bar)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root, style='TNotebook')
        self.notebook.pack(side=tk.LEFT, expand=1, fill="both")

        self.notebook.bind("<ButtonRelease-1>", self.on_tab_selected)

        languages = ["HTML", "CSS", "SCSS", "JavaScript", "Python"]
        self.text_widgets = {}
        for lang in languages:
            text_widget = scrolledtext.ScrolledText(self.notebook,
                                                    wrap=tk.WORD,
                                                    bg='#282c34',
                                                    fg='white',
                                                    insertbackground='white',
                                                    insertwidth=4,
                                                    padx=10,
                                                    pady=10)
            text_widget.config(font=('helvetica', 12))
            tab_name = lang
            self.notebook.add(text_widget, text=tab_name)
            self.text_widgets[tab_name] = text_widget
            text_widget.bind("<Control-s>", lambda event, tab=tab_name: self.save_file(tab))

    def create_toolbar(self):
        toolbar = ttk.Frame(self.root)

        new_button = ttk.Button(toolbar, text="New", command=self.new_file)
        open_button = ttk.Button(toolbar, text="Open", command=self.open_file)
        save_button = ttk.Button(toolbar, text="Save", command=self.save_file)
        plus_button = ttk.Button(toolbar, text="+ add Tab +", command=self.create_new_tab)

        new_button.pack(side=tk.LEFT, padx=5)
        open_button.pack(side=tk.LEFT, padx=5)
        save_button.pack(side=tk.LEFT, padx=5)
        plus_button.pack(side=tk.LEFT, padx=5)

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def create_note_space(self):
        note_space = NoteSpace(self.root)
        note_space.pack(side=tk.LEFT, fill="both", padx=10, pady=10, expand=True)

    def on_tab_selected(self, event):
        active_tab = self.notebook.tab(self.notebook.select(), "text")
        self.current_tab = active_tab
        extension_mapping = {
            "HTML": "html",
            "CSS": "css",
            "SCSS": "scss",
            "JavaScript": "js",
            "Python": "py"
        }
        self.current_extension = extension_mapping.get(active_tab, "")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                if self.current_tab:
                    text_widget = self.text_widgets[self.current_tab]
                    text_widget.delete(1.0, tk.END)
                    text_widget.insert(tk.END, content)
                self.current_file_path = file_path  # Update the current file path

    def save_file(self, tab_name=None):
        if not tab_name:
            tab_name = self.current_tab

        if tab_name:
            if "Undefined" in tab_name:
                self.save_file_as(tab_name)
            elif self.current_file_path:  # If a file is opened
                with open(self.current_file_path, "w") as file:
                    text_widget = self.text_widgets[tab_name]
                    content = text_widget.get(1.0, tk.END)
                    file.write(content)
            else:
                self.save_file_as(tab_name)
        else:
            messagebox.showwarning("Save Error", "Please select a tab to save.")

    def save_file_as(self, tab_name=None):
        if not tab_name:
            tab_name = self.current_tab

        if tab_name:
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{self.current_extension}" if self.current_extension else "",
                filetypes=[(f"{self.current_extension.upper()} files",
                            f"*.{self.current_extension}") if self.current_extension else ("All files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    text_widget = self.text_widgets[tab_name]
                    content = text_widget.get(1.0, tk.END)
                    file.write(content)
                self.current_file_path = file_path  # Update the current file path
                self.update_tab_count(tab_name)

                # If the tab is "Undefined," update the tab label
                if "Undefined" in tab_name:
                    new_tab_name = os.path.basename(file_path)
                    self.notebook.tab(tab_name, text=new_tab_name)
        else:
            messagebox.showwarning("Save Error", "Please select a tab to save.")

    def create_new_tab(self):
        new_tab_name = simpledialog.askstring("New Tab",
                                              "Enter the name for the new tab:",
                                              parent=self.root)
        if new_tab_name:
            language_options = [
                "Python", "HTML", "CSS", "SCSS", "JavaScript", "Undefined"
            ]
            selected_language = simpledialog.askstring(
                "New Tab",
                "Select a language for the new tab:",
                parent=self.root,
                initialvalue="Undefined")

            if selected_language is not None:
                selected_language = selected_language.lower()
                if selected_language not in map(lambda x: x.lower(), language_options):
                    selected_language = ""

            if selected_language:
                auto_detected_extension = selected_language
                if selected_language.lower() == "undefined":
                    selected_language = ""
                    auto_detected_extension = ""

                closeable_tab = CloseableTab(self.notebook)
                text_widget = scrolledtext.ScrolledText(closeable_tab,
                                                        wrap=tk.WORD,
                                                        bg='#282c34',
                                                        fg='white',
                                                        insertbackground='white',
                                                        insertwidth=4,
                                                        padx=10,
                                                        pady=10)
                text_widget.config(font=('helvetica', 12))
                tab_name = f"{new_tab_name} ({auto_detected_extension})"
                closeable_tab.label.config(text=tab_name)
                closeable_tab.pack()
                text_widget.pack(expand="yes", fill="both")
                closeable_tab.text_widget = text_widget

                self.notebook.add(closeable_tab, text=tab_name)
                self.notebook.select(closeable_tab)

                self.text_widgets[tab_name] = text_widget
                self.current_tab = tab_name
                self.current_extension = auto_detected_extension
                self.current_file_path = None  # Set the current file path to None for new tabs

                self.update_tab_count(tab_name)
            else:
                messagebox.showwarning("New Tab Error", "Please select a valid language for the new tab.")

    def update_tab_count(self, selected_tab):
        count = self.tab_counts.get(selected_tab, 0) + 1
        self.tab_counts[selected_tab] = count
        return count

    def new_file(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure("TNotebook", tabposition="n")
    SMIDE = smIDE(root)
    root.mainloop()
