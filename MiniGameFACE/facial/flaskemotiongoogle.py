from Google import Create_Service

CLIENT_SECRET_FILE = 'client_secret_mirrorcare.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

spreadsheet_id = '1yOmEXi-7S6PydeWj9mPBoQfhNda4Q8BtkMxB_40WkLs'
worksheet_name = 'Data!'

def update_google_sheet(mydata, spreadsheet_id, worksheet_name):
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # Function: Obtain Values from A1 cell
    response = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        majorDimension='ROWS',
        range='Data!A1:A1'
    ).execute()

    value = response.get('values')[0][0] if 'values' in response and response.get('values') else None

    # Function: Insert all of the current data into the google sheet
    cell_range_insert = 'B' + str(value)

    # Prepare values for insertion
    values = []
    for data in mydata:
        row_values = [
            data.get('highScore', ''),
            data.get('dominant_emotion', ''),
            data.get('current_date', ''),
            data.get('current_time', '')
        ]
        values.append(row_values)

    # Define value range body
    value_range_body = {
        'majorDimension': 'ROWS',
        'values': values
    }

    # Update the Google Sheet
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        valueInputOption='USER_ENTERED',
        range=worksheet_name + cell_range_insert,
        body=value_range_body
    ).execute()

    # Function: Update the Values from A1 Cell
    final_value = int(value) + len(mydata)

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        valueInputOption='USER_ENTERED',
        range='Data!A1',
        body={'values': [[final_value]]}
    ).execute()

#--------------------------------------



import cv2
import mediapipe as mp
import numpy as np
from deepface import DeepFace
import time
from flask import Flask, render_template, Response, jsonify
import webbrowser
import threading
from datetime import datetime
#
app = Flask(__name__)
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
highScore = 0
game_data = []

mp_drawing.DrawingSpec(color=(0,0,225), thickness=2, circle_radius=2)


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    return angle

try:
    with open('highscore_data.txt', 'r') as f:
        highScore = int(f.read())
        print(highScore)
except:
    pass

@app.route('/')
def index():
    return render_template('template3/index.html')

@app.route('/start_game')
def start_game():
    threading.Thread(target=start_countdown_and_camera).start()
    return 'Game started!'

def start_countdown_and_camera():
    threading.Thread(target=start_camera).start()
    countdown_duration = 3  # Adjust countdown duration as needed
    start_time = time.time()
    
    while time.time() - start_time < countdown_duration:
        time_left = countdown_duration - (time.time() - start_time)
        print(f"Starting in {int(time_left)} seconds...")
        time.sleep(1)
    
    print("Starting the game!")
    
def start_camera():
    
    #global highScore
    global game_data
    
    cap = cv2.VideoCapture(0)
    counter = 0
    stage = None
    start_time = time.time()
    countdown_duration = 30  # 1 minute countdown
    countdown_start = start_time
    # Create OpenCV window with flag WINDOW_NORMAL
    #cv2.imshow('Demo video', image)
    cv2.namedWindow('Pose Detection', cv2.WINDOW_FULLSCREEN)
    # Set the window to be on top of others
    cv2.setWindowProperty('Pose Detection', cv2.WND_PROP_TOPMOST, 1)
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            current_time = time.time()
            if current_time - start_time >= 30:
                break

            ret, frame = cap.read()

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Calculate time left for countdown
            time_left = countdown_duration - (current_time - countdown_start)
            minutes = int(time_left // 60)
            seconds = int(time_left % 60)

            # Format the timer text
            timer_text = f"Time Left: {minutes:02d}:{seconds:02d}"         

            # Make detection
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            # Add timer text to the frame
            cv2.putText(image, timer_text, (image.shape[1] - 300, image.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)  
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                shoulder2 = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow2 = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist2 = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                #calculate angle
                angle = calculate_angle(shoulder, elbow, wrist)
                angle2 = calculate_angle(shoulder2, elbow2, wrist2)

                #visualise angle
                cv2.putText(image, str(angle),
                            tuple(np.multiply(shoulder, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, str(angle2),
                            tuple(np.multiply(shoulder2, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                #curl counter logic
                if angle > 120 and angle2 > 120:
                    stage = "down"
                if angle < 30 and angle2 < 30 and stage == 'down':
                    stage = "up"
                    counter += 1
                print(counter)

            except:
                pass
                
            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0,0), (265,73), (245,117,16), -1) #main box
            cv2.rectangle(image, (460,0), (620,73), (245, 117,16), -1) #highscore box

            # Rep data
            cv2.putText(image, 'REPS', (15,12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter),
                        (10,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (95,12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage,
                        (100,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            '''
            #Highscore data
            cv2.putText(image, 'Highscore', (470,12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(highScore),
                        (475,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                        )
            '''
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                    )
        
            # Perform face detection using the cascade classifier
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.1, 4)
    
            # Iterate through detected faces
            for (x, y, w, h) in faces:
                # Extract the face region
                face_region = frame[y:y+h, x:x+w]
        
                # Analyze the emotions using the loaded model
                predictions = DeepFace.analyze(face_region, actions=['emotion'], enforce_detection=False)
        
                # Check the structure of predictions
                if isinstance(predictions, list):
                    # If predictions is a list, extract the first item (assuming it's the dominant emotion)
                    dominant_emotion = predictions[0]['dominant_emotion']
                else:
                    # If predictions is a dictionary, directly access the dominant emotion
                    dominant_emotion = predictions['dominant_emotion']
                
                # timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
                current_time = datetime.now().strftime('%I:%M:%S %p')
                current_date = datetime.now().strftime('%m/%d/%Y')

                #append current game data to the list
                print(type(counter), counter)
                print(type(dominant_emotion), dominant_emotion)
                print(type(current_date), current_date)
                print(type(current_time), current_time)
                
                game_data.append({'highScore' : counter, 'dominant_emotion' : dominant_emotion, 'current_date' : current_date, 'current_time' : current_time})
                print(game_data)
                
                # Draw rectangle around the face
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
                # Put text indicating the dominant emotion on the frame
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image, dominant_emotion, (x, y - 10), font, 0.9, (0, 255, 0), 2, cv2.LINE_AA)
            
            cv2.imshow('Pose Detection', image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        update_google_sheet(game_data, spreadsheet_id, worksheet_name)

    cap.release()
    cv2.destroyAllWindows()

def open_browser():
    url = 'http://127.0.0.2:5000/'  # Change the URL to match your Flask application's URL
    webbrowser.open(url)

if __name__ == "__main__":
    open_browser()
    app.run(host='127.0.0.2')