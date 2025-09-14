# Terminal Text Editor

A feature-rich terminal-based text editor built with Python and curses, similar to nano but with additional functionality including search/replace, clipboard operations, and text selection.

## Features

### Basic Editing
- Text insertion and deletion
- Line creation and joining
- Multi-line editing support
- Automatic scrolling
- Line numbers display
- Status bar with file info and cursor position

### File Operations
- Open existing files
- Create new files
- Save files (with Save As support)
- Modified file detection
- Quit with unsaved changes protection

### Navigation
- Arrow key navigation
- Home/End for line start/end
- Page Up/Down for scrolling
- Go to specific line number
- Word-by-word navigation (Ctrl+Left/Right - coming soon)

### Text Selection
- Manual selection mode (Ctrl+P to start/end)
- Select all text (Ctrl+A)
- Visual selection highlighting
- Selection info in status bar

### Clipboard Operations
- Copy selected text (Ctrl+C)
- Cut selected text (Ctrl+X)
- Paste from clipboard (Ctrl+V)
- Automatic line operations when no selection

### Search and Replace
- Text search with case sensitivity options
- Find next/previous occurrences
- Replace single occurrence
- Replace all occurrences
- Search result highlighting

### Advanced Features
- Tab insertion (4 spaces)
- Selection-based indentation
- Multiple file format support
- Terminal resizing support
- Color support (when available)

## Installation

1. Ensure you have Python 3.6+ installed
2. Download all the Python files to a directory
3. Make the main script executable (optional):
   ```bash
   chmod +x main.py
   ```

## Usage

### Starting the Editor

```bash
# Create a new file
python3 main.py

# Open an existing file
python3 main.py filename.txt

# Make executable and run directly (Linux/Mac)
./main.py filename.txt
```

### Key Bindings

#### File Operations
- **Ctrl+N**: New file
- **Ctrl+O**: Open file
- **Ctrl+S**: Save file
- **Ctrl+Q**: Quit editor

#### Navigation
- **Arrow Keys**: Move cursor
- **Home**: Move to line start
- **End**: Move to line end
- **Page Up/Down**: Scroll by screen
- **Ctrl+G**: Go to line number

#### Editing
- **Enter**: New line
- **Backspace**: Delete character before cursor
- **Delete**: Delete character at cursor
- **Tab**: Insert 4 spaces (or indent selection)

#### Selection and Clipboard
- **Ctrl+P**: Start/end selection mode
- **Ctrl+A**: Select all text
- **Ctrl+C**: Copy selection (or current line)
- **Ctrl+X**: Cut selection (or current line)
- **Ctrl+V**: Paste from clipboard

#### Search and Replace
- **Ctrl+F**: Search for text
- **F3**: Find next occurrence
- **Ctrl+R**: Replace text

### Selection Mode

1. Press **Ctrl+P** to start selection
2. Use arrow keys to extend selection
3. Press **Ctrl+P** again to end selection
4. Use **Ctrl+C** or **Ctrl+X** to copy/cut selected text

### Search Functionality

1. Press **Ctrl+F** to start search
2. Enter search term
3. Use **F3** to find next occurrence
4. Selected text will be highlighted

### Replace Functionality

1. Press **Ctrl+R** to start replace
2. Enter search term
3. Enter replacement text
4. Choose single replace or replace all

## File Structure

```
editor/
├── main.py              # Entry point and curses initialization
├── editor.py            # Main editor coordination class
├── text_buffer.py       # Text content and file operations
├── cursor.py            # Cursor movement and positioning
├── display.py           # Screen rendering and UI
├── search.py            # Search and replace functionality
├── clipboard.py         # Cut, copy, and paste operations
├── selection.py         # Text selection management
└── README.md           # This documentation
```

## Advanced Usage

### Search Options
- Case-sensitive search (configurable in search.py)
- Regular expression support (configurable)
- Wrap-around search behavior

### Clipboard Behavior
- Copy/cut with no selection operates on current line
- Multi-line clipboard support
- Paste replaces selected text if selection exists

### Status Bar Information
- Current filename and modification status
- Cursor position (line and column)
- Selection information when active
- Help messages and operation feedback

## Extending the Editor

The editor is designed with modularity in mind. Each component can be extended:

- **Syntax Highlighting**: Add to display.py
- **Multiple Tabs**: Extend editor.py
- **Plugin System**: Create new modules
- **Custom Key Bindings**: Modify editor.py key handling
- **Themes**: Extend color support in display.py

## Troubleshooting

### Common Issues

1. **Terminal too small**: Ensure terminal is at least 80x24 characters
2. **Key not working**: Some terminals may handle special keys differently
3. **Colors not showing**: Ensure terminal supports color
4. **File permissions**: Check read/write permissions for files

### Terminal Compatibility

Tested on:
- Linux terminals (gnome-terminal, konsole, xterm)
- macOS Terminal
- Windows WSL
- tmux/screen sessions

## Future Enhancements

- Syntax highlighting for common languages
- Multiple file tabs
- Plugin system
- Configuration file support
- Mouse support
- Undo/redo functionality
- Auto-save features
- Code folding

## Contributing

This editor serves as a foundation for a more advanced editor. Contributions and improvements are welcome!

## License

This project is provided as-is for educational and practical use.