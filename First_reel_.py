
import edge_tts
import asyncio
import numpy as np
import soundfile as sf

from moviepy import *

# =========================================
# PATHS
# =========================================

IMAGE_PATH = r"C:\Users\admin\OneDrive\Desktop\psychology\Boy.png"

VOICE_PATH = r"C:\Users\admin\OneDrive\Desktop\psychology\voice.mp3"

MUSIC_PATH = r"C:\Users\admin\OneDrive\Desktop\psychology\ambient_stoic.wav"

OUTPUT_PATH = r"C:\Users\admin\OneDrive\Desktop\psychology\reel.mp4"

# =========================================
# STOIC QUOTE
# =========================================

LINES = [
    "You cannot control the storm.",
    "You cannot control other people.",
    "You can control your response.",
    "And that is where your power begins."
]

TEXT = " ".join(LINES)

# =========================================
# GENERATE VOICE
# =========================================

async def generate_voice():

    communicate = edge_tts.Communicate(
        text=TEXT,
        voice="en-US-AndrewNeural",
        rate="-10%"
    )

    await communicate.save(VOICE_PATH)

    print("Voice Generated")

asyncio.run(generate_voice())

# =========================================
# GENERATE AMBIENT MUSIC
# =========================================

sample_rate = 44100
duration_music = 30

t = np.linspace(
    0,
    duration_music,
    int(sample_rate * duration_music)
)

layer1 = 0.15 * np.sin(
    2 * np.pi * 110 * t
)

layer2 = 0.08 * np.sin(
    2 * np.pi * 220 * t
)

layer3 = 0.04 * np.sin(
    2 * np.pi * 330 * t
)

layer4 = 0.05 * np.sin(
    2 * np.pi * 0.08 * t
)

ambient = (
    layer1 +
    layer2 +
    layer3 +
    layer4
)

ambient = ambient / np.max(np.abs(ambient))
ambient *= 0.30

sf.write(
    MUSIC_PATH,
    ambient,
    sample_rate
)

print("Ambient Music Generated")

# =========================================
# LOAD AUDIO
# =========================================

voice = AudioFileClip(VOICE_PATH)

duration = voice.duration

music = (
    AudioFileClip(MUSIC_PATH)
    .subclipped(0, duration)
    .with_volume_scaled(0.08)
)

final_audio = CompositeAudioClip(
    [music, voice]
)

# =========================================
# BACKGROUND IMAGE
# =========================================

bg = (
    ImageClip(IMAGE_PATH)
    .resized(height=1920)
    .with_duration(duration)
)

# Cinematic zoom
bg = bg.resized(
    lambda t: 1 + 0.08 * t / duration
)

# =========================================
# DARK OVERLAY
# =========================================

overlay = (
    ColorClip(
        size=(1080, 1920),
        color=(0, 0, 0)
    )
    .with_opacity(0.35)
    .with_duration(duration)
)

# =========================================
# CAPTIONS
# =========================================


# =====================================
# SMART CAPTION TIMING
# =====================================

clips = []

# Count total words
total_words = sum(
    len(line.split())
    for line in LINES
)

current_start = 0

for line in LINES:

    words = len(line.split())

    # Allocate duration proportional to words
    caption_duration = (
        words / total_words
    ) * duration

    txt = (
        TextClip(
            text=line.upper(),
            font_size=100,
            color="white",
            stroke_color="black",
            stroke_width=5,
            size=(950, None),
            method="caption"
        )
        .with_position(("center", 1450))
        .with_start(current_start)
        .with_duration(caption_duration)
    )

    clips.append(txt)

    current_start += caption_duration



# =========================================
# FINAL VIDEO
# =========================================

video = CompositeVideoClip(
    [bg, overlay] + clips,
    size=(1080, 1920)
)

video = video.with_audio(final_audio)

video.write_videofile(
    OUTPUT_PATH,
    fps=30,
    codec="libx264",
    audio_codec="aac"
)

print("===================================")
print("✅ REEL CREATED SUCCESSFULLY")
print("📁", OUTPUT_PATH)
print("===================================")

