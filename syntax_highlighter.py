"""
Syntax Highlighter - Provides syntax highlighting using Pygments
"""

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_for_filename, get_lexer_by_name, TextLexer
    from pygments.formatters import Terminal256Formatter, TerminalFormatter
    from pygments.util import ClassNotFound
    from pygments.token import Token
    import curses
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

class SyntaxHighlighter:
    """Handles syntax highlighting for different file types"""
    
    def __init__(self):
        self.enabled = PYGMENTS_AVAILABLE
        self.lexer = None
        self.language = None
        
        if self.enabled:
            # Try to use 256-color formatter if available, fallback to basic
            try:
                self.formatter = Terminal256Formatter(style='monokai')
            except:
                self.formatter = TerminalFormatter()
        
        # Define color mappings for curses
        self.token_colors = {
            Token.Keyword: curses.COLOR_BLUE,
            Token.Keyword.Constant: curses.COLOR_BLUE,
            Token.Keyword.Declaration: curses.COLOR_BLUE,
            Token.Keyword.Namespace: curses.COLOR_BLUE,
            Token.Keyword.Pseudo: curses.COLOR_BLUE,
            Token.Keyword.Reserved: curses.COLOR_BLUE,
            Token.Keyword.Type: curses.COLOR_BLUE,
            
            Token.Name.Class: curses.COLOR_YELLOW,
            Token.Name.Function: curses.COLOR_YELLOW,
            Token.Name.Builtin: curses.COLOR_CYAN,
            Token.Name.Exception: curses.COLOR_RED,
            
            Token.String: curses.COLOR_GREEN,
            Token.String.Doc: curses.COLOR_GREEN,
            Token.String.Escape: curses.COLOR_GREEN,
            Token.String.Interpol: curses.COLOR_GREEN,
            
            Token.Number: curses.COLOR_MAGENTA,
            Token.Number.Float: curses.COLOR_MAGENTA,
            Token.Number.Integer: curses.COLOR_MAGENTA,
            
            Token.Comment: curses.COLOR_WHITE,  # Will be dimmed
            Token.Comment.Single: curses.COLOR_WHITE,
            Token.Comment.Multiline: curses.COLOR_WHITE,
            
            Token.Operator: curses.COLOR_RED,
            Token.Punctuation: curses.COLOR_WHITE,
        }
        
        # Initialize color pairs if curses is available
        if curses.has_colors():
            self.init_color_pairs()
    
    def init_color_pairs(self):
        """Initialize curses color pairs for syntax highlighting"""
        try:
            # Define color pairs (pair_number, foreground, background)
            curses.init_pair(10, curses.COLOR_BLUE, -1)    # Keywords
            curses.init_pair(11, curses.COLOR_YELLOW, -1)  # Functions/Classes
            curses.init_pair(12, curses.COLOR_CYAN, -1)    # Builtins
            curses.init_pair(13, curses.COLOR_GREEN, -1)   # Strings
            curses.init_pair(14, curses.COLOR_MAGENTA, -1) # Numbers
            curses.init_pair(15, curses.COLOR_WHITE, -1)   # Comments (dim)
            curses.init_pair(16, curses.COLOR_RED, -1)     # Operators
        except:
            # Color initialization failed, highlighting will be disabled
            pass
    
    def set_language_from_filename(self, filename):
        """Set the syntax highlighting language based on filename"""
        if not self.enabled or not filename:
            return False
        
        try:
            self.lexer = get_lexer_for_filename(filename)
            self.language = self.lexer.name
            return True
        except ClassNotFound:
            self.lexer = TextLexer()
            self.language = "text"
            return False
    
    def set_language_by_name(self, language_name):
        """Set the syntax highlighting language by name"""
        if not self.enabled:
            return False
        
        try:
            self.lexer = get_lexer_by_name(language_name)
            self.language = self.lexer.name
            return True
        except ClassNotFound:
            self.lexer = TextLexer()
            self.language = "text"
            return False
    
    def get_line_tokens(self, line_text):
        """Get syntax tokens for a single line"""
        if not self.enabled or not self.lexer:
            return [(Token.Text, line_text)]
        
        try:
            tokens = list(self.lexer.get_tokens(line_text))
            return tokens
        except:
            return [(Token.Text, line_text)]
    
    def get_token_color_pair(self, token_type):
        """Get the curses color pair for a token type"""
        if not curses.has_colors():
            return 0
        
        # Check for exact match first
        if token_type in self.token_colors:
            color = self.token_colors[token_type]
            return self.color_to_pair(color)
        
        # Check parent token types
        for parent in token_type.split():
            if parent in self.token_colors:
                color = self.token_colors[parent]
                return self.color_to_pair(color)
        
        # Default color
        return 0
    
    def color_to_pair(self, color):
        """Convert color constant to color pair number"""
        color_map = {
            curses.COLOR_BLUE: 10,
            curses.COLOR_YELLOW: 11,
            curses.COLOR_CYAN: 12,
            curses.COLOR_GREEN: 13,
            curses.COLOR_MAGENTA: 14,
            curses.COLOR_WHITE: 15,
            curses.COLOR_RED: 16,
        }
        return color_map.get(color, 0)
    
    def highlight_line_for_terminal(self, line_text):
        """Get highlighted line with color information for terminal display"""
        if not self.enabled:
            return [(line_text, 0)]  # (text, color_pair)
        
        tokens = self.get_line_tokens(line_text)
        result = []
        
        for token_type, text in tokens:
            color_pair = self.get_token_color_pair(token_type)
            result.append((text, color_pair))
        
        return result
    
    def is_available(self):
        """Check if syntax highlighting is available"""
        return self.enabled
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        if not self.enabled:
            return []
        
        try:
            from pygments.lexers import get_all_lexers
            return [lexer[1][0] for lexer in get_all_lexers() if lexer[1]]
        except:
            return []
    
    def get_current_language(self):
        """Get the current language name"""
        return self.language or "text"

# Usage example for integration with display.py:
"""
# In display.py, modify render_text method:

def render_text(self, text_buffer, cursor, selection_manager=None, syntax_highlighter=None):
    # ... existing code ...
    
    for i in range(self.text_height):
        line_index = start_line + i
        y_pos = i
        
        # ... existing code ...
        
        if line_index < text_buffer.get_line_count():
            line_text = text_buffer.get_line(line_index)
            
            if syntax_highlighter and syntax_highlighter.is_available():
                # Get highlighted tokens
                highlighted_tokens = syntax_highlighter.highlight_line_for_terminal(line_text)
                
                x_pos = self.text_start_col
                for text_part, color_pair in highlighted_tokens:
                    for char_idx, char in enumerate(text_part):
                        if x_pos >= self.text_start_col + self.text_width:
                            break
                        
                        # Check if selected
                        is_selected = (selection_manager and 
                                     selection_manager.is_position_selected(line_index, x_pos - self.text_start_col))
                        
                        try:
                            if is_selected:
                                self.stdscr.addstr(y_pos, x_pos, char, curses.color_pair(3))
                            elif color_pair > 0:
                                self.stdscr.addstr(y_pos, x_pos, char, curses.color_pair(color_pair))
                            else:
                                self.stdscr.addstr(y_pos, x_pos, char)
                        except curses.error:
                            pass
                        
                        x_pos += 1
            else:
                # Fallback to regular rendering
                # ... existing character-by-character rendering code ...
"""