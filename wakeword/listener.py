import sys
import os

# Allow access to project folders like ai/ and config/
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

from command_listener import listen_for_command
from ai.assistant import ask_zeno
from config.settings import WAKE_WORDS

# Better accuracy model
model = WhisperModel(
    "medium",
    device="cpu",
    compute_type="int8"
)

print("🤖 Zeno listener started...")


while True:
    try:
        print("\n🎤 Listening for wake word...")

        duration = 2
        sample_rate = 16000

        audio = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype=np.int16
        )

        sd.wait()

        write("temp.wav", sample_rate, audio)

        segments, _ = model.transcribe(
            "temp.wav",
            language="en"
        )

        text = " ".join(segment.text for segment in segments)

        print("Heard:", text)

        wake_words = WAKE_WORDS

        if any(word in text.lower() for word in wake_words):

            print("🚀 WAKE WORD DETECTED!")

            # Zeno acknowledges
            ask_zeno("Reply only with: Yes, Parth?")

            # Listen for actual command
            command = listen_for_command()

            print("📝 Command:", command)

            if not command:
                continue

            command = command.strip()

            # Ignore accidental wake word in command
            for word in wake_words:
                command = command.replace(word, "")

            command = command.strip()

            if not command:
                continue

            answer = ask_zeno(command)

            print("🤖 Zeno:", answer)

    except Exception as e:
        print("\n❌ ERROR:")
        print(type(e).__name__)
        print(str(e))