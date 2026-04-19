import time
from functools import wraps
from typing import Callable
import threading

def timed_task(label=None) -> Callable:
    """
    A decorator that displays a real-time running timer with optional custom label.
    Clears the console line completely after task finishes.
    """
    # Handle decorator usage with or without parentheses
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            running = True

            def show_timer():
                while running:
                    elapsed = int(time.time() - start_time)
                    # Build display string
                    if label:
                        display = f"\r[{label}] time elapsed: {elapsed:5d} seconds"
                    else:
                        display = f"\r(time elapsed: {elapsed:5d} seconds)"
                    
                    print(display, end="", flush=True)
                    time.sleep(0.1)

            # Start timer thread
            timer_thread = threading.Thread(target=show_timer, daemon=True)
            timer_thread.start()

            try:
                return func(*args, **kwargs)
            finally:
                # Stop and clean up
                running = False
                timer_thread.join()
                print("\r" + " " * 60 + "\r", end="", flush=True)

        return wrapper

    # Support both @timed_task and @timed_task(label="Logging in")
    if callable(label):
        func = label
        label = None
        return decorator(func)

    return decorator


# ------------------------------
# Usage Examples
# ------------------------------
# 1. No label (original style)
# @timed_task
# def your_login_function():
#     time.sleep(5)

# 2. With custom label (new feature)
# @timed_task(label="BUAA Login")
# def your_login_function():
#     time.sleep(5)

# if __name__ == "__main__":
#     your_login_function()
