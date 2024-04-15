# Step 1: Launch All Webpage
import subprocess
import time
import os

# Launch Terminal 1 h
# Change to the Avatar directory
avatar_directory = r'.\Avatar'
subprocess.Popen(['start', 'cmd', '/k', 'python', 'VoiceRecord.py'], shell=True, cwd=avatar_directory)

# Launch Terminal 2
# Change to the Telegram directory
telegram_directory = r'.\ReAct\public\images'
subprocess.Popen(['start', 'cmd', '/k', 'python', 'Telegram.py'], shell=True, cwd=telegram_directory)

# Launch Terminal 3
# Change to the ReAct directory
react_directory = r'.\ReAct'
subprocess.run(['start', 'cmd', '/k', 'npm', 'run', 'dev'], shell=True, cwd=react_directory)

# Launch Terminal 4
# Change to the Avatar directory
avatar_directory = r'.\Avatar'
subprocess.run(['start', 'cmd', '/k', 'yarn', 'dev'], shell=True, cwd=avatar_directory)


# Launch Terminal 5 (Deployed Under https://monumental-snickerdoodle-9c90a1.netlify.app/)
# Change to the PeerChat directory
# peerchat_directory = r'.\PeerChat'
# subprocess.run(['start', 'cmd', '/k', 'npm', 'run', 'dev'], shell=True, cwd=peerchat_directory)

#-------------------------------------------------
# Step 2: Routing

#5173 -> Avatar
#5174 -> Main
#5175 -> PeerChat

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import keyboard

# Initialize the WebDriver
driver = webdriver.Chrome()

# List of webpages to toggle between
webpages = ["http://localhost:5174/", "http://localhost:5173/", "https://monumental-snickerdoodle-9c90a1.netlify.app/", "https://glistening-scone-1a8f3e.netlify.app/"]
current_page_index = 0

import pyautogui

def closeprogram():        
        pyautogui.hotkey('alt', 'tab', 'tab')  # Activate window menu
        time.sleep(2)
        pyautogui.hotkey('alt', 'f4')     # Close the specific window
        time.sleep(2)
        pyautogui.hotkey('f5')     # Close the specific window


flag = False

# Function to toggle between webpages
def toggle_webpage():
    global current_page_index
    global flag
    current_page_index = (current_page_index + 1) % len(webpages)
    print(flag)



    if webpages[current_page_index] == "https://glistening-scone-1a8f3e.netlify.app/":
        flag = True
        dino_directory = r'.\MiniGameDINO'
        subprocess.Popen(['start', 'cmd', '/c', 'python', 'script.py'], shell=True, cwd=dino_directory)
    
    if (webpages[current_page_index] != "https://glistening-scone-1a8f3e.netlify.app/") and (flag == True):
        
        closeprogram()
        flag = False
    

    driver.get(webpages[current_page_index])

    if webpages[current_page_index] == "https://monumental-snickerdoodle-9c90a1.netlify.app/": #/index.html?room=vAww3f
        # Define the path to the text file
        file_path = os.path.join(r'.\ReAct\public\images', 'password.txt')

        # Read the contents of the text file
        with open(file_path, 'r') as file:
            password = file.read()

        print(password)
        driver.get(webpages[current_page_index] + "/index.html?room=" + password)


# Open the initial webpage
driver.get(webpages[current_page_index])

# Continuous loop to listen for key presses
while True:
    if keyboard.is_pressed('t'):
        toggle_webpage()
        time.sleep(0.2)  # debounce delay to prevent multiple toggles with one key press