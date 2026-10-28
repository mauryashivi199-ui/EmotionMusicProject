import os
import json
import urllib.request
import urllib.parse
from flask import Flask, render_template, jsonify, request, send_from_directory, Response
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(BASE_DIR, "music")

# Curated High Quality Full Songs & Popular Ringtones
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

# Dedicated Popular Free Ringtones
CURATED_RINGTONES = [
    {
        "id": "rt_1",
        "title": "Bhojpuri Dhamaal Bass Ringtone",
        "artist": "Desi Beat Tone",
        "category": "Bhojpuri",
        "cover": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2022/01/26/audio_d0c6ff1101.mp3?filename=sport-rock-workout-10700.mp3",
        "duration": "0:30",
        "type": "ringtone"
    },
    {
        "id": "rt_2",
        "title": "Romantic Flute & Violin Ringtone",
        "artist": "Soulful Melody",
        "category": "Romantic",
        "cover": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2021/09/06/audio_34b3fdbdb1.mp3?filename=sad-piano-ambient-8068.mp3",
        "duration": "0:28",
        "type": "ringtone"
    },
    {
        "id": "rt_3",
        "title": "iPhone Stylish Ambient Chime",
        "artist": "Apple Vibe",
        "category": "Caller Tune",
        "cover": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73467.mp3?filename=ukulele-trip-version-60s-9893.mp3",
        "duration": "0:25",
        "type": "ringtone"
    },
    {
        "id": "rt_4",
        "title": "Sad Emotional Heartbeat Tone",
        "artist": "Arijit Vibe Tone",
        "category": "Emotional",
        "cover": "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3?filename=sad-soul-10574.mp3",
        "duration": "0:32",
        "type": "ringtone"
    },
    {
        "id": "rt_5",
        "title": "KGF Action Power BGM Ringtone",
        "artist": "Heavy Mass Bass",
        "category": "Action BGM",
        "cover": "https://images.unsplash.com/photo-1464375117522-1311d6a5b81f?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2022/08/04/audio_2dde660f40.mp3?filename=rock-it-21275.mp3",
        "duration": "0:34",
        "type": "ringtone"
    },
    {
        "id": "rt_6",
        "title": "Chill Morning Acoustic Ringtone",
        "artist": "Sweet Melody",
        "category": "Alarm / Tune",
        "cover": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=500",
        "url": "https://cdn.pixabay.com/download/audio/2022/10/14/audio_9939f7772f.mp3?filename=good-vibes-124990.mp3",
        "duration": "0:29",
        "type": "ringtone"
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/songs")
def get_songs():
    """Return cloud full tracks + local music files"""
    data = {}
    for mood, tracks in FULL_AUDIO_LIBRARY.items():
        data[mood] = list(tracks)
        
        # Local files if available
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
        # Fallback: Redirect directly
        return f"<script>window.location.href='{url}';</script>"

@app.route("/music/<emotion>/<filename>")
def serve_music(emotion, filename):
    folder = os.path.join(MUSIC_DIR, emotion)
    return send_from_directory(folder, filename)

if __name__ == "__main__":
    print("==========================================================")
    print("  MOODBEAT AI - FULL MUSIC & RINGTONE DOWNLOAD ENGINE")
    print("  Local PC: http://localhost:5000")
    print("  Mobile:   http://192.168.1.9:5000")
    print("==========================================================")
    app.run(host="0.0.0.0", port=5000, debug=True)
