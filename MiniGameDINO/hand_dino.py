import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import pyautogui
import webbrowser

# webbrowser.open('https://chromedino.com/')
detector = HandDetector(detectionCon=0.8, maxHands=1)

time.sleep(2.0)

#current_key_pressed = set()

video = cv2.VideoCapture(0)
#start = 0

def alt_tab():
    pyautogui.keyDown('alt')
    time.sleep(.2)
    pyautogui.press('tab')
    time.sleep(.2)
    pyautogui.keyUp('alt')

change_tab = 0


def updatetextfile(actionnumber):
    with open('userinput.txt', 'r') as file:
        lines = file.readlines()
                
    # Update the first line with '1'
    lines[0] = ''+ str(actionnumber) +'\n'  # Add '\n' to ensure the line ends with a newline character
    
    print(lines[0])

    with open('userinput.txt', 'w') as file:
        file.writelines(lines)

updatetextfile(actionnumber=0)

while True:
    ret, frame = video.read()
    hands, img = detector.findHands(frame)
    cv2.rectangle(img, (0, 480), (300, 425), (50, 50, 255), -2)
    cv2.rectangle(img, (640, 480), (400, 425), (50, 50, 255), -2)

    if hands:
        lmList = hands[0]
        fingerUp = detector.fingersUp(lmList)
        print(fingerUp)

        if fingerUp == [0, 0, 0, 0, 0]:
            cv2.putText(frame, 'Finger Count: 0', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Jumping', (440, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

            updatetextfile(actionnumber=1)

        elif fingerUp == [0, 1, 1, 0, 0]:
            cv2.putText(frame, 'Finger Count: 2', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Ducking', (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

            updatetextfile(actionnumber=2)

        elif fingerUp == [1, 1, 0, 0, 1]:
            cv2.putText(frame, 'ROCK n ROLL', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'STARTING', (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

            updatetextfile(actionnumber=-1)
        
        else:
            updatetextfile(actionnumber=0)


    cv2.imshow("Frame", frame)
    cv2.moveWindow("Frame", 300, 1200)  # Adjust the coordinates as needed
    cv2.setWindowProperty('Frame', cv2.WND_PROP_TOPMOST, 1)

    change_tab += 1
    if change_tab == 1:
        alt_tab()

    k = cv2.waitKey(1)
    if k == ord('q'):
        break


video.release()
#cv2.waitKey(1)
cv2.destroyAllWindows()
updatetextfile(actionnumber=0)