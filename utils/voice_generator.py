from gtts import gTTS
from pydub import AudioSegment
import os
from gtts import gTTS
import os

def generate_welcome_audio():
    text = "Welcome to Walmart Voice Assistant. Tap the mic and tell me where you want to go."
    tts = gTTS(text)
    tts.save("static/audio/welcome.mp3")


def generate_voice(instructions, output_path='static/audio/final_instructions.mp3'):
    filenames = []
    pause = AudioSegment.silent(duration=600)

    for i, instruction in enumerate(instructions):
        tts = gTTS(instruction, slow=False, lang='en')
        filename = f"temp_instruction_{i}.mp3"
        tts.save(filename)
        filenames.append(filename)

    final_audio = AudioSegment.empty()
    for file in filenames:
        final_audio += AudioSegment.from_mp3(file)
        final_audio += pause
        os.remove(file)

    final_audio.export(output_path, format="mp3")
    return output_path
