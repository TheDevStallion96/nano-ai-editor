"""
Display - Manages screen rendering and UI layout
"""

import curses
import os

class Display:
    """Manages the terminal display and rendering"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.scroll_offset = 0
        self.line_number_width = 4
        self.show_line_numbers = True
        self.start_y = 0
        self.start_x = 0
        
        # Calculate usable areas
        self.text_start_col = self.line_number_width if self.show_line_numbers else 0
        self.text_width = self.width - self.text_start_col
        self.text_height = self.height - 1  # Reserve bottom line for status
        
    def update_size(self):
        """Update display size (call when terminal is resized)"""
        self.height, self.width = self.stdscr.getmaxyx()
        self.text_start_col = self.line_number_width if self.show_line_numbers else 0
        self.text_width = self.width - self.text_start_col
        self.text_height = self.height - 1
    
    def scroll_if_needed(self, cursor):
        """Adjust scroll offset to keep cursor visible"""
        # Vertical scrolling
        if cursor.row < self.scroll_offset:
            self.scroll_offset = cursor.row
        elif cursor.row >= self.scroll_offset + self.text_height:
            self.scroll_offset = cursor.row - self.text_height + 1
        
        # Ensure scroll offset is not negative
        self.scroll_offset = max(0, self.scroll_offset)
    
    def render_line_numbers(self, text_buffer):
        """Render line numbers on the left side"""
        if not self.show_line_numbers:
            return
        
        start_line = self.scroll_offset
        end_line = min(start_line + self.text_height, text_buffer.get_line_count())
        
        for i in range(self.text_height):
            line_num = start_line + i + 1
            y_pos = i
            
            if line_num <= text_buffer.get_line_count():
                # Format line number
                line_str = f"{line_num:3d} "
                try:
                    if curses.has_colors():
                        self.stdscr.addstr(y_pos, 0, line_str, curses.color_pair(2))
                    else:
                        self.stdscr.addstr(y_pos, 0, line_str)
                except curses.error:
                    pass  # Ignore errors at screen edges
    
    def render_text(self, text_buffer, cursor):
        """Render the text content"""
        start_line = self.scroll_offset
        end_line = min(start_line + self.text_height, text_buffer.get_line_count())
        
        for i in range(self.text_height):
            line_index = start_line + i
            y_pos = i
            
            # Clear the line first
            try:
                self.stdscr.move(y_pos, self.text_start_col)
                self.stdscr.clrtoeol()
            except curses.error:
                pass
            
            if line_index < text_buffer.get_line_count():
                line_text = text_buffer.get_line(line_index)
                
                # Truncate line if it's too long for screen
                if len(line_text) > self.text_width:
                    line_text = line_text[:self.text_width]
                
                try:
                    self.stdscr.addstr(y_pos, self.text_start_col, line_text)
                except curses.error:
                    pass  # Ignore errors at screen edges
    
    def render_status_bar(self, text_buffer, cursor):
        """Render the status bar at the bottom"""
        status_y = self.height - 1
        
        # Clear status line
        try:
            self.stdscr.move(status_y, 0)
            self.stdscr.clrtoeol()
        except curses.error:
            pass
        
        # Prepare status text
        # Get relative path from user's home directory to the current file
        home_dir = os.path.expanduser("~")
        if text_buffer.filename:
            abs_path = os.path.abspath(text_buffer.filename)
            try:
                rel_path = os.path.relpath(abs_path, home_dir)
            except ValueError:
                rel_path = abs_path
        else:
            rel_path = "[New File]"
        filename = text_buffer.filename or "[New File]"
        modified = "*" if text_buffer.modified else ""
        position = f"Line {cursor.row + 1}, Col {cursor.col + 1}"
        
        # Create status line
        left_status = f"{rel_path}{modified}"
        right_status = position
        
        # Calculate spacing
        available_width = self.width
        spacing = available_width - len(left_status) - len(right_status)
        
        if spacing > 0:
            status_line = left_status + " " * spacing + right_status
        else:
            # Truncate filename if too long
            max_filename_len = available_width - len(right_status) - 5
            if len(left_status) > max_filename_len:
                left_status = left_status[:max_filename_len] + "..."
            status_line = left_status + " " + right_status
        
        # Render status bar with highlighting
        try:
            if curses.has_colors():
                self.stdscr.addstr(status_y, 0, status_line[:self.width], 
                                 curses.color_pair(1))
            else:
                self.stdscr.addstr(status_y, 0, status_line[:self.width], 
                                 curses.A_REVERSE)
        except curses.error:
            pass
    
    def render_help_line(self):
        """Render help text at the bottom"""
        help_text = "^S Save  ^Q Quit  ^O Open  ^F Find"
        status_y = self.height - 1
        
        try:
            self.stdscr.move(status_y, 0)
            self.stdscr.clrtoeol()
            if curses.has_colors():
                self.stdscr.addstr(status_y, 0, help_text[:self.width], 
                                 curses.color_pair(1))
            else:
                self.stdscr.addstr(status_y, 0, help_text[:self.width], 
                                 curses.A_REVERSE)
        except curses.error:
            pass
    
    def position_cursor(self, cursor):
        """Position the terminal cursor at the text cursor location"""
        screen_row = self.start_y + cursor.row - self.scroll_offset
        screen_col = cursor.col + self.text_start_col
        
        if (self.start_y <= screen_row < self.start_y + self.text_height and 
            self.text_start_col <= screen_col < self.start_x + self.width):
            try:
                self.stdscr.move(screen_row, screen_col)
            except curses.error:
                pass
    
    def clear_screen(self):
        """Clear the entire screen"""
        self.stdscr.clear()
    
    def refresh(self):
        """Refresh the screen to show changes"""
        self.stdscr.refresh()
    
    def render_all(self, text_buffer, cursor, selection_manager):
        """Render everything: text, line numbers, status bar, and position cursor"""
        self.scroll_if_needed(cursor)
        self.render_line_numbers(text_buffer)
        self.render_text(text_buffer, cursor)
        self.render_status_bar(text_buffer, cursor)
        self.position_cursor(cursor)
        self.refresh()