# 🎵 MoodBeat AI — Intelligent Music, Ringtones & Emotion Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite3-orange.svg)](https://www.sqlite.org/)
[![TailwindCSS](https://img.shields.io/badge/UI-TailwindCSS%203.0-06B6D4.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

**MoodBeat AI** is an ultra-modern, cross-platform intelligent audio streaming web application. It combines real-time facial expression AI detection with high-speed cloud audio indexing, allowing users to experience **100% full-length songs**, authentic **Hindi & Pakistani ringtones**, and **direct device MP3 downloads** protected by a **strict SQLite database authentication system**.

---

## 🌟 Key Features

### 1. 🔐 Strict SQLite Database Authentication (No Passwordless Access)
- **Zero-Bypass Gate**: Users cannot access or stream music without authenticating.
- **SQL Data Persistence**: User registrations and encrypted password credentials are safely stored inside a native SQLite relational database (`moodbeat.db`).
- **Secure Hashing**: Passwords are encrypted using Werkzeug cryptographic PBKDF2 hashes before saving.

### 2. 🎶 100% Full-Length Audio Streaming (No 30-Second Previews)
- Direct high-bitrate **320kbps MP3 stream delivery**.
- Complete 3 to 5+ minute studio official tracks without trial cuts or sudden stops.
- Interactive **Spinning Vinyl Record** player with sound-reactive equalizer visualization.

### 3. 🔍 Universal Multi-Language Search (40+ Tracks Per Query)
- Search across Indian & International artists:
  - **Bollywood**: Arijit Singh, Shreya Ghoshal, Neha Kakkar, Atif Aslam.
  - **Pakistani & Coke Studio**: Kaifi Khalil (*Kahani Suno*), Ali Sethi (*Pasoori*), Rahat Fateh Ali Khan (*Afreen Afreen*).
  - **Regional**: Pawan Singh, Khesari Lal (Bhojpuri), Sidhu Moosewala, Diljit Dosanjh (Punjabi).
  - **Global**: Taylor Swift, Ed Sheeran, Imagine Dragons, The Weeknd.
- Instant 40+ track pagination per search.

### 4. 🔔 Dedicated Ringtone Vault & Search
- Handcrafted popular hook beats, romantic violin tunes, flute solos, and action BGMs.
- Dedicated **"Find Tone"** search bar to find matching caller tunes.

### 5. 📥 1-Click High-Speed MP3 Downloader
- Backend stream proxy enables direct downloading of full songs and ringtones straight to device storage (`Downloads/` folder).
- Offline Vault manager tracks and saves your downloaded audio files.

### 6. 🎭 Face-API Emotion AI Vision
- Runs locally in-browser using neural TinyFaceDetector + FaceExpressionNet.
- Automatically adjusts mood stations based on 4 emotions: **Happy 😊**, **Sad 😢**, **Angry 🔥**, and **Chill ☕**.

---

## 📱 Mobile & Desktop Architecture

MoodBeat AI is designed mobile-first with a native 6-tab bottom navigation bar:
- 🏠 **Home**: Hero banner, top mixes & trending featured tracks.
- 🧭 **Search**: Real-time query search for 40+ full tracks.
- 🔔 **Tones**: Authentic Hindi, Pakistani & regional caller tunes.
- 📥 **Saved**: Download history and offline vault.
- 🎵 **Player**: Vinyl turntable player with scrub timeline and volume sliders.
- 📑 **Playlists**: Liked songs auto-categorized by mood.

---

## 🚀 Quick Setup & Installation

### 1. Clone Repository
```bash
git clone https://github.com/mauryashivi199-ui/EmotionMusicProject.git
cd EmotionMusicProject
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python app.py
```
*Or double click `run_app.bat` on Windows.*

### 4. Open in Browser
- **PC Access**: `http://localhost:5000`
- **Mobile Access (Same Wi-Fi)**: `http://<YOUR_LOCAL_IP>:5000`

---

## 🛡️ Database Schema

The app uses `moodbeat.db` (SQLite3):
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 👤 Author
Developed with ❤️ by **Shivangi Maurya**  
GitHub: [@mauryashivi199-ui](https://github.com/mauryashivi199-ui)
