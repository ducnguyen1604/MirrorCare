from threading import Thread
from werkzeug.serving import run_simple

import pyaudio
import wave
import keyboard
from pydub import AudioSegment
import subprocess
import os
#------------------------
import speech_recognition as sr

import google.generativeai as genai
genai.configure(api_key="AIzaSyAIwi8Tn3vcl8L_SluRolAlqYsvHC7BvPI")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

#------------------------
from gtts import gTTS
from elevenlabs import play, save
from elevenlabs.client import ElevenLabs
client = ElevenLabs(
  api_key="cde1e7dfd335ded40ad3e8fdd02cb369", # Defaults to ELEVEN_API_KEY
)
#------------------------
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the status as False
playAudio = False

@app.route('/get_data', methods=['GET'])
def get_data():
    data = playAudio
    return jsonify(data)
#------------------------------------------------------
# Convert mp3 to ogg (Path)
mp3_input_path = "public/audios/output_speech.mp3"
ogg_output_path = "public/audios/output_speech.ogg"

# Convert ogg to json (Path)
input_audio_file = r"public\audios\output_speech.ogg"
output_json_file = r"public\audios\output_speech.json"

# Save input recording
filename = "input_recording.wav"
r = sr.Recognizer()
#------------------------------------------------------
# Function to convert ogg to json
def run_rhubarb(input_file, output_file):
    rhubarb_exe_path = r"Rhubarb-Lip-Sync-1.13.0-Windows\rhubarb.exe"

    input_file = os.path.abspath(input_file)
    output_file = os.path.abspath(output_file)

    command = [
        rhubarb_exe_path,
        "-f", "json",
        input_file,
        "-o", output_file
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Rhubarb Lip Sync completed. Output saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running Rhubarb Lip Sync: {e}")
#------------------------------------------------------
# Function to convert mp3 to ogg
def convert_mp3_to_ogg(input_path, output_path):
    # Load the MP3 file
    audio = AudioSegment.from_mp3(input_path)

    # Convert MP3 to OGG
    audio.export(output_path, format="ogg")
#------------------------------------------------------
def save_latest_recording(frames):
    global playAudio
    
    playAudio = True

    if frames:
        sound_file = wave.open("input_recording.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()
        print("Latest recording saved as input_recording.wav")

        with sr.AudioFile(filename) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            try:
                text = r.recognize_google(audio_data)
                print("Recognized speech:", text)

                #print("You are a Kind Singaporean Caretaker which uses slang and full of personality, Please Response to this message:" + text)

                #convo = model.start_chat(history=[])
                #convo.send_message("You are a Kind Singaporean Caretaker which uses slang and full of personality, Please Response to this message:" + text)

                #print("Response from model:", convo.last.text)

                #outputaudio = client.generate(
                #    text= "Of course lah! You all triple E students are truly champions, lah! With your mirror care project, you'll be spreading good vibes and making a real difference for the elderly, no doubt about it!",
                #    voice= "Lily",
                #)
                #save(outputaudio, "./public/audios/output_speech.mp3")

                #convert_mp3_to_ogg(mp3_input_path, ogg_output_path)

                #run_rhubarb(input_audio_file, output_json_file)

                  # Set playAudio to True when a new output file is generated
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
#------------------------------------------------------
def run_flask_app():
    run_simple("127.0.0.1", 5000, app, use_reloader=False, use_debugger=True, threaded=True)

if __name__ == "__main__":
    # Start Flask app in a separate thread
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    recording = False  # Flag to indicate whether recording is in progress
    frames = []  # List to store the current recording frames

    try:
        while True:
            if keyboard.is_pressed('h'):
                if not recording:
                    print("Recording started...")
                    recording = True
                    frames = []  # Clear frames for a new recording
            elif recording:
                print("Recording stopped.")
                recording = False
                save_latest_recording(frames)

            if recording:
                data = stream.read(1024)
                frames.append(data)

    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    audio.terminate()
#------------------------------------------------------