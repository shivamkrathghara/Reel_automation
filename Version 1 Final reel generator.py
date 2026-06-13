
# from moviepy import *

# # =====================================
# # PATHS
# # =====================================

# IMAGE_PATH = r"C:\Users\admin\OneDrive\Desktop\psychology\Boy.png"

# AUDIO_PATH = r"C:\Users\admin\OneDrive\Desktop\psychology\Voice_Samples\en-CA-LiamNeural.mp3"

# OUTPUT_PATH = r"C:\Users\admin\OneDrive\Desktop\psychology\reel.mp4"

# # =====================================
# # CAPTIONS
# # =====================================

# LINES = [
#     "Nobody is coming.",
#     "Nobody is going to save you.",
#     "At some point.",
#     "You must become.",
#     "Your own rescue plan.",
#     "Built In Silence."
# ]

# # =====================================
# # AUDIO
# # =====================================

# audio = AudioFileClip(AUDIO_PATH)

# duration = audio.duration

# print("Audio Duration:", duration)

# # =====================================
# # BACKGROUND IMAGE
# # =====================================

# bg = (
#     ImageClip(IMAGE_PATH)
#     .resized(height=1920)
#     .with_duration(duration)
# )

# # Cinematic slow zoom
# bg = bg.resized(
#     lambda t: 1 + 0.08 * t / duration
# )

# # =====================================
# # TEXT CLIPS
# # =====================================

# clips = []

# line_duration = duration / len(LINES)

# for i, line in enumerate(LINES):

#     txt = (
#         TextClip(
#             text=line,
#             font_size=90,
#             color="white",
#             stroke_color="black",
#             stroke_width=4,
#             size=(950, None),
#             method="caption"
#         )
#         .with_position(("center", 1450))
#         .with_start(i * line_duration)
#         .with_duration(line_duration)
#     )

#     clips.append(txt)

# # =====================================
# # COMBINE
# # =====================================

# video = CompositeVideoClip(
#     [bg] + clips,
#     size=(1080, 1920)
# )

# video = video.with_audio(audio)

# # =====================================
# # EXPORT
# # =====================================

# video.write_videofile(
#     OUTPUT_PATH,
#     fps=30,
#     codec="libx264",
#     audio_codec="aac"
# )

# print("✅ Reel Created Successfully")
# print("📁", OUTPUT_PATH)


import edge_tts
import asyncio
from moviepy import *

# =====================================
# PATHS
# =====================================

IMAGE_PATH = r"C:\Users\admin\OneDrive\Desktop\psychology\Boy.png"

VOICE_PATH = r"C:\Users\admin\OneDrive\Desktop\psychology\voice.mp3"

OUTPUT_PATH = r"C:\Users\admin\OneDrive\Desktop\psychology\reel.mp4"

# =====================================
# STOIC SCRIPT
# =====================================

LINES = [
    "You cannot control the storm.",
    "You cannot control other people.",
    "You can control your response.",
    "And that is where your power begins."
]

TEXT = " ".join(LINES)

# =====================================
# GENERATE VOICE
# =====================================

async def generate_voice():

    communicate = edge_tts.Communicate(
        text=TEXT,
        voice="en-US-AndrewNeural",
        rate="-10%"
    )

    await communicate.save(VOICE_PATH)

    print("Voice Generated")

asyncio.run(generate_voice())

# =====================================
# LOAD AUDIO
# =====================================

audio = AudioFileClip(VOICE_PATH)

duration = audio.duration

print("Audio Duration:", duration)

# =====================================
# IMAGE
# =====================================

bg = (
    ImageClip(IMAGE_PATH)
    .resized(height=1920)
    .with_duration(duration)
)

# Slow cinematic zoom
bg = bg.resized(
    lambda t: 1 + 0.08 * t / duration
)

# =====================================
# CAPTIONS
# =====================================

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

# =====================================
# FINAL VIDEO
# =====================================

video = CompositeVideoClip(
    [bg] + clips,
    size=(1080, 1920)
)

video = video.with_audio(audio)

video.write_videofile(
    OUTPUT_PATH,
    fps=30,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Reel Created Successfully")
print("📁 Saved at:", OUTPUT_PATH)
