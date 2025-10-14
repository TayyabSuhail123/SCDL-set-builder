import os
import librosa
import numpy as np

# Camelot wheel for harmonic compatibility
CAMELOT_WHEEL = {
    'A♯0': ['F0', 'D♯0', 'A♯0'],
    'C0': ['G0', 'F0', 'C0'],
    'D♯0': ['A♯0', 'G♯0', 'D♯0'],
    'F0': ['C0', 'A♯0', 'F0'],
    'G0': ['C0', 'D0', 'G0'],
    'G♯0': ['D♯0', 'C♯0', 'G♯0'],
    # Add more keys as needed
}

def is_harmonically_compatible(key1, key2):
    return key2 in CAMELOT_WHEEL.get(key1, [])

def analyze_tracks(directory):
    tracks = []
    for filename in os.listdir(directory):
        if filename.lower().endswith('.mp3'):
            path = os.path.join(directory, filename)
            if not os.path.isfile(path):
                continue
            try:
                y, sr = librosa.load(path, duration=120)
                tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
                chroma = librosa.feature.chroma_stft(y=y, sr=sr)
                key_index = int(chroma.mean(axis=1).argmax())
                key = librosa.midi_to_note(key_index + 12)
                energy = float(np.std(y))
                tracks.append({
                    "title": filename,
                    "bpm": round(float(tempo)),
                    "key": key,
                    "energy": round(energy, 2)
                })
            except Exception as e:
                print(f"Error analyzing {filename}: {e}")
    return tracks
