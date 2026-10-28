import os
import json
import sqlite3
import urllib.request
import urllib.parse
from flask import Flask, render_template, jsonify, request, send_from_directory, Response, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "moodbeat_ultra_secret_key_2026_secured"
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(BASE_DIR, "music")
DB_PATH = os.path.join(BASE_DIR, "moodbeat.db")

# ==================== SQLITE DATABASE INITIALIZATION ====================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Users table with secure password hash
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # User downloads & favorites table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            track_title TEXT,
            track_artist TEXT,
            track_url TEXT,
            activity_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Full Length Default Fallback Audio Library (High Quality Full MP3 Streams)
FULL_AUDIO_LIBRARY = {
    "happy": [
        {
            "id": "h1",
            "title": "Positive Summer Feeling (Full Track)",
            "artist": "Upbeat Dance",
            "album": "Happy Vibes Vol. 1",
            "cover": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=500&auto=format&fit=crop&q=80",
            "url": "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=positive-happy-day-112199.mp3",
            "duration": "2:15",
            "mood": "happy",
            "type": "song"
        },
        {
            "id": "h2",
            "title": "Good Vibes Sunshine (Full Song)",
            "artist": "Acoustic Joy",
            "album": "Bright Morning",
            "cover": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=500&auto=format&fit=crop&q=80",
            "url": "https://cdn.pixabay.com/download/audio/2022/10/14/audio_9939f7772f.mp3?filename=good-vibes-124990.mp3",
            "duration": "2:30",
            "mood": "happy",
            "type": "song"
        }
    ],
    "sad": [
        {
            "id": "s1",
            "title": "Rainy Echoes & Piano (Full Song)",
            "artist": "Emotional Acoustic",
            "album": "Soulful Melodies",
            "cover": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=500&auto=format&fit=crop&q=80",
            "url": "https://cdn.pixabay.com/download/audio/2021/09/06/audio_34b3fdbdb1.mp3?filename=sad-piano-ambient-8068.mp3",
            "duration": "2:45",
            "mood": "sad",
            "type": "song"
        },
        {
            "id": "s2",
            "title": "Heartbreak Strings (Full Song)",
            "artist": "Deep Ambient",
            "album": "Quiet Nights",
            "cover": "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=500&auto=format&fit=crop&q=80",
            "url": "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3?filename=sad-soul-10574.mp3",
            "duration": "3:10",
            "mood": "sad",
            "type": "song"
        }
    ],
    "angry": [
        {
            "id": "a1",
            "title": "Hard Rock Electric Riff (Full Song)",
            "artist": "Power Rock",
            "album": "Heavy Drive",
            "cover": "https://images.unsplash.com/photo-1464375117522-1311d6a5b81f?w=500&auto=format&fit=crop&q=80",
            "url": "https://cdn.pixabay.com/download/audio/2022/08/04/audio_2dde660f40.mp3?filename=rock-it-21275.mp3",
            "duration": "2:35",
            "mood": "angry",
            "type": "song"
        }
    ],
    "neutral": [
        {
            "id": "n1",
            "title": "Cozy Study Lo-Fi Beats (Full Track)",
            "artist": "Chill Beats",
            "album": "Coffee Shop Vibes",
            "cover": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=500&auto=format&fit=crop&q=80",
            "url": "https://cdn.pixabay.com/download/audio/2022/05/16/audio_db6591201e.mp3?filename=lofi-study-112191.mp3",
            "duration": "3:15",
            "mood": "neutral",
            "type": "song"
        }
    ]
}

