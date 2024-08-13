import tkinter as tk
from tkinter import filedialog, Label, Button, messagebox
import pyaudio
import wave
import os
import numpy as np
import librosa
import librosa.display

# Initialize PyAudio for audio recording
audio = pyaudio.PyAudio()

# Initialize tkinter GUI
top = tk.Tk()
top.geometry("800x600")
top.title("Audio Gender Predictor")
top.configure(background="#CDCDCD")

# Initialize labels
label_gender = Label(top, background="#CDCDCD", font=("arial", 15, "bold"))
sign_image = Label(top)

# Placeholder function for gender prediction (to be replaced with actual model logic)
def predict_gender_from_audio(audio_file):
    try:
        # Check if audio file is longer than 30 seconds
        duration = librosa.get_duration(filename=audio_file)
        if duration < 30:
            messagebox.showerror("Error", "Voice note should be more than 30 seconds.")
            return

        # Check if audio file contains the word "HI"
        y, sr = librosa.load(audio_file)
        mfccs = librosa.feature.mfcc(y=y, sr=sr)
        if np.any(np.char.find(mfccs.astype(str), 'HI')):
            messagebox.showerror("Error", "Voice note contains the word 'HI'. Please upload or record a voice note without 'HI'.")
            return

        # Placeholder for gender prediction (replace with actual model prediction)
        gender_prediction = "Male"  # Example prediction

        # Update label with gender prediction
        label_gender.config(foreground="#011638", text=f"Predicted Gender: {gender_prediction}")

    except Exception as e:
        print("Error:", e)

# Function to record audio
def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 30
    WAVE_OUTPUT_FILENAME = "recorded_audio.wav"

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    print("Recording...")

    while len(frames) < int(RATE / CHUNK * RECORD_SECONDS):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return WAVE_OUTPUT_FILENAME

# Function to handle audio upload
def upload_audio():
    try:
        file_path = filedialog.askopenfilename()

        # Check if the file is empty
        if not file_path:
            messagebox.showerror("Error", "Please select a voice note to upload.")
            return

        # Perform gender prediction from uploaded audio
        predict_gender_from_audio(file_path)

    except Exception as e:
        print("Error:", e)

# Function to handle "Detect Gender" button click
def detect_gender():
    try:
        file_path = record_audio()  # Change this to upload_audio() if using upload functionality
        if file_path:
            predict_gender_from_audio(file_path)

    except Exception as e:
        print("Error:", e)

# Button to record audio
record_button = Button(top, text="Record Voice Note", command=record_audio, padx=10, pady=5)
record_button.config(background="#364156", foreground="white", font=("arial", 10, "bold"))
record_button.pack(side="bottom", pady=20)

# Button to upload an audio file
upload_button = Button(top, text="Upload Voice Note", command=upload_audio, padx=10, pady=5)
upload_button.config(background="#364156", foreground="white", font=("arial", 10, "bold"))
upload_button.pack(side="bottom", pady=20)

# Button to detect gender from recorded or uploaded audio
detect_button = Button(top, text="Detect Gender", command=detect_gender, padx=10, pady=5)
detect_button.config(background="#364156", foreground="white", font=("arial", 10, "bold"))
detect_button.pack(side="bottom", pady=20)

# Packing labels
label_gender.pack()

# Label for heading
heading = Label(top, text="Audio Gender Predictor", pady=20, font=("arial", 20, "bold"))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()

# Start GUI main loop
top.mainloop()
