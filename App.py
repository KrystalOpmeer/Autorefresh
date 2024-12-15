from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import threading

# Flags to control execution
stop_flag = False
pause_flag = False
countdown_flag = False

# Function to monitor for the 'q' key press
def monitor_keypress():
    global stop_flag, pause_flag, countdown_flag
    try:
        import keyboard
        while not stop_flag:
            if keyboard.is_pressed('q'):
                print("Detected 'q' key press. Stopping the process in 2 minutes...")
                countdown_flag = True
                break
            if keyboard.is_pressed('p'):
                pause_flag = not pause_flag
                state = "paused" if pause_flag else "resumed"
                print(f"Execution {state}.")
                time.sleep(0.5)  # Debounce for key press
    except ImportError:
        print("The 'keyboard' module is not available. Install it using 'pip install keyboard'.")
    except Exception as e:
        print(f"Key monitoring failed: {e}")

# Countdown timer to close the program 2 minutes after 'q' is pressed
def countdown_timer():
    global stop_flag, countdown_flag
    while not stop_flag:
        if countdown_flag:
            print("Countdown started: Program will terminate in 2 minutes.")
            for remaining in range(120, 0, -1):
                if stop_flag:  # Allow immediate termination
                    break
                print(f"Time remaining: {remaining} seconds", end='\r')
                time.sleep(1)
            if countdown_flag and not stop_flag:
                print("\n2 minutes elapsed. Terminating program.")
                stop_flag = True

# Function to monitor mouse clicks and pause execution
def monitor_mouse_clicks(driver):
    global pause_flag
    driver.execute_script("""
        window.pauseExecutionFlag = false;
        document.addEventListener('click', function() {
            window.pauseExecutionFlag = true;
        });
    """)
    while not stop_flag:
        try:
            pause_flag = driver.execute_script("return window.pauseExecutionFlag;")
            if pause_flag:
                print("Mouse click detected. Execution paused. Complete manual actions and press 'p' to resume.")
                driver.execute_script("window.pauseExecutionFlag = false;")  # Reset flag in JavaScript
                time.sleep(0.5)  # Prevent rapid triggering
        except Exception as e:
            print(f"Mouse click monitoring failed: {e}")
        time.sleep(0.5)

# Start WebDriver
driver = webdriver.Chrome()

# Start the keypress monitoring thread
key_thread = threading.Thread(target=monitor_keypress, daemon=True)
key_thread.start()

# Start the mouse click monitoring thread
mouse_thread = threading.Thread(target=monitor_mouse_clicks, args=(driver,), daemon=True)
mouse_thread.start()

# Start the countdown timer thread
timer_thread = threading.Thread(target=countdown_timer, daemon=True)
timer_thread.start()

try:
    print("Browser started. Please log in and navigate to the required page.")
    driver.get("about:blank")
    input("Press Enter after reaching the desired page...")

    print("Press 'q' to stop, 'p' to pause/resume, or click on the page to pause.")
    while not stop_flag:
        if pause_flag:
            time.sleep(1)  # Check periodically if execution is resumed
            continue

        try:
            if countdown_flag:  # Stop further button clicking after 'q'
                print("Execution stopped. No further actions will be performed.")
                break

            print("Attempting to locate the course button...")
            course_button = WebDriverWait(driver, 5).until(  # Reduced waiting time to 5 seconds
                EC.element_to_be_clickable((By.XPATH, 'replace  your course button's Xpath here'))
            )

            driver.execute_script("arguments[0].scrollIntoView(true);", course_button)
            try:
                course_button.click()
                print("Course button clicked successfully.")
            except Exception as e:
                print("Direct click failed. Attempting JavaScript click.")
                driver.execute_script("arguments[0].click();", course_button)

            print("Waiting before locating the back button...")
            time.sleep(3)

            print("Waiting for the back button...")
            back_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, 'Replace your go back button's Xpath here'))
            )

            driver.execute_script("arguments[0].scrollIntoView(true);", back_button)
            try:
                back_button.click()
                print("Back button clicked successfully.")
            except Exception as e:
                print("Direct click on back button failed. Attempting JavaScript click.")
                driver.execute_script("arguments[0].click();", back_button)

        except Exception as e:
            print(f"An error occurred while processing buttons: {e}")

        time.sleep(1)

except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    stop_flag = True  # Ensure threads exit
    print("You can now complete manual actions or close the browser manually.")
