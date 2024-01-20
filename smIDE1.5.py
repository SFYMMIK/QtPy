import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, simpledialog, END
import webbrowser
from time import strftime
import os

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

class smIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("smIDE 1.5")
        self.root.geometry("1350x750")
        self.root.option_add('*Font', 'helvetica 11')

        self.create_menu()
        self.create_notebook()
        self.create_toolbar()
        self.create_clock()
        self.create_directory_opener()

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

        run_menu = tk.Menu(menu_bar, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_file)
        menu_bar.add_cascade(label="Run", menu=run_menu)

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
        html_tags_button = ttk.Button(toolbar, text="HTML Tags", command=self.show_html_tags)

        new_button.pack(side=tk.LEFT, padx=5)
        open_button.pack(side=tk.LEFT, padx=5)
        save_button.pack(side=tk.LEFT, padx=5)
        plus_button.pack(side=tk.LEFT, padx=5)
        html_tags_button.pack(side=tk.LEFT, padx=5)

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def create_clock(self):
        clock_label = ttk.Label(self.root, text="", font=('helvetica', 12))
        clock_label.pack(side=tk.RIGHT, padx=10, pady=5)
        self.update_clock(clock_label)

    def update_clock(self, label):
        time_string = strftime('%H:%M:%S')
        label.config(text=time_string)
        self.root.after(1000, lambda: self.update_clock(label))  # Update every 1000ms (1 second)

    def create_directory_opener(self):
        directory_button = ttk.Button(self.root, text="Open Directory", command=self.open_directory)
        directory_button.pack(side=tk.RIGHT, padx=10, pady=5)
        self.file_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, exportselection=0)
        self.file_listbox.pack(side=tk.RIGHT, padx=10, pady=5)
        self.file_listbox.bind("<Double-Button-1>", self.open_selected_file)
        self.directory_path = None  # Add this line to store the directory path

    def open_directory(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            file_list = [f for f in os.listdir(self.directory_path) if os.path.isfile(os.path.join(self.directory_path, f))]
            self.file_listbox.delete(0, tk.END)
            for file_name in file_list:
                self.file_listbox.insert(tk.END, file_name)

    def open_selected_file(self, event):
        if self.directory_path:
            selected_index = self.file_listbox.curselection()
            if selected_index:
                selected_file = self.file_listbox.get(selected_index)
                file_path = os.path.join(self.directory_path, selected_file)
                tab_name = simpledialog.askstring("Open File", f"In which tab do you want to open '{selected_file}'?")
                if tab_name and tab_name in self.text_widgets:
                    text_widget = self.text_widgets[tab_name]
                    with open(file_path, "r") as file:
                        content = file.read()
                        text_widget.delete(1.0, tk.END)
                        text_widget.insert(tk.END, content)
                    self.current_file_path = file_path
                    self.notebook.select(tab_name)
                    self.save_file(tab_name)

    def create_file_selector(self, directory_path, file_list):
        selector_window = tk.Toplevel(self.root)
        selector_window.title("Select a File")

        for file_name in file_list:
            button = ttk.Button(selector_window, text=file_name,
                                command=lambda name=file_name: self.ask_tab_for_file(directory_path, name))
            button.pack(pady=5)

    def ask_tab_for_file(self, directory_path, file_name):
        file_path = os.path.join(directory_path, file_name)
        tab_name = simpledialog.askstring("Open File", f"In which tab do you want to open '{file_name}'?")
        if tab_name and tab_name in self.text_widgets:
            text_widget = self.text_widgets[tab_name]
            with open(file_path, "r") as file:
                content = file.read()
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, content)
            self.current_file_path = file_path
            self.notebook.select(tab_name)
            self.save_file(tab_name)

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
                return closeable_tab  # Return the reference to the new tab
            else:
                messagebox.showwarning("New Tab Error", "Please select a valid language for the new tab.")
                return None

    def update_tab_count(self, selected_tab):
        count = self.tab_counts.get(selected_tab, 0) + 1
        self.tab_counts[selected_tab] = count
        return count

    def new_file(self):
        pass

    def run_file(self):
        if not self.directory_path:
            messagebox.showwarning("Run Error", "Please open a directory first.")
            return

        selected_file = simpledialog.askstring("Run File", "Enter the file name to run:")
        if not selected_file:
            return

        file_path = os.path.join(self.directory_path, selected_file)
        _, file_extension = os.path.splitext(selected_file)

        if file_extension.lower() == '.html':
            webbrowser.open(file_path, new=2)  # Open HTML files in the default web browser
        elif file_extension.lower() == '.py':
            messagebox.showinfo("Run Info", "You need to run Python files manually.")
        else:
            messagebox.showwarning("Run Error", f"Unsupported file type: {file_extension}")

    def show_html_tags(self):
        html_tags_window = tk.Toplevel(self.root)
        html_tags_window.title("HTML Keyword Help")

        html_tags_text = tk.Text(html_tags_window, wrap=tk.WORD, height=20, width=60)
        html_tags_text.pack(padx=10, pady=10, fill="both", expand=True)

        html_tags_text.insert(tk.END, """
            <html>
                <head>
                    <title>This is the title</title>
                </head>
                <body>
                    <h1>This is a heading</h1>
                    <p>This is a paragraph.</p>
                    <a href="https://www.example.com">This is a link</a>
                    <img src="image.jpg" alt="Image Alt Text">
                    <ul>
                        <li>Item 1</li>
                        <li>Item 2</li>
                        <li>Item 3</li>
                    </ul>
                    <ol>
                        <li>Item 1</li>
                        <li>Item 2</li>
                        <li>Item 3</li>
                    </ol>
                    <span style="color: red;">This is a red span</span>
                    <div style="background-color: #e0e0e0; padding: 10px;">This is a div with a gray background</div>
                    <input type="text" placeholder="Enter text">
                    <select>
                        <option value="option1">Option 1</option>
                        <option value="option2">Option 2</option>
                        <option value="option3">Option 3</option>
                    </select>
                    <textarea rows="4" cols="50">This is a textarea</textarea>
                    <strong>This text is strong</strong>
                    <em>This text is emphasized</em>
                    <pre>This is preformatted text</pre>
                    <code>This is code</code>
                    <hr>
                    <br>
                    <table border="1">
                        <tr>
                            <td>Row 1, Cell 1</td>
                            <td>Row 1, Cell 2</td>
                        </tr>
                        <tr>
                            <td>Row 2, Cell 1</td>
                            <td>Row 2, Cell 2</td>
                        </tr>
                    </table>
                </body>
            </html>
        """)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure("TNotebook", tabposition="n")
    SMIDE = smIDE(root)
    root.mainloop()
