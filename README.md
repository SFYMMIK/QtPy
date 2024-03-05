![Logo](logo.png)

# QtPy IDE Overview

## Introduction
QtPy IDE is a lightweight Integrated Development Environment (IDE) developed in Python using the PyQt5 library. It offers a simple and intuitive interface for coding in various programming languages.

## Features
- **Tabbed Interface:** Easily manage and switch between multiple files with a tabbed interface.
- **File Operations:** Create, open, save, and save as files effortlessly.
- **Dynamic Tabs:** Tabs dynamically update based on the selected tab and file name.
- **Browser Preview:** View HTML files directly in your default web browser.

## Windows
- **Just Install the .exe and open it**

## Linux
1. **download the 'QtPy_IDE_1.6'**
2. **Then Place It In Your Desired Directory**
3. **Make It Actually Executable, Example:**
   ```shell
   sfymmik@SFYM ~ $ cd /Path/To/Your/Directory
   ```
   ```shell
   sfymmik@SFYM ~/home/sfymmik/Path/To/Your/Direcotry $ chmod +x QtPy_IDE_1.6
   ```
   ```shell
   sfymmik@SFYM ~/home/sfymmik/Path/To/Your/Direcotry $ ./QtPy_IDE_1.6
   ```
4. **After That You Can Use QtPy IDE!**

## Usage (QtPy)

1. **Open/Save:**
   - Open existing files and edit them in the chosen tab.
   - Save updates or use 'Save As' to create a new file from the current one.

2. **Create New Tab:**
   - Click "+ Create New Tab +" to create a new tab.
   - Choose a name
   - And code!

3. **Close Tabs:**
   - Click the 'x' button on a tab. Confirm to close.

4. **Browser Preview:**
   - Run HTML files to view them directly in your default web browser when clicking the 'Run' button.

## Feedback and Support
For feedback, suggestions, or support, visit [official website](https://sfymmik.web.fc2.com) or contact on Discord: ball_sx.

Thank you for using QtPy IDE!

---

## Code Overview

### Classes
- `QtPy`: Main class for the QtPy IDE application, providing file management and UI functionalities.

### Functions
- `create_menu`: Creates menu bar for file operations and running files.
- `create_toolbar`: Sets up toolbar with buttons for file operations and HTML tags display.
- `create_notebook`: Initializes tabbed notebook for programming languages.
- `create_directory_opener`: Creates button to open a directory and list files.
- `open_directory`: Opens directory and populates the file list.
- `refresh_file_list`: Refreshes the file list displayed in the directory opener.
- `open_selected_file`: Opens selected file from file list in chosen tab.
- `open_file`: Opens existing file and displays content in current tab.
- `save_file`: Saves content of current tab to a file.
- `save_file_as`: Saves content of current tab with new name or extension.
- `run_file`: Runs a selected file, opening HTML files in the default web browser.
- `create_new_tab`: Creates a new tab with a specified name and language.
- `search`: Performs a web search based on the entered query.
- `close_all_tabs`: Closes all tabs in the IDE.
- `close_tab`: Closes the selected tab.
- `close_directory`: Closes the currently opened directory.
- `remove_unsaved_indicator`: Removes the unsaved indicator from tab names.
- `update_tab_counts`: Updates the count of tabs.
- `set_style_dark`: Sets the dark mode style for the IDE.
- `get_dark_palette`: Returns a dark color palette for the dark mode.

### Main Section
- Initializes the application, sets up UI elements, and runs the main event loop.
