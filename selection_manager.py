"""
Selection - Handle text selection for copy/cut operations
"""

class SelectionManager:
    """Manages text selection state"""
    
    def __init__(self):
        self.is_selecting = False
        self.start_row = 0
        self.start_col = 0
        self.end_row = 0
        self.end_col = 0
    
    def start_selection(self, row, col):
        """Start a new selection at the given position"""
        self.is_selecting = True
        self.start_row = row
        self.start_col = col
        self.end_row = row
        self.end_col = col
    
    def update_selection(self, row, col):
        """Update the end position of the selection"""
        if self.is_selecting:
            self.end_row = row
            self.end_col = col
    
    def end_selection(self):
        """End the current selection"""
        self.is_selecting = False
    
    def clear_selection(self):
        """Clear the selection"""
        self.is_selecting = False
        self.start_row = 0
        self.start_col = 0
        self.end_row = 0
        self.end_col = 0
    
    def has_selection(self):
        """Check if there is an active selection"""
        return (self.is_selecting and 
                (self.start_row != self.end_row or self.start_col != self.end_col))
    
    def get_selection_bounds(self):
        """Get the normalized selection bounds (start always before end)"""
        if not self.has_selection():
            return None
        
        # Normalize so start is always before end
        if (self.start_row < self.end_row or 
            (self.start_row == self.end_row and self.start_col <= self.end_col)):
            return {
                'start_row': self.start_row,
                'start_col': self.start_col,
                'end_row': self.end_row,
                'end_col': self.end_col
            }
        else:
            return {
                'start_row': self.end_row,
                'start_col': self.end_col,
                'end_row': self.start_row,
                'end_col': self.start_col
            }
    
    def is_position_selected(self, row, col):
        """Check if a given position is within the selection"""
        bounds = self.get_selection_bounds()
        if not bounds:
            return False
        
        if row < bounds['start_row'] or row > bounds['end_row']:
            return False
        
        if row == bounds['start_row'] and row == bounds['end_row']:
            # Single line selection
            return bounds['start_col'] <= col < bounds['end_col']
        elif row == bounds['start_row']:
            # First line of multi-line selection
            return col >= bounds['start_col']
        elif row == bounds['end_row']:
            # Last line of multi-line selection
            return col < bounds['end_col']
        else:
            # Middle line of multi-line selection
            return True
    
    def select_word_at_position(self, text_buffer, row, col):
        """Select the word at the given position"""
        line = text_buffer.get_line(row)
        if col >= len(line):
            return False
        
        # Find word boundaries
        start_col = col
        end_col = col
        
        # Move start_col to beginning of word
        while start_col > 0 and line[start_col - 1].isalnum():
            start_col -= 1
        
        # Move end_col to end of word
        while end_col < len(line) and line[end_col].isalnum():
            end_col += 1
        
        if start_col == end_col:
            return False
        
        self.start_selection(row, start_col)
        self.update_selection(row, end_col)
        return True
    
    def select_line(self, text_buffer, row):
        """Select an entire line"""
        line_length = text_buffer.get_line_length(row)
        self.start_selection(row, 0)
        self.update_selection(row, line_length)
    
    def select_all(self, text_buffer):
        """Select all text in the buffer"""
        last_row = text_buffer.get_line_count() - 1
        last_col = text_buffer.get_line_length(last_row)
        
        self.start_selection(0, 0)
        self.update_selection(last_row, last_col)
    
    def get_selected_text(self, text_buffer):
        """Get the currently selected text as a string"""
        bounds = self.get_selection_bounds()
        if not bounds:
            return ""
        
        if bounds['start_row'] == bounds['end_row']:
            # Single line selection
            line = text_buffer.get_line(bounds['start_row'])
            return line[bounds['start_col']:bounds['end_col']]
        else:
            # Multi-line selection
            lines = []
            
            # First line
            first_line = text_buffer.get_line(bounds['start_row'])
            lines.append(first_line[bounds['start_col']:])
            
            # Middle lines
            for row in range(bounds['start_row'] + 1, bounds['end_row']):
                lines.append(text_buffer.get_line(row))
            
            # Last line
            last_line = text_buffer.get_line(bounds['end_row'])
            lines.append(last_line[:bounds['end_col']])
            
            return '\n'.join(lines)