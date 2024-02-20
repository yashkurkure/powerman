import psutil
import curses

def draw_menu(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Press 'q' to quit.")

    # Get system info
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    # Display system info
    stdscr.addstr(2, 0, f"CPU Usage: {cpu_usage}%")
    stdscr.addstr(3, 0, f"Memory Usage: {memory_usage}%")

    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Make getch non-blocking

    while True:
        draw_menu(stdscr)
        key = stdscr.getch()
        if key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)