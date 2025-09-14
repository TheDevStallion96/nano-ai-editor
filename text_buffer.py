"""
TextBuffer - Manages the text content and file operations
"""

import os

class TextBuffer:
    """Manages the text content of the file being edited"""
    
    def __init__(self):
        self.lines = ['']  # Start with one empty line
        self.filename = None
        self.modified = False
        
    def load_file(self, filename):
        """Load a file into the buffer"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                if content:
                    # Split into lines, preserving empty lines
                    self.lines = content.splitlines()
                    # Ensure we have at least one line
                    if not self.lines:
                        self.lines = ['']
                else:
                    self.lines = ['']
                    
            self.filename = filename
            self.modified = False
            return True
        except IOError as e:
            raise IOError(f"Could not load file {filename}: {e}")
    
    def save_file(self, filename=None):
        """Save the buffer to a file"""
        if filename:
            self.filename = filename
        
        if not self.filename:
            raise ValueError("No filename specified")
        
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                # Join lines with newlines
                content = '\n'.join(self.lines)
                f.write(content)
            
            self.modified = False
            return True
        except IOError as e:
            raise IOError(f"Could not save file {self.filename}: {e}")
    
    def insert_char(self, row, col, char):
        """Insert a character at the specified position"""
        if row >= len(self.lines):
            # Extend lines if necessary
            while len(self.lines) <= row:
                self.lines.append('')
        
        line = self.lines[row]
        # Insert character at column position
        self.lines[row] = line[:col] + char + line[col:]
        self.modified = True
    
    def delete_char(self, row, col):
        """Delete character at the specified position"""
        if row >= len(self.lines) or col >= len(self.lines[row]):
            return False
        
        line = self.lines[row]
        if col < len(line):
            self.lines[row] = line[:col] + line[col + 1:]
            self.modified = True
            return True
        return False
    
    def backspace_char(self, row, col):
        """Delete character before the cursor"""
        if col > 0:
            # Delete character before cursor
            line = self.lines[row]
            self.lines[row] = line[:col-1] + line[col:]
            self.modified = True
            return row, col - 1
        elif row > 0:
            # Join with previous line
            prev_line = self.lines[row - 1]
            current_line = self.lines[row]
            self.lines[row - 1] = prev_line + current_line
            del self.lines[row]
            self.modified = True
            return row - 1, len(prev_line)
        
        return row, col
    
    def insert_line(self, row, col):
        """Insert a new line at the cursor position"""
        if row >= len(self.lines):
            self.lines.append('')
            self.modified = True
            return row + 1, 0
        
        line = self.lines[row]
        # Split the current line at cursor position
        self.lines[row] = line[:col]
        self.lines.insert(row + 1, line[col:])
        self.modified = True
        return row + 1, 0
    
    def get_line_count(self):
        """Get the total number of lines"""
        return len(self.lines)
    
    def get_line(self, row):
        """Get a specific line by row number"""
        if 0 <= row < len(self.lines):
            return self.lines[row]
        return ""
    
    def get_line_length(self, row):
        """Get the length of a specific line"""
        if 0 <= row < len(self.lines):
            return len(self.lines[row])
        return 0
    
    def is_empty(self):
        """Check if the buffer is empty"""
        return len(self.lines) == 1 and self.lines[0] == ""