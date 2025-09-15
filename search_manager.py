"""
Search - Handle search and replace functionality
"""

import re

class SearchManager:
    """Manages search and replace operations"""
    
    def __init__(self):
        self.last_search = ""
        self.current_matches = []
        self.current_match_index = -1
        self.case_sensitive = False
        self.use_regex = False
    
    def find_all_matches(self, text_buffer, search_term):
        """Find all matches of the search term in the buffer"""
        if not search_term:
            return []
        
        matches = []
        flags = 0 if self.case_sensitive else re.IGNORECASE
        
        try:
            if self.use_regex:
                pattern = re.compile(search_term, flags)
            else:
                # Escape special regex characters for literal search
                escaped_term = re.escape(search_term)
                pattern = re.compile(escaped_term, flags)
            
            for row in range(text_buffer.get_line_count()):
                line = text_buffer.get_line(row)
                for match in pattern.finditer(line):
                    matches.append({
                        'row': row,
                        'col': match.start(),
                        'length': match.end() - match.start(),
                        'text': match.group()
                    })
        
        except re.error:
            # Invalid regex pattern
            return []
        
        return matches
    
    def search(self, text_buffer, search_term, start_row=0, start_col=0):
        """Search for a term starting from the given position"""
        self.last_search = search_term
        self.current_matches = self.find_all_matches(text_buffer, search_term)
        
        if not self.current_matches:
            return None
        
        # Find the first match at or after the current position
        for i, match in enumerate(self.current_matches):
            if (match['row'] > start_row or 
                (match['row'] == start_row and match['col'] >= start_col)):
                self.current_match_index = i
                return match
        
        # If no match found after current position, wrap to beginning
        if self.current_matches:
            self.current_match_index = 0
            return self.current_matches[0]
        
        return None
    
    def find_next(self, text_buffer):
        """Find the next occurrence of the last search term"""
        if not self.current_matches or not self.last_search:
            return None
        
        if self.current_match_index < len(self.current_matches) - 1:
            self.current_match_index += 1
        else:
            # Wrap to beginning
            self.current_match_index = 0
        
        return self.current_matches[self.current_match_index]
    
    def find_previous(self, text_buffer):
        """Find the previous occurrence of the last search term"""
        if not self.current_matches or not self.last_search:
            return None
        
        if self.current_match_index > 0:
            self.current_match_index -= 1
        else:
            # Wrap to end
            self.current_match_index = len(self.current_matches) - 1
        
        return self.current_matches[self.current_match_index]
    
    def replace_current(self, text_buffer, replacement):
        """Replace the current match with replacement text"""
        if (self.current_match_index < 0 or 
            self.current_match_index >= len(self.current_matches)):
            return False
        
        match = self.current_matches[self.current_match_index]
        row, col = match['row'], match['col']
        length = match['length']
        
        # Delete the matched text
        line = text_buffer.get_line(row)
        new_line = line[:col] + replacement + line[col + length:]
        text_buffer.lines[row] = new_line
        text_buffer.modified = True
        
        # Update positions of subsequent matches in the same line
        length_diff = len(replacement) - length
        for i in range(self.current_match_index + 1, len(self.current_matches)):
            if self.current_matches[i]['row'] == row:
                self.current_matches[i]['col'] += length_diff
        
        return True
    
    def replace_all(self, text_buffer, search_term, replacement):
        """Replace all occurrences of search_term with replacement"""
        self.last_search = search_term
        matches = self.find_all_matches(text_buffer, search_term)
        
        if not matches:
            return 0
        
        # Process matches in reverse order to maintain correct positions
        matches.reverse()
        replacements_made = 0
        
        for match in matches:
            row, col = match['row'], match['col']
            length = match['length']
            
            line = text_buffer.get_line(row)
            new_line = line[:col] + replacement + line[col + length:]
            text_buffer.lines[row] = new_line
            replacements_made += 1
        
        if replacements_made > 0:
            text_buffer.modified = True
        
        # Clear current matches since positions have changed
        self.current_matches = []
        self.current_match_index = -1
        
        return replacements_made
    
    def get_match_info(self):
        """Get information about current match"""
        if (self.current_match_index >= 0 and 
            self.current_match_index < len(self.current_matches)):
            return {
                'current': self.current_match_index + 1,
                'total': len(self.current_matches),
                'match': self.current_matches[self.current_match_index]
            }
        return None