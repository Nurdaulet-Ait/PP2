import math
import wave
import struct
import os

BASE_DIR = os.path.dirname(__file__)
MUSIC_DIR = os.path.join(BASE_DIR, 'music')
os.makedirs(MUSIC_DIR, exist_ok=True)

sample_rate = 44100
seconds = 4
tracks = [
    ('track1.wav', 440),
    ('track2.wav', 523),
    ('track3.wav', 659),
]

for filename, freq in tracks:
    path = os.path.join(MUSIC_DIR, filename)
    with wave.open(path, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for i in range(sample_rate * seconds):
            value = int(16000 * math.sin(2 * math.pi * freq * i / sample_rate))
            wav.writeframes(struct.pack('<h', value))
    print('Created:', path)
