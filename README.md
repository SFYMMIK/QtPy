![Logo](logo.png)

# smIDE Overview

## Introduction
smIDE is a lightweight Integrated Development Environment (IDE) developed in Python using the Tkinter library. It offers a simple and intuitive interface for coding in various programming languages, including HTML, CSS, SCSS, JavaScript, and Python. smIDE supports undefined tabs, allowing flexibility for any language.

## Features
- **Tabbed Interface:** Easily manage and switch between multiple files with a tabbed interface.
- **File Operations:** Create, open, save, and save as files effortlessly.
- **Dynamic Tabs:** Tabs dynamically update based on the selected language and file name.
- **Browser Preview:** View HTML files directly in your default web browser.

## Usage
1. **New File:**
   - Click on any tab to create a new file. Save using the save button.

2. **Open/Save:**
   - Open existing files and edit them in the chosen tab.
   - Save updates or use 'Save As' to create a new file from the current one.

3. **Add New Tab:**
   - Click "+ add Tab +" to create a new tab.
   - Choose a name and language (or leave as 'Undefined' for 'All Files').

4. **Close Tabs:**
   - Click the 'x' button on a tab. Confirm to close.

5. **Browser Preview:**
   - Run HTML files to view them directly in your default web browser.

## Feedback and Support
For feedback, suggestions, or support, visit [official website](https://sfymmik.web.fc2.com) or contact on Discord: ball_sx.

Thank you for using smIDE!

---

## Code Overview

### Classes
- `CloseableTab`: Represents a closeable tab with a close button.
- `smIDE`: Main class for the smIDE application, providing file management and UI functionalities.

### Functions
- `create_menu`: Creates menu bar for file operations and running files.
- `create_notebook`: Initializes tabbed notebook for programming languages.
- `create_toolbar`: Sets up toolbar with buttons for file operations and HTML tags display.
- `create_clock`: Displays a clock in the top-right corner.
- `update_clock`: Updates displayed time every second.
- `create_directory_opener`: Creates button to open a directory and list files.
- `open_directory`: Opens directory and populates the file list.
- `open_selected_file`: Opens selected file from file list in chosen tab.
- `create_file_selector`: Creates window to select a file from a list.
- `ask_tab_for_file`: Asks user in which tab to open a selected file.
- `on_tab_selected`: Handles event when a tab is selected.
- `open_file`: Opens existing file and displays content in current tab.
- `save_file`: Saves content of current tab to a file.
- `save_file_as`: Saves content of current tab with new name or extension.
- `create_new_tab`: Creates a new tab with a specified name and language.
- `update_tab_count`: Updates count of tabs.
- `new_file`: Placeholder function for creating a new file.
- `run_file`: Runs a selected file, opening HTML files in the default web browser.
- `show_html_tags`: Displays a window with example HTML code.

### Main Section
- Initializes Tkinter root window, sets notebook style, and creates an instance of the smIDE class.
- Runs Tkinter main loop.
