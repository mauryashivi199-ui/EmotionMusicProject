import tkinter as tk
from tkinter import Label, Button
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import pygame
import os
import random

# init pygame
pygame.mixer.init()

# load model
model = load_model("model.h5")

emotions = ['angry', 'happy', 'sad']

# UI window
root = tk.Tk()
root.title("Emotion Music Player")
root.geometry("400x300")

emotion_label = Label(root, text="Emotion: ---", font=("Arial", 16))
emotion_label.pack(pady=10)

song_label = Label(root, text="Now Playing: ---", font=("Arial", 12))
song_label.pack(pady=5)

cap = None
running = False

def play_music(emotion):
    folder = f"music/{emotion}"
    if not os.path.exists(folder):
        song_label.config(text="No music folder")
        return

    song = random.choice(os.listdir(folder))
    pygame.mixer.music.load(os.path.join(folder, song))
    pygame.mixer.music.play()
    song_label.config(text=f"Now Playing: {song}")

def start_camera():
    global cap, running
    running = True
    cap = cv2.VideoCapture(0)

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = cv2.resize(gray, (64, 64))
        face = face / 255.0
        face = np.reshape(face, (1, 64, 64, 1))

        prediction = model.predict(face)
        emotion = emotions[np.argmax(prediction)]

        emotion_label.config(text=f"Emotion: {emotion.upper()}")
        play_music(emotion)

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_camera()
            break

    cap.release()
    cv2.destroyAllWindows()

def stop_camera():
    global running
    running = False
    pygame.mixer.music.stop()
    emotion_label.config(text="Emotion: ---")
    song_label.config(text="Now Playing: ---")

start_btn = Button(root, text="Start Camera", command=start_camera, width=15)
start_btn.pack(pady=10)

stop_btn = Button(root, text="Stop", command=stop_camera, width=15)
stop_btn.pack()

root.mainloop()
