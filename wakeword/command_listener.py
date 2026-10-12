import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

model = WhisperModel(
    "medium",
    device="cpu",
    compute_type="int8"
)


def listen_for_command():
    print("🎤 Listening for command...")

    duration = 3
    sample_rate = 16000

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype=np.int16,
        device=1
    )

    sd.wait()

    write("command.wav", sample_rate, audio)

    segments, _ = model.transcribe(
        "command.wav",
        language="en",
        beam_size=5
    )

    text = " ".join(
        segment.text for segment in segments
    ).strip()

    print("🎙️ Heard Command:", text)

    return text