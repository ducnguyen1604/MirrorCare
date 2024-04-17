import cv2
from cvzone.HandTrackingModule import HandDetector
from directkeys import PressKey, ReleaseKey
from directkeys import space_pressed, up_pressed, down_pressed
import time
import pyautogui,time
import webbrowser


#webbrowser.open('https://chromedino.com/')
detector=HandDetector(detectionCon=0.8, maxHands=1)

space_key_pressed=space_pressed
up_key_pressed=up_pressed
down_key_pressed=down_pressed


time.sleep(2.0)

current_key_pressed = set()

video=cv2.VideoCapture(0)
start=0

def alt_tab():
    pyautogui.keyDown('alt')
    time.sleep(.2)
    pyautogui.press('tab')
    time.sleep(.2)
    pyautogui.keyUp('alt')
    
change_tab=0

while True:
    ret,frame=video.read()
    keyPressed = False
    spacePressed=False
    key_count=0
    key_pressed=0   
    hands,img=detector.findHands(frame)
    cv2.rectangle(img, (0, 480), (300, 425),(50, 50, 255), -2)
    cv2.rectangle(img, (640, 480), (400, 425),(50, 50, 255), -2)
    #get_value()
    if hands:
        lmList=hands[0]
        fingerUp=detector.fingersUp(lmList)
        print(fingerUp)
        if fingerUp==[0,0,0,0,0]:            
            cv2.putText(frame, 'Finger Count: 0', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Jumping', (440,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            PressKey(up_key_pressed)
            spacePressed=True
            current_key_pressed.add(up_key_pressed)
            key_pressed=up_key_pressed
            keyPressed = True
            key_count=key_count+1
            #get_value()
        if fingerUp==[0,1,0,0,0]:
            cv2.putText(frame, 'Finger Count: 1', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        if fingerUp==[0,1,1,0,0]:
            cv2.putText(frame, 'Finger Count: 2', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            PressKey(down_key_pressed)
            spacePressed=True
            current_key_pressed.add(down_key_pressed)
            key_pressed=down_key_pressed
            keyPressed = True
            key_count=key_count+1
        if fingerUp==[0,1,1,1,0]:
            cv2.putText(frame, 'Finger Count: 3', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        if fingerUp==[0,1,1,1,1]:
            cv2.putText(frame, 'Finger Count: 4', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        if fingerUp==[1,1,1,1,1]:
            cv2.putText(frame, 'Finger Count: 5', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Not Jumping', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        if not keyPressed and len(current_key_pressed) != 0:
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
        elif key_count==1 and len(current_key_pressed)==2:    
            for key in current_key_pressed:             
                if key_pressed!=key:
                    ReleaseKey(key)
            current_key_pressed = set()
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
    #get_value()
    #cv2.resizeWindow("Frame", 700, 200) 
    cv2.imshow("Frame",frame)
    #webbrowser.open('https://chromedino.com/')

    change_tab+=1
    if change_tab==1:
        alt_tab()

    k=cv2.waitKey(1)
    if k==ord('q'):
        break
    #webbrowser.open('https://chromedino.com/')

video.release()
#webbrowser.open('https://chromedino.com/')
cv2.destroyAllWindows()
