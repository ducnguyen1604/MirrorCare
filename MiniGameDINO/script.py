import threading
import subprocess
import pyautogui,time
#from hand_dino import get_value


#value = get_value()
#value=1
#print(value)

def run_script(script_name):
    subprocess.run(["python", script_name])

#pyautogui.keyDown('alt')
#time.sleep(.2)
#pyautogui.press('tab')
#time.sleep(.2)
#pyautogui.keyUp('alt')


if __name__ == "__main__":
    script1_thread = threading.Thread(target=run_script, args=("hand_dino.py",))
    script2_thread = threading.Thread(target=run_script, args=("main.py",))
    #script3_thread = threading.Thread(target=run_script, args="alt_tab.py")

    script1_thread.start()
    script2_thread.start()

    script1_thread.join()
    script2_thread.join()

    print("Both scripts have finished executing.")