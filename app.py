from flask import Flask, render_template

app = Flask(__name__)

import os
import yaml

def load_songs():
    songs = []
    songs_dir = os.path.join(os.path.dirname(__file__), 'songs')

    if not os.path.exists(songs_dir):
        return []

    files = [f for f in os.listdir(songs_dir) if f.endswith('.txt') or not os.path.isdir(os.path.join(songs_dir, f))]
    files.sort()

    for filename in files:
        filepath = os.path.join(songs_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            _, front_matter, lyrics = content.split('---', 2)
            metadata = yaml.safe_load(front_matter)
            
            songs.append({
                "id": metadata['id'],
                "title": metadata['title'],
                "lyrics": lyrics.strip()
            })
        except (ValueError, yaml.YAMLError, KeyError) as e:
            print(f"Warning: Could not parse {filename}: {e}")
            continue

    return sorted(songs, key=lambda s: s['id'])

songs = load_songs()

@app.route('/')
def index():
    return render_template('index.html', songs=songs)

@app.route('/song/<int:song_id>')
def song(song_id):
    song = next((s for s in songs if s['id'] == song_id), None)
    if song:
        return render_template('song.html', song=song)
    return "Song not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
