import edge_tts
import asyncio
import os

SAVE_FOLDER = r"C:\Users\admin\OneDrive\Desktop\psychology\Voice_Samples"

os.makedirs(SAVE_FOLDER, exist_ok=True)

TEXT = """
You have power over your mind.

Not outside events.

Realize this.

And you will find strength.

The strongest men are not the loudest.

They are the most disciplined.

Built in silence.
"""

voices = [
    "en-US-BrianMultilingualNeural",
    "en-US-ChristopherNeural",
    "en-US-AndrewNeural",
    "en-US-GuyNeural",
    "en-US-RogerNeural",
    "en-US-SteffanNeural",
    "en-US-EricNeural",
    "en-GB-RyanNeural",
    "en-GB-ThomasNeural",
    "en-AU-WilliamNeural",
    "en-CA-LiamNeural",
    "en-IN-PrabhatNeural"
]

async def main():

    for voice in voices:

        try:

            filename = os.path.join(
                SAVE_FOLDER,
                f"{voice}.wav"
            )

            communicate = edge_tts.Communicate(
                text=TEXT,
                voice=voice,
                rate="-10%",
                pitch="-5Hz"
            )

            await communicate.save(filename)

            print(f"✅ Saved: {voice}")

        except Exception as e:

            print(f"❌ Failed: {voice}")
            print(e)

    print("\n🎉 Finished generating all available voices!")

asyncio.run(main())
