import cv2
from fer import FER
import pygame
import random
import os

# Initialize emotion detector
detector = FER()

# Initialize pygame mixer
pygame.mixer.init()

# Function to play music for detected emotion
def play_music(emotion):
    folder_path = f"music/{emotion}"

    if not os.path.exists(folder_path):
        print(f"No folder found for emotion: {emotion}")
        return

    songs = os.listdir(folder_path)

    if not songs:
        print(f"No music found inside: {folder_path}")
        return

    selected_song = random.choice(songs)
    song_path = os.path.join(folder_path, selected_song)

    print(f"\nPlaying: {song_path}\n")

    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

# Start video camera
cam = cv2.VideoCapture(0)

current_emotion = ""

print("Detecting Emotion... Press 'q' to quit.")

while True:
    ret, frame = cam.read()
    if not ret:
        print("Camera error!")
        break

    # Detect emotions
    result = detector.detect_emotions(frame)

    if result:
        emotions = result[0]['emotions']
        detected = max(emotions, key=emotions.get)     # highest probability emotion

        cv2.putText(frame, detected, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Play music only if emotion changes
        if detected != current_emotion:
            current_emotion = detected
            print(f"Emotion Detected: {current_emotion}")
            play_music(current_emotion)

    cv2.imshow("Emotion Music Player - Shivi ❤️", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
