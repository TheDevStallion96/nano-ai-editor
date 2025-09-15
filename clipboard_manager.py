"""
Clipboard - Handle cut, copy, and paste operations
"""

class ClipboardManager:
    """Manages clipboard operations for cut, copy, and paste"""
    
    def __init__(self):
        self.clipboard_lines = []
        self.is_line_mode = False  # True if entire lines were copied
    
    def copy_text(self, text_buffer, start_row, start_col, end_row, end_col):
        """Copy text from buffer to clipboard"""
        self.clipboard_lines = []
        self.is_line_mode = False
        
        if start_row == end_row:
            # Single line selection
            line = text_buffer.get_line(start_row)
            copied_text = line[start_col:end_col]
            self.clipboard_lines = [copied_text]
        else:
            # Multi-line selection
            # First line (from start_col to end)
            first_line = text_buffer.get_line(start_row)
            self.clipboard_lines.append(first_line[start_col:])
            
            # Middle lines (entire lines)
            for row in range(start_row + 1, end_row):
                self.clipboard_lines.append(text_buffer.get_line(row))
            
            # Last line (from start to end_col)
            last_line = text_buffer.get_line(end_row)
            self.clipboard_lines.append(last_line[:end_col])
    
    def copy_line(self, text_buffer, row):
        """Copy an entire line to clipboard"""
        self.clipboard_lines = [text_buffer.get_line(row)]
        self.is_line_mode = True
    
    def copy_word_at_cursor(self, text_buffer, cursor):
        """Copy the word at cursor position"""
        line = text_buffer.get_line(cursor.row)
        if cursor.col >= len(line):
            return False
        
        # Find word boundaries
        start_col = cursor.col
        end_col = cursor.col
        
        # Move start_col to beginning of word
        while start_col > 0 and line[start_col - 1].isalnum():
            start_col -= 1
        
        # Move end_col to end of word
        while end_col < len(line) and line[end_col].isalnum():
            end_col += 1
        
        if start_col == end_col:
            return False
        
        word = line[start_col:end_col]
        self.clipboard_lines = [word]
        self.is_line_mode = False
        return True
    
    def cut_text(self, text_buffer, start_row, start_col, end_row, end_col):
        """Cut text from buffer to clipboard"""
        # First copy the text
        self.copy_text(text_buffer, start_row, start_col, end_row, end_col)
        
        # Then delete it
        if start_row == end_row:
            # Single line
            line = text_buffer.get_line(start_row)
            new_line = line[:start_col] + line[end_col:]
            text_buffer.lines[start_row] = new_line
        else:
            # Multi-line deletion
            first_line = text_buffer.get_line(start_row)
            last_line = text_buffer.get_line(end_row)
            
            # Combine first part of first line with last part of last line
            combined_line = first_line[:start_col] + last_line[end_col:]
            
            # Replace the first line with combined line
            text_buffer.lines[start_row] = combined_line
            
            # Delete the lines in between (including the last line)
            for _ in range(end_row - start_row):
                if start_row + 1 < len(text_buffer.lines):
                    del text_buffer.lines[start_row + 1]
        
        text_buffer.modified = True
    
    def cut_line(self, text_buffer, row):
        """Cut an entire line"""
        self.copy_line(text_buffer, row)
        
        # Delete the line
        if len(text_buffer.lines) > 1:
            del text_buffer.lines[row]
        else:
            # If it's the only line, clear it but keep the line
            text_buffer.lines[0] = ""
        
        text_buffer.modified = True
    
    def paste_text(self, text_buffer, cursor):
        """Paste clipboard content at cursor position"""
        if not self.clipboard_lines:
            return cursor.row, cursor.col
        
        if self.is_line_mode:
            # Paste entire lines
            for i, line in enumerate(self.clipboard_lines):
                text_buffer.lines.insert(cursor.row + i, line)
            text_buffer.modified = True
            return cursor.row + len(self.clipboard_lines), 0
        else:
            # Paste text at cursor position
            if len(self.clipboard_lines) == 1:
                # Single line paste
                line = text_buffer.get_line(cursor.row)
                new_line = line[:cursor.col] + self.clipboard_lines[0] + line[cursor.col:]
                text_buffer.lines[cursor.row] = new_line
                new_col = cursor.col + len(self.clipboard_lines[0])
                text_buffer.modified = True
                return cursor.row, new_col
            else:
                # Multi-line paste
                current_line = text_buffer.get_line(cursor.row)
                
                # Split current line at cursor
                line_before = current_line[:cursor.col]
                line_after = current_line[cursor.col:]
                
                # First line: line_before + first clipboard line
                text_buffer.lines[cursor.row] = line_before + self.clipboard_lines[0]
                
                # Insert middle lines
                for i in range(1, len(self.clipboard_lines) - 1):
                    text_buffer.lines.insert(cursor.row + i, self.clipboard_lines[i])
                
                # Last line: last clipboard line + line_after
                last_line = self.clipboard_lines[-1] + line_after
                text_buffer.lines.insert(cursor.row + len(self.clipboard_lines) - 1, last_line)
                
                text_buffer.modified = True
                new_row = cursor.row + len(self.clipboard_lines) - 1
                new_col = len(self.clipboard_lines[-1])
                return new_row, new_col
    
    def is_empty(self):
        """Check if clipboard is empty"""
        return len(self.clipboard_lines) == 0
    
    def get_clipboard_preview(self, max_length=50):
        """Get a preview of clipboard content"""
        if not self.clipboard_lines:
            return "Empty"
        
        if len(self.clipboard_lines) == 1:
            content = self.clipboard_lines[0]
            if len(content) > max_length:
                return content[:max_length] + "..."
            return content
        else:
            return f"{len(self.clipboard_lines)} lines"