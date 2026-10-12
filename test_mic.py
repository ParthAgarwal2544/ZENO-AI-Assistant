import sounddevice as sd
import numpy as np

audio = sd.rec(
    16000,
    samplerate=16000,
    channels=4,
    dtype=np.int16,
    device=1
)

sd.wait()

print("Shape:", audio.shape)
print("Max:", np.max(np.abs(audio)))