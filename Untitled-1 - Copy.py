# ==========================================================
# PURPOSE
# ==========================================================
# This script automatically creates a motivational reel.
#
# INPUTS:
#   1. Background image (Boy.png)
#   2. Motivational text (LINES list)
#
# PROCESS:
#   1. Generate AI voice using Edge TTS
#   2. Convert MP3 to WAV
#   3. Load background image
#   4. Create timed captions
#   5. Add slow zoom effect
#   6. Combine image + captions + voice
#
# OUTPUT:
#   reel.mp4
#
# ==========================================================

import edge_tts
import asyncio
from pydub import AudioSegment
from moviepy import *

# ==========================================================
# FILE PATHS
# ==========================================================
# All input and output files used by the script

IMAGE_PATH = r"C:\Users\admin\OneDrive\Desktop\psychology\Boy.png"

VOICE_MP3 = r"C:\Users\admin\OneDrive\Desktop\psychology\voice.mp3"
VOICE_WAV = r"C:\Users\admin\OneDrive\Desktop\psychology\voice.wav"

OUTPUT_VIDEO = r"C:\Users\admin\OneDrive\Desktop\psychology\reel.mp4"

# ==========================================================
# REEL CONTENT
# ==========================================================
# Each line becomes a caption in the final video

LINES = [
    "Nobody is coming.",
    "Nobody is going to save you.",
    "At some point.",
    "You must become.",
    "Your own rescue plan.",
    "Built In Silence."
]

# Join all lines into one paragraph for AI narration
TEXT = " ".join(LINES)

# ==========================================================
# STEP 1 : GENERATE AI VOICE
# ==========================================================
# Convert text into speech using Microsoft's Edge TTS

async def generate_voice():

    communicate = edge_tts.Communicate(
        text=TEXT,

        # AI voice selection
        voice="en-US-AndrewNeural",

        # Speak slightly slower
        rate="-10%",

        # Slightly deeper tone
        pitch="-5Hz"
    )

    # Save generated narration
    await communicate.save(VOICE_MP3)

    # Convert MP3 to WAV for MoviePy compatibility
    AudioSegment.from_mp3(
        VOICE_MP3
    ).export(
        VOICE_WAV,
        format="wav"
    )

    print("Voice generated successfully")

# Execute voice generation
asyncio.run(generate_voice())

# ==========================================================
# STEP 2 : LOAD GENERATED AUDIO
# ==========================================================
# Audio duration determines video duration

audio = AudioFileClip(VOICE_WAV)

duration = audio.duration

print(f"Audio Duration = {duration:.2f} seconds")

# ==========================================================
# STEP 3 : CREATE BACKGROUND IMAGE CLIP
# ==========================================================
# Use a single image as the reel background

bg = (
    ImageClip(IMAGE_PATH)
    .resized(height=1920)
    .with_duration(duration)
)

# ==========================================================
# STEP 4 : ADD SLOW CINEMATIC ZOOM
# ==========================================================
# Scale image gradually from 100% to 105%

bg = bg.resized(
    lambda t: 1 + 0.05 * t / duration
)

# ==========================================================
# STEP 5 : CREATE CAPTIONS
# ==========================================================
# Display one caption at a time

clips = []

# Divide total audio duration equally across lines
line_duration = duration / len(LINES)

for i, line in enumerate(LINES):

    txt = (
        TextClip(
            text=line,

            # Caption appearance
            font_size=90,
            color="white",

            # Black outline for readability
            stroke_color="black",
            stroke_width=4,

            # Wrap long text automatically
            size=(950, None),

            method="caption"
        )

        # Position caption near bottom of reel
        .with_position(("center", 1450))

        # Start time for this caption
        .with_start(i * line_duration)

        # How long this caption stays visible
        .with_duration(line_duration)
    )

    clips.append(txt)

# ==========================================================
# STEP 6 : COMBINE EVERYTHING
# ==========================================================
# Layer order:
#
# Background Image
# + Captions
#
# Creates video without audio

video = CompositeVideoClip(
    [bg] + clips,
    size=(1080, 1920)
)

# ==========================================================
# STEP 7 : ADD NARRATION
# ==========================================================
# Attach generated voice to video

video = video.with_audio(audio)

# ==========================================================
# STEP 8 : EXPORT FINAL REEL
# ==========================================================
# Save reel in MP4 format

video.write_videofile(
    OUTPUT_VIDEO,

    fps=30,

    codec="libx264",

    audio_codec="aac"
)

print("✅ Reel Created Successfully")
print(f"Output File: {OUTPUT_VIDEO}")