import edge_tts
import asyncio
import os

BASE_FOLDER = r"C:\Users\admin\OneDrive\Desktop\psychology\Voice_Samples"

TEXT = """
You have power over your mind.

Not outside events.

Realize this.

And you will find strength.

The strongest men are not the loudest.

They are the most disciplined.

Built in silence.
"""

VOICE_GROUPS = {

    "Male_Stoic": [
        "en-US-EricNeural",
        "en-US-AndrewNeural",
        "en-US-RogerNeural",
        "en-GB-ThomasNeural",
    ],

    "Male_Narrator": [
        "en-US-GuyNeural",
        "en-US-ChristopherNeural",
        "en-US-BrianMultilingualNeural",
        "en-AU-WilliamNeural",
    ],

    "Male_Young": [
        "en-US-JasonNeural",
        "en-CA-LiamNeural",
        "en-IN-PrabhatNeural",
    ],

    "Female_Soft": [
        "en-US-JennyNeural",
        "en-US-MichelleNeural",
        "en-US-AnaNeural",
    ],

    "Female_Psychologist": [
        "en-US-AriaNeural",
        "en-US-JennyNeural",
        "en-GB-SoniaNeural",
    ],

    "Female_Storytelling": [
        "en-US-EmmaNeural",
        "en-AU-NatashaNeural",
        "en-CA-ClaraNeural",
    ]
}


async def generate_voice(text, voice, output_file):

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate="-10%",
        pitch="-5Hz"
    )

    await communicate.save(output_file)


async def main():

    for folder_name, voices in VOICE_GROUPS.items():

        folder_path = os.path.join(
            BASE_FOLDER,
            folder_name
        )

        os.makedirs(folder_path, exist_ok=True)

        print(f"\nGenerating {folder_name} voices")

        for voice in voices:

            try:

                output_file = os.path.join(
                    folder_path,
                    f"{voice}.mp3"
                )

                await generate_voice(
                    TEXT,
                    voice,
                    output_file
                )

                print(f"✅ {voice}")

            except Exception as e:

                print(f"❌ {voice}")
                print(e)

    print("\n🎉 All voice samples generated.")


asyncio.run(main())