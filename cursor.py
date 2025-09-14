"""
Cursor - Manages cursor position and movement
"""

class Cursor:
    """Manages cursor position and movement within the text buffer"""
    
    def __init__(self):
        self.row = 0
        self.col = 0
        self.desired_col = 0  # Used for vertical movement to maintain column preference
    
    def move_up(self, text_buffer):
        """Move cursor up one line"""
        if self.row > 0:
            self.row -= 1
            # Try to maintain the desired column position
            line_length = text_buffer.get_line_length(self.row)
            self.col = min(self.desired_col, line_length)
    
    def move_down(self, text_buffer):
        """Move cursor down one line"""
        if self.row < text_buffer.get_line_count() - 1:
            self.row += 1
            # Try to maintain the desired column position
            line_length = text_buffer.get_line_length(self.row)
            self.col = min(self.desired_col, line_length)
    
    def move_left(self, text_buffer):
        """Move cursor left one character"""
        if self.col > 0:
            self.col -= 1
        elif self.row > 0:
            # Move to end of previous line
            self.row -= 1
            self.col = text_buffer.get_line_length(self.row)
        
        # Update desired column for vertical movement
        self.desired_col = self.col
    
    def move_right(self, text_buffer):
        """Move cursor right one character"""
        line_length = text_buffer.get_line_length(self.row)
        if self.col < line_length:
            self.col += 1
        elif self.row < text_buffer.get_line_count() - 1:
            # Move to beginning of next line
            self.row += 1
            self.col = 0
        
        # Update desired column for vertical movement
        self.desired_col = self.col
    
    def move_to_line_start(self):
        """Move cursor to the beginning of the current line"""
        self.col = 0
        self.desired_col = 0
    
    def move_to_line_end(self, text_buffer):
        """Move cursor to the end of the current line"""
        self.col = text_buffer.get_line_length(self.row)
        self.desired_col = self.col
    
    def move_word_forward(self, text_buffer):
        """Move cursor to the start of the next word"""
        line = text_buffer.get_line(self.row)
        
        # Skip current word
        while self.col < len(line) and line[self.col].isalnum():
            self.col += 1
        
        # Skip whitespace
        while self.col < len(line) and line[self.col].isspace():
            self.col += 1
        
        # If we reached end of line, move to next line
        if self.col >= len(line) and self.row < text_buffer.get_line_count() - 1:
            self.row += 1
            self.col = 0
        
        self.desired_col = self.col
    
    def move_word_backward(self, text_buffer):
        """Move cursor to the start of the previous word"""
        if self.col > 0:
            self.col -= 1
            line = text_buffer.get_line(self.row)
            
            # Skip whitespace
            while self.col > 0 and line[self.col].isspace():
                self.col -= 1
            
            # Skip word
            while self.col > 0 and line[self.col - 1].isalnum():
                self.col -= 1
        
        elif self.row > 0:
            # Move to end of previous line
            self.row -= 1
            self.col = text_buffer.get_line_length(self.row)
        
        self.desired_col = self.col
    
    def clamp_to_buffer(self, text_buffer):
        """Ensure cursor position is valid within the text buffer"""
        # Clamp row
        max_row = max(0, text_buffer.get_line_count() - 1)
        self.row = max(0, min(self.row, max_row))
        
        # Clamp column
        line_length = text_buffer.get_line_length(self.row)
        self.col = max(0, min(self.col, line_length))
        
        # Update desired column
        self.desired_col = self.col
    
    def set_position(self, row, col):
        """Set cursor to specific position"""
        self.row = row
        self.col = col
        self.desired_col = col
    
    def get_position(self):
        """Get current cursor position as (row, col) tuple"""
        return (self.row, self.col)