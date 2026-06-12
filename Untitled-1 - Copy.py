
import edge_tts
import asyncio
from pydub import AudioSegment
from moviepy import *

# ==========================================
# PATHS
# ==========================================

IMAGE_PATH = r"C:\Users\admin\OneDrive\Desktop\psychology\Boy.png"

VOICE_MP3 = r"C:\Users\admin\OneDrive\Desktop\psychology\voice.mp3"
VOICE_WAV = r"C:\Users\admin\OneDrive\Desktop\psychology\voice.wav"

OUTPUT_VIDEO = r"C:\Users\admin\OneDrive\Desktop\psychology\reel.mp4"

# ==========================================
# REEL SCRIPT
# ==========================================

LINES = [
    "Nobody is coming.",
    "Nobody is going to save you.",
    "At some point.",
    "You must become.",
    "Your own rescue plan.",
    "Built In Silence."
]

TEXT = " ".join(LINES)

# ==========================================
# GENERATE VOICE
# ==========================================

async def generate_voice():

    communicate = edge_tts.Communicate(
        text=TEXT,
        voice="en-US-AndrewNeural",
        rate="-10%",
        pitch="-5Hz"
    )

    await communicate.save(VOICE_MP3)

    AudioSegment.from_mp3(
        VOICE_MP3
    ).export(
        VOICE_WAV,
        format="wav"
    )

    print("Voice generated")

asyncio.run(generate_voice())

# ==========================================
# LOAD AUDIO
# ==========================================

audio = AudioFileClip(VOICE_WAV)

duration = audio.duration

# ==========================================
# IMAGE
# ==========================================

bg = (
    ImageClip(IMAGE_PATH)
    .resized(height=1920)
    .with_duration(duration)
)

# Slow zoom
bg = bg.resized(lambda t: 1 + 0.05 * t / duration)

# ==========================================
# CAPTIONS
# ==========================================

clips = []

line_duration = duration / len(LINES)

for i, line in enumerate(LINES):

    txt = (
        TextClip(
            text=line,
            font_size=90,
            color="white",
            stroke_color="black",
            stroke_width=4,
            size=(950, None),
            method="caption"
        )
        .with_position(("center", 1450))
        .with_start(i * line_duration)
        .with_duration(line_duration)
    )

    clips.append(txt)

# ==========================================
# FINAL VIDEO
# ==========================================

video = CompositeVideoClip(
    [bg] + clips,
    size=(1080, 1920)
)

video = video.with_audio(audio)

video.write_videofile(
    OUTPUT_VIDEO,
    fps=30,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Reel Created")
print(OUTPUT_VIDEO)

