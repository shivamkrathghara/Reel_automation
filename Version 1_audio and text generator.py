import os
import random
import asyncio
import edge_tts

from moviepy import (
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    ColorClip
)

# ==========================================
# PATHS
# ==========================================

WORKING_DIR = r"C:\Users\admin\OneDrive\Desktop\psychology"

IMAGE_FOLDER = os.path.join(
    WORKING_DIR,
    "Sample Images"
)

VOICE_PATH = os.path.join(
    WORKING_DIR,
    "voice.mp3"
)

OUTPUT_PATH = os.path.join(
    WORKING_DIR,
    "reel.mp4"
)

# ==========================================
# STORY
# ==========================================


LINES = [
    "At 20 years old...",
    "a boy asked an old Stoic...",
    '"How do I become respected?"',
    "The old man handed him a seed...",
    "and said...",
    '"Plant it."',
    "The boy laughed...",
    '"A seed won\'t make me strong."',
    "The old man smiled...",
    "and replied...",
    '"Exactly."',
    '"Neither will talking about your dreams."',
    "Years passed...",
    "The seed became a giant tree.",
    "And the boy finally understood...",
    "While others were busy talking...",
    "the tree was busy growing.",
    "At 20...",
    "Don't focus on being noticed.",
    "Focus on becoming impossible to ignore."
]

TEXT = " ".join(LINES)

# ==========================================
# GENERATE VOICE
# ==========================================

async def generate_voice():

    communicate = edge_tts.Communicate(
        text=TEXT,
        voice="en-US-JennyNeural",
        rate="-20%"
    )

    await communicate.save(VOICE_PATH)

asyncio.run(generate_voice())

print("Voice Generated")

# ==========================================
# AUDIO
# ==========================================

audio = AudioFileClip(VOICE_PATH)

duration = audio.duration

print(f"Audio Duration: {duration:.2f}")

# ==========================================
# LOAD IMAGES
# ==========================================

all_images = [
    os.path.join(IMAGE_FOLDER, f)
    for f in os.listdir(IMAGE_FOLDER)
    if f.lower().endswith(
        (".png", ".jpg", ".jpeg", ".webp")
    )
]

if len(all_images) == 0:
    raise Exception(
        "No images found in Sample Images folder"
    )

random.shuffle(all_images)

print(f"Found {len(all_images)} images")

if len(all_images) == 1:

    print("Using single image mode")

    img = all_images[0]

    img_clip = ImageClip(img)

    img_w, img_h = img_clip.size

    scale = min(
        1080 / img_w,
        1920 / img_h
    )

    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    foreground = (
        img_clip
        .resized((new_w, new_h))
        .with_duration(duration)
        .with_position(("center", "center"))
    )

    foreground = foreground.resized(
        lambda t: 1 + (0.08 * t / duration)
    )

    background = ColorClip(
        size=(1080, 1920),
        color=(15, 15, 15),
        duration=duration
    )

    background_video = CompositeVideoClip(
        [background, foreground],
        size=(1080, 1920)
    )

else:

# ==========================================
# IMAGE SLIDESHOW
# ==========================================

CHANGE_EVERY = 3.5

image_clips = []

current_time = 0
image_index = 0

while current_time < duration:

    img = all_images[
        image_index % len(all_images)
    ]

    clip_duration = min(
        CHANGE_EVERY,
        duration - current_time
    )

    print(
        f"Using {os.path.basename(img)}"
    )

    img_clip = ImageClip(img)

    img_w, img_h = img_clip.size

    scale = min(
        1080 / img_w,
        1920 / img_h
    )

    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    foreground = (
        img_clip
        .resized((new_w, new_h))
        .with_duration(clip_duration)
        .with_position(("center", "center"))
    )

    foreground = foreground.resized(
        lambda t: 1 + (0.08 * t / clip_duration)
    )

    background = ColorClip(
        size=(1080, 1920),
        color=(15, 15, 15),
        duration=clip_duration
    )

    clip = CompositeVideoClip(
        [background, foreground],
        size=(1080, 1920)
    )

    image_clips.append(clip)

    current_time += clip_duration
    image_index += 1

background_video = concatenate_videoclips(
    image_clips,
    method="compose"
)

# ==========================================
# DARK OVERLAY
# ==========================================

dark_overlay = (
    ColorClip(
        size=(1080, 1920),
        color=(0, 0, 0),
        duration=duration
    )
    .with_opacity(0.20)
)

# ==========================================
# CAPTIONS
# ==========================================

caption_clips = []

line_duration = duration / len(LINES)

for i, line in enumerate(LINES):

    txt = (
        TextClip(
            text=line,
            font_size=44,
            color="white",
            stroke_color="black",
            stroke_width=4,
            size=(900, None),
            method="caption"
        )
        .with_position(("center", 1350))
        .with_start(i * line_duration)
        .with_duration(line_duration)
    )

    caption_clips.append(txt)

# ==========================================
# FINAL VIDEO
# ==========================================

final_video = CompositeVideoClip(
    [background_video, dark_overlay] + caption_clips,
    size=(1080, 1920)
)

final_video = final_video.with_audio(audio)

# ==========================================
# EXPORT
# ==========================================

final_video.write_videofile(
    OUTPUT_PATH,
    fps=30,
    codec="libx264",
    audio_codec="aac"
)

print("Reel Created Successfully")
print(OUTPUT_PATH)