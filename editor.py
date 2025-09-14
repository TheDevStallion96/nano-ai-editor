"""
Editor - Main editor class that coordinates all components
"""

import curses
import os
from text_buffer import TextBuffer
from cursor import Cursor
from display import Display

class Editor:
    """Main editor class that coordinates the text buffer, cursor, and display"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.text_buffer = TextBuffer()
        self.cursor = Cursor()
        self.display = Display(stdscr)
        self.running = True
        self.message = ""  # For status messages
        
    def open_file(self, filename):
        """Open a file for editing"""
        try:
            self.text_buffer.load_file(filename)
            self.cursor.set_position(0, 0)
            self.message = f"Opened {filename}"
        except IOError as e:
            self.message = str(e)
    
    def save_file(self, filename=None):
        """Save the current file"""
        try:
            self.text_buffer.save_file(filename)
            self.message = f"Saved {self.text_buffer.filename}"
        except (IOError, ValueError) as e:
            self.message = str(e)
    
    def handle_key_input(self, key):
        """Handle keyboard input"""
        # Control characters
        if key == 17:  # Ctrl+Q
            self.quit()
        elif key == 19:  # Ctrl+S
            if self.text_buffer.filename:
                self.save_file()
            else:
                self.prompt_save_as()
        elif key == 15:  # Ctrl+O
            self.prompt_open_file()
        
        # Navigation keys
        elif key == curses.KEY_UP:
            self.cursor.move_up(self.text_buffer)
        elif key == curses.KEY_DOWN:
            self.cursor.move_down(self.text_buffer)
        elif key == curses.KEY_LEFT:
            self.cursor.move_left(self.text_buffer)
        elif key == curses.KEY_RIGHT:
            self.cursor.move_right(self.text_buffer)
        elif key == curses.KEY_HOME:
            self.cursor.move_to_line_start()
        elif key == curses.KEY_END:
            self.cursor.move_to_line_end(self.text_buffer)
        elif key == curses.KEY_PPAGE:  # Page Up
            self.page_up()
        elif key == curses.KEY_NPAGE:  # Page Down
            self.page_down()
        
        # Editing keys
        elif key == 10 or key == 13:  # Enter
            row, col = self.text_buffer.insert_line(self.cursor.row, self.cursor.col)
            self.cursor.set_position(row, col)
        elif key == 127 or key == curses.KEY_BACKSPACE:  # Backspace
            row, col = self.text_buffer.backspace_char(self.cursor.row, self.cursor.col)
            self.cursor.set_position(row, col)
        elif key == curses.KEY_DC:  # Delete
            self.text_buffer.delete_char(self.cursor.row, self.cursor.col)
        elif key == 9:  # Tab
            self.insert_tab()
        
        # Regular character input
        elif 32 <= key <= 126:  # Printable ASCII characters
            self.text_buffer.insert_char(self.cursor.row, self.cursor.col, chr(key))
            self.cursor.move_right(self.text_buffer)
        
        # Ensure cursor stays within bounds
        self.cursor.clamp_to_buffer(self.text_buffer)
    
    def insert_tab(self):
        """Insert tab or spaces"""
        # Insert 4 spaces instead of tab for consistent display
        for _ in range(4):
            self.text_buffer.insert_char(self.cursor.row, self.cursor.col, ' ')
            self.cursor.move_right(self.text_buffer)
    
    def page_up(self):
        """Move cursor up by one page"""
        for _ in range(self.display.text_height):
            self.cursor.move_up(self.text_buffer)
    
    def page_down(self):
        """Move cursor down by one page"""
        for _ in range(self.display.text_height):
            self.cursor.move_down(self.text_buffer)
    
    def prompt_save_as(self):
        """Prompt user for filename to save as"""
        filename = self.get_user_input("Save as: ")
        if filename:
            self.save_file(filename)
    
    def prompt_open_file(self):
        """Prompt user for filename to open"""
        if self.text_buffer.modified:
            response = self.get_user_input("File modified. Save first? (y/n): ")
            if response and response.lower().startswith('y'):
                if self.text_buffer.filename:
                    self.save_file()
                else:
                    self.prompt_save_as()
        
        filename = self.get_user_input("Open file: ")
        if filename and os.path.exists(filename):
            self.open_file(filename)
        elif filename:
            self.message = f"File not found: {filename}"
    
    def get_user_input(self, prompt):
        """Get a line of input from the user"""
        # Save current cursor state
        curses.curs_set(1)
        
        # Display prompt at bottom of screen
        status_y = self.display.height - 1
        self.stdscr.move(status_y, 0)
        self.stdscr.clrtoeol()
        self.stdscr.addstr(status_y, 0, prompt)
        self.stdscr.refresh()
        
        # Get input
        curses.echo()
        try:
            user_input = self.stdscr.getstr(status_y, len(prompt)).decode('utf-8')
        except KeyboardInterrupt:
            user_input = ""
        finally:
            curses.noecho()
            curses.curs_set(1)
        
        return user_input.strip()
    
    def quit(self):
        """Quit the editor"""
        if self.text_buffer.modified:
            response = self.get_user_input("File modified. Save before quit? (y/n): ")
            if response and response.lower().startswith('y'):
                if self.text_buffer.filename:
                    self.save_file()
                else:
                    self.prompt_save_as()
        
        self.running = False
    
    def run(self):
        """Main editor loop"""
        while self.running:
            try:
                # Update display size in case terminal was resized
                self.display.update_size()
                
                # Render everything
                self.display.render_all(self.text_buffer, self.cursor)
                
                # Show any status message
                if self.message:
                    # Temporarily show message in status bar
                    status_y = self.display.height - 1
                    self.stdscr.move(status_y, 0)
                    self.stdscr.clrtoeol()
                    if curses.has_colors():
                        self.stdscr.addstr(status_y, 0, self.message[:self.display.width], 
                                         curses.color_pair(1))
                    else:
                        self.stdscr.addstr(status_y, 0, self.message[:self.display.width], 
                                         curses.A_REVERSE)
                    self.stdscr.refresh()
                    
                    # Wait for any key to clear message
                    self.stdscr.getch()
                    self.message = ""
                    continue
                
                # Get user input
                key = self.stdscr.getch()
                
                # Handle the key
                self.handle_key_input(key)
                
            except KeyboardInterrupt:
                self.quit()
            except curses.error:
                # Ignore curses errors (like screen size issues)
                pass