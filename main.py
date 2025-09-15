"""
Terminal Text Editor - Main Entry Point
A simple nano-like text editor built with Python curses
"""

import curses
import sys
import os
from editor import Editor

def init_curses():
    """Initialize curses with proper settings"""
    # Initialize the screen
    stdscr = curses.initscr()
    
    # Configure curses
    curses.noecho()        # Don't echo keys to screen
    curses.cbreak()        # React to keys instantly
    curses.raw()           # Enable raw mode for special keys
    stdscr.keypad(True)    # Enable special keys like arrow keys
    
    # Hide cursor initially
    curses.curs_set(1)
    
    # Enable colors if available
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        # Define color pairs
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)   # Status bar
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Line numbers
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Highlighted text
    
    return stdscr

def cleanup_curses():
    """Cleanup curses before exit"""
    try:
        curses.endwin()
    except curses.error:
        pass  # Ignore if curses is not initialized or already ended
    # curses.nocbreak()
    # curses.echo()
    # curses.endwin()

def main():
    """Main entry point"""
    filename = None
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        # Check if file exists
        if not os.path.exists(filename):
            # Create empty file
            try:
                with open(filename, 'w') as f:
                    pass
            except IOError as e:
                print(f"Error creating file {filename}: {e}")
                sys.exit(1)
    
    stdscr = None
    try:
        # Initialize curses
        stdscr = init_curses()
        
        # Create and run editor
        editor = Editor(stdscr)
        if filename:
            editor.open_file(filename)
        
        editor.run()
        
    except KeyboardInterrupt:
        pass
    except Exception as e:
        # Make sure we cleanup curses before showing error
        if stdscr:
            cleanup_curses()
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        # Always cleanup curses
        cleanup_curses()

if __name__ == "__main__":
    main()