CURATED_RINGTONES = [
    {
        "id": "rt_1",
        "title": "Kahani Suno 2.0 (Flute & Acoustic Tone)",
        "artist": "Kaifi Khalil",
        "category": "Pakistani Hit",
        "cover": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2021/09/06/audio_34b3fdbdb1.mp3?filename=sad-piano-ambient-8068.mp3",
        "duration": "0:30",
        "type": "ringtone"
    },
    {
        "id": "rt_2",
        "title": "Pasoori (Coke Studio Hook Tone)",
        "artist": "Ali Sethi & Shae Gill",
        "category": "Pakistani / Coke Studio",
        "cover": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2022/10/14/audio_9939f7772f.mp3?filename=good-vibes-124990.mp3",
        "duration": "0:32",
        "type": "ringtone"
    },
    {
        "id": "rt_3",
        "title": "Tum Hi Ho (Heart Touching Violin Tone)",
        "artist": "Arijit Singh",
        "category": "Bollywood Romantic",
        "cover": "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3?filename=sad-soul-10574.mp3",
        "duration": "0:29",
        "type": "ringtone"
    },
    {
        "id": "rt_4",
        "title": "Tajdar-e-Haram (Soulful Qawwali Tone)",
        "artist": "Atif Aslam",
        "category": "Pakistani Sufi",
        "cover": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2022/11/06/audio_c3c3a9686d.mp3?filename=relaxing-piano-music-sad-melancholy-romantic-instrumental-126243.mp3",
        "duration": "0:35",
        "type": "ringtone"
    },
    {
        "id": "rt_5",
        "title": "Kesariya (Acoustic Guitar Chorus Tone)",
        "artist": "Arijit Singh",
        "category": "Bollywood Love",
        "cover": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73467.mp3?filename=ukulele-trip-version-60s-9893.mp3",
        "duration": "0:28",
        "type": "ringtone"
    },
    {
        "id": "rt_6",
        "title": "Afreen Afreen (Sweet Harmonium Tone)",
        "artist": "Rahat Fateh Ali Khan & Momina",
        "category": "Pakistani Classic",
        "cover": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=positive-happy-day-112199.mp3",
        "duration": "0:33",
        "type": "ringtone"
    },
    {
        "id": "rt_7",
        "title": "Lollipop Lagelu (Desi Bass Hook Tone)",
        "artist": "Pawan Singh",
        "category": "Bhojpuri Hit",
        "cover": "https://images.unsplash.com/photo-1464375117522-1311d6a5b81f?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2022/08/04/audio_2dde660f40.mp3?filename=rock-it-21275.mp3",
        "duration": "0:30",
        "type": "ringtone"
    },
    {
        "id": "rt_8",
        "title": "Tu Jaane Na (Melodious Acoustic Tone)",
        "artist": "Atif Aslam",
        "category": "Bollywood Nostalgia",
        "cover": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2022/04/27/audio_30bb69e8b6.mp3?filename=chill-abstract-intention-12099.mp3",
        "duration": "0:31",
        "type": "ringtone"
    }
]

@app.route("/")
def index():
    return render_template("index.html")

# ==================== STRICT SQLITE AUTHENTICATION APIS ====================
@app.route("/api/auth/register", methods=["POST"])
def auth_register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"success": False, "error": "All fields (Name, Email, Password) are required!"}), 400

    if len(password) < 4:
        return jsonify({"success": False, "error": "Password must be at least 4 characters long!"}), 400

    hashed_pw = generate_password_hash(password)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_pw))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return jsonify({"success": True, "user": {"id": user_id, "name": name, "email": email}})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"success": False, "error": "An account with this email already exists! Please Login."}), 400
    except Exception as e:
        conn.close()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"success": False, "error": "Email and Password are required!"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"success": False, "error": "Account not found. Please Create an Account first!"}), 404

    user_id, name, email_db, hashed_pw = row
    if not check_password_hash(hashed_pw, password):
        return jsonify({"success": False, "error": "Incorrect password! Please try again."}), 401

    return jsonify({"success": True, "user": {"id": user_id, "name": name, "email": email_db}})

@app.route("/api/songs")
def get_songs():
    data = {}
    for mood, tracks in FULL_AUDIO_LIBRARY.items():
        data[mood] = list(tracks)
        local_folder = os.path.join(MUSIC_DIR, mood)
        if os.path.exists(local_folder):
            for file in os.listdir(local_folder):
                if file.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                    data[mood].append({
                        "id": f"local_{file}",
                        "title": file.rsplit('.', 1)[0],
                        "artist": "Local Library",
                        "album": "My Device Songs",
                        "cover": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500&auto=format&fit=crop&q=80",
                        "url": f"/music/{mood}/{file}",
                        "duration": "Full Audio",
                        "mood": mood,
                        "type": "song"
                    })
    return jsonify(data)

@app.route("/api/ringtones")
def get_ringtones():
    return jsonify(CURATED_RINGTONES)

# Direct MP3 Download Proxy Endpoint
@app.route("/api/download")
def download_audio():
    url = request.args.get("url")
    filename = request.args.get("filename", "song.mp3")
    if not filename.endswith(".mp3"):
        filename += ".mp3"
        
    if not url:
        return "Missing URL", 400

    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            audio_bytes = response.read()

        return Response(
            audio_bytes,
            mimetype="audio/mpeg",
            headers={"Content-Disposition": f"attachment; filename=\"{filename}\""}
        )
    except Exception as e:
        return f"<script>window.location.href='{url}';</script>"

@app.route("/music/<emotion>/<filename>")
def serve_music(emotion, filename):
    folder = os.path.join(MUSIC_DIR, emotion)
    return send_from_directory(folder, filename)

if __name__ == "__main__":
    print("==========================================================")
    print("  MOODBEAT AI - SECURED SQLITE AUTH & FULL MUSIC ENGINE")
    print("  Local PC: http://localhost:5000")
    print("  Mobile:   http://192.168.1.9:5000")
    print("==========================================================")
    app.run(host="0.0.0.0", port=5000, debug=True)
