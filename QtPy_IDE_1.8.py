import os
import webbrowser
from PyQt5.QtGui import QIcon, QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QFileDialog, QMessageBox, QTextEdit,
    QVBoxLayout, QWidget, QTabWidget, QPushButton, QLabel, QSlider ,QScrollArea, QInputDialog,
    QGridLayout, QLineEdit, QSplitter
)
from PyQt5.QtCore import Qt

class QtPy(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set dark mode style
        self.set_style_dark()

        self.setWindowTitle("QtPy IDE 1.8")
        self.setGeometry(100, 100, 1350, 750)
        self.tab_counts = {}
        self.current_extension = ""
        self.current_tab = None
        self.current_file_path = None
        self.directory_path = None
        self.previous_directories = []
        self.next_directories = []

        self.initUI()

    def initUI(self):
        self.return_button = QPushButton("Return To The Previous Directory")
        self.return_button.clicked.connect(self.return_to_previous_directory)
        self.return_button.setVisible(True)  # Initially hide the button
        self.return_button.setMaximumWidth(169)

        self.next_button = QPushButton("Go To The Next Directory")
        self.next_button.clicked.connect(self.return_to_next_directory)
        self.next_button.setVisible(True)  # Initially hide the button

        self.create_menu()
        self.create_toolbar()
        self.create_notebook()
        self.create_directory_opener()

        self.search_box = QLineEdit()
        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search)
        self.search_button.setMaximumWidth(120)
        self.search_button.setMinimumWidth(120)

        central_widget_layout = QGridLayout()
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.addWidget(self.scroll_area)

    # Adjust column span for the buttons to bring them closer
        central_widget_layout.addWidget(self.return_button, 0, 0, 1, 1)
        central_widget_layout.addWidget(self.next_button, 0, 1, 1, 1)

        central_widget_layout.addWidget(self.splitter, 1, 0, 1, 2)
        central_widget_layout.addWidget(self.search_box, 2, 0, 1, 1)
        central_widget_layout.addWidget(self.search_button, 2, 1, 1, 1)

        central_widget = QWidget()
        central_widget.setLayout(central_widget_layout)
        self.setCentralWidget(central_widget)

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')

        openAct = QAction(QIcon('icons/open.png'), 'Open', self)
        openAct.triggered.connect(self.open_file)
        file_menu.addAction(openAct)

        saveAct = QAction(QIcon('icons/save.png'), 'Save', self)
        saveAct.triggered.connect(self.save_file)
        file_menu.addAction(saveAct)

        saveAsAct = QAction(QIcon('icons/save_as.png'), 'Save As', self)
        saveAsAct.triggered.connect(self.save_file_as)
        file_menu.addAction(saveAsAct)

        exitAct = QAction(QIcon('icons/exit.png'), 'Exit', self)
        exitAct.triggered.connect(self.close)
        file_menu.addAction(exitAct)

        run_menu = menu_bar.addMenu('Run')
        runAct = QAction(QIcon('icons/run.png'), 'Run (html)', self)
        runAct.triggered.connect(self.run_file)
        run_menu.addAction(runAct)

    def create_toolbar(self):
        self.toolbar = self.addToolBar('Toolbar')

        plus_button = QAction('Create New Tab', self)
        plus_button.triggered.connect(self.create_new_tab)
        self.toolbar.addAction(plus_button)

        close_all_button = QAction('Close All Tabs', self)
        close_all_button.triggered.connect(self.close_all_tabs)
        self.toolbar.addAction(close_all_button)

        openAct = QAction('Open', self)
        openAct.triggered.connect(self.open_file)
        self.toolbar.addAction(openAct)

        saveAct = QAction('Save', self)
        saveAct.triggered.connect(self.save_file)
        self.toolbar.addAction(saveAct)

        saveAsAct = QAction('Save As', self)
        saveAsAct.triggered.connect(self.save_file_as)
        self.toolbar.addAction(saveAsAct)

        open_directory_button = QAction('Open Directory', self)
        open_directory_button.triggered.connect(self.open_directory)
        self.toolbar.addAction(open_directory_button)

        label = QLabel("Text Size:")
        self.toolbar.addWidget(label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)  # Set minimum font size
        self.slider.setMaximum(40)  # Set maximum font size
        self.slider.setValue(12)  # Set initial font size
        self.toolbar.addWidget(self.slider)
        self.slider.setMaximumWidth(100)

        # Connect slider valueChanged signal to change_font_size slot
        self.slider.valueChanged.connect(self.change_font_size)

    def create_notebook(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)  # Allow closing tabs
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

    def change_font_size(self, size):
        # Slot to change the font size of the text
        font = self.tab_widget.font()
        font.setPointSize(size)
        self.tab_widget.setFont(font)

    def create_directory_opener(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

    def open_directory(self):
        self.directory_path = QFileDialog.getExistingDirectory(self, 'Open Directory')
        if self.directory_path:
            self.previous_directories.append(self.directory_path)
            self.return_button.setVisible(True)  # Show the return button
            self.refresh_file_list()

    def refresh_file_list(self):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        file_list = []
        folder_list = []
        if self.directory_path:
            entries = os.listdir(self.directory_path)
            for entry in entries:
                entry_path = os.path.join(self.directory_path, entry)
                if os.path.isfile(entry_path):
                    file_list.append(entry)
                elif os.path.isdir(entry_path):
                    folder_list.append(entry)

        for folder_name in folder_list:
            folder_button = QPushButton(folder_name + "  (Folder)")
            folder_button.clicked.connect(lambda checked, name=folder_name: self.open_folder_confirmation(name))
            self.scroll_layout.addWidget(folder_button)

        for file_name in file_list:
            file_button = QPushButton(file_name)
            file_button.clicked.connect(lambda checked, name=file_name: self.open_selected_file(name))
            self.scroll_layout.addWidget(file_button)

    def open_folder(self, folder_name):
        folder_path = os.path.join(self.directory_path, folder_name)
        self.previous_directories.append(self.directory_path)  # Add current directory to previous_directories
        self.directory_path = folder_path
        self.refresh_file_list()

    def open_selected_file(self, file_name):
        file_path = os.path.join(self.directory_path, file_name)
        tab_name, ok = QInputDialog.getText(self, 'Open File', f"In which tab do you want to open '{file_name}'?")
        if ok:
            # Get the index of the tab
            index = self.tab_widget.currentIndex()
            # If the tab already exists, remove it
            if index != -1:
                self.tab_widget.removeTab(index)
            # Load the file into the selected tab
            text_edit = QTextEdit()
            text_edit.setPlainText(open(file_path).read())
            self.tab_widget.addTab(text_edit, tab_name)
            self.current_tab = tab_name
            self.current_file_path = file_path  # Set current_file_path when opening a file

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File')
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                text_edit = QTextEdit()
                text_edit.setPlainText(content)
                self.tab_widget.addTab(text_edit, os.path.basename(file_path))
                self.current_file_path = file_path
                self.current_tab = os.path.basename(file_path)

    def save_file(self):
        if not self.current_tab:
            QMessageBox.warning(self, "Save Error", "Please select a tab to save.")
            return

        for index in range(self.tab_widget.count()):
            if self.tab_widget.tabText(index) == self.current_tab:
                text_edit = self.tab_widget.widget(index)
                content = text_edit.toPlainText()
                if self.current_file_path:
                    with open(self.current_file_path, 'w') as file:
                        file.write(content)
                    self.remove_unsaved_indicator()
                else:
                    self.save_file_as()

    def save_file_as(self):
        if not self.current_tab:
            QMessageBox.warning(self, "Save Error", "Please select a tab to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'All files (*)')  # Change the filter here
        if file_path:
            for index in range(self.tab_widget.count()):
                if self.tab_widget.tabText(index) == self.current_tab:
                    text_edit = self.tab_widget.widget(index)
                    content = text_edit.toPlainText()
                    with open(file_path, 'w') as file:
                        file.write(content)
                    self.current_file_path = file_path
                    self.remove_unsaved_indicator()

    def run_file(self):
        if not self.directory_path:
            QMessageBox.warning(self, "Run Error", "Please open a directory first.")
            return

        selected_file, _ = QInputDialog.getText(self, 'Run File', 'Enter the file name to run:')
        if selected_file:
            file_path = os.path.join(self.directory_path, selected_file)
            _, file_extension = os.path.splitext(selected_file)
            if file_extension.lower() == '.html':
                webbrowser.open(file_path, new=2)  # Open HTML files in the default web browser
            elif file_extension.lower() == '.py':
                QMessageBox.information(self, "Run Info", "You need to run Python files manually.")
            else:
                QMessageBox.warning(self, "Run Error", f"Unsupported file type: {file_extension}")

    def create_new_tab(self):
        tab_name, ok = QInputDialog.getText(self, 'New Tab', 'Enter the name for the new tab:')
        if ok:
            text_edit = QTextEdit()
            self.tab_widget.addTab(text_edit, tab_name + "*")  # Add '*' for new tabs
            self.current_tab = tab_name + "*"

    def search(self):
        self.query = self.search_box.text()  # Define query as an instance variable
        if self.query:
            url = f"https://search.brave.com/search?q={self.query}"
            webbrowser.open(url)
        else:
            QMessageBox.warning(self, 'Warning', 'Please enter a search query.')

    def close_all_tabs(self):
        self.tab_widget.clear()

    def close_tab(self, index):
        self.tab_widget.removeTab(index)

    def close_directory(self):
        self.scroll_layout.removeWidget(self.directory_button)
        self.directory_button.deleteLater()
        self.create_directory_opener()

    def remove_unsaved_indicator(self):
        for index in range(self.tab_widget.count()):
            if self.tab_widget.tabText(index).endswith("*"):
                new_name = self.tab_widget.tabText(index)[:-1]
                self.tab_widget.setTabText(index, new_name)

    def update_tab_counts(self):
        current_count = self.tab_widget.count()
        self.tab_counts[current_count] = current_count

    def set_style_dark(self):
        dark_palette = self.get_dark_palette()
        QApplication.setStyle("Fusion")
        QApplication.setPalette(dark_palette)

    def get_dark_palette(self):
        dark_palette = QPalette()

        # Dark Color
        dark_color = QColor(51, 51, 51)
        dark_palette.setColor(QPalette.Window, dark_color)
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(34, 34, 34))
        dark_palette.setColor(QPalette.AlternateBase, dark_color)
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, dark_color)
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        return dark_palette

    def return_to_previous_directory(self):
        if self.previous_directories:
            previous_directory = self.previous_directories.pop()
            if not self.previous_directories:  # Hide the return button if no previous directory left
                self.return_button.setVisible(False)
            self.next_directories.append(self.directory_path)  # Add current directory to next_directories
            self.directory_path = previous_directory
            self.refresh_file_list()
            self.next_button.setVisible(True)  # Show the next button

    def return_to_next_directory(self):
        if self.next_directories:
            next_directory = self.next_directories.pop()
            if not self.next_directories:  # Hide the next button if no next directory left
                self.next_button.setVisible(False)
            self.previous_directories.append(self.directory_path)  # Add current directory to previous_directories
            self.directory_path = next_directory
            self.refresh_file_list()
            self.return_button.setVisible(True)  # Show the return button

    def open_folder(self, folder_name):
        folder_path = os.path.join(self.directory_path, folder_name)
        self.directory_path = folder_path
        self.previous_directories.append(self.directory_path)
        self.refresh_file_list()

    def open_folder_confirmation(self, folder_name):
        confirmation = QMessageBox.question(self, 'Confirmation', f"Do you want to open the folder '{folder_name}'?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            self.open_folder(folder_name)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ex = QtPy()
    ex.show()
    sys.exit(app.exec_())
