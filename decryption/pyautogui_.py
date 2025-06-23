import pyautogui
import time
import os

# Path to the PDF file
pdf_path = r"C:\path\to\your\protected.pdf"

# Credentials
username = "your_username"
password = "your_password"

# Open the PDF with default program (e.g., Adobe)
os.startfile(pdf_path)

# Wait for Adobe to load and show login prompt
time.sleep(5)  # Adjust based on your system's speed

# Simulate typing username
pyautogui.write(username)
pyautogui.press("tab")  # Move to password field

# Simulate typing password
pyautogui.write(password)
pyautogui.press("enter")  # Submit the login

# Wait for decryption to complete and file to load
time.sleep(5)

# Optional: Trigger save-as to export decrypted copy
# Use shortcut for "Save As" (Alt + F, then A) or Ctrl+Shift+S
pyautogui.hotkey('ctrl', 'shift', 's')
time.sleep(2)

# Type the output filename
pyautogui.write("decrypted_copy.pdf")
pyautogui.press("enter")
