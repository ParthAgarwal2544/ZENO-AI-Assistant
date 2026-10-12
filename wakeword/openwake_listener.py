import sys
import os
import threading
import time

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from openwakeword.model import Model
import sounddevice as sd
import numpy as np

from command_listener import listen_for_command
from ai.assistant import ask_zeno
from actions.system_actions import run_command

# Custom model path check for Hey Zeno
CUSTOM_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "hey_zeno.onnx")

if os.path.exists(CUSTOM_MODEL_PATH):
    model = Model(wakeword_models=[CUSTOM_MODEL_PATH], inference_framework="onnx")
    TARGET_WAKEWORD_KEY = "hey_zeno"
    print(f"📦 Loaded custom wake-word model: {CUSTOM_MODEL_PATH}")
else:
    # Default openWakeWord pretrained models
    model = Model(inference_framework="onnx")
    # Note: openWakeWord has no pretrained 'hey_zeno' model.
    # Pretrained models: ['alexa', 'hey_mycroft', 'hey_jarvis', 'hey_rhasspy', 'timer', 'weather']
    if "hey_zeno" in model.models:
        TARGET_WAKEWORD_KEY = "hey_zeno"
    else:
        TARGET_WAKEWORD_KEY = "hey_jarvis"
        print("⚠️ [OpenWakeWord] Pretrained 'hey_zeno' model is not bundled with openWakeWord by default.")
        print("⚠️ To trigger via openWakeWord, train/download a custom 'hey_zeno.onnx' model and place it in 'wakeword/models/'.")
        print("⚠️ Falling back to monitoring 'hey_jarvis' model channel for testing compatibility.\n")

print("🤖 Zeno Wake Listener Started")
print("🎤 Listening for 'Hey Zeno'...")

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280

last_detection = 0
is_busy = False


def handle_zeno():
    global is_busy

    try:
        print("🎤 Listening for command...")

        # Zeno acknowledgement
        print("ready")

        command = listen_for_command()

        if not command:
            print("❌ No command heard")
            return

        print("📝 Command:", command)

        # Check system commands first
        result = run_command(command)

        if result:
            print("🤖", result)

            ask_zeno(
                f"Reply ONLY with: {result}"
            )
            return

        # Send normal questions to Ollama
        answer = ask_zeno(command)

        print("🤖 Zeno:", answer)

    except Exception as e:
        print(" ERROR:", e)

    finally:
        is_busy = False

# Backward compatibility alias
handle_jarvis = handle_zeno


def audio_callback(indata, frames, time_info, status):
    global last_detection
    global is_busy

    if status:
        print(status)

    # Use first microphone channel
    audio = indata[:, 0].astype(np.int16)

    prediction = model.predict(audio)

    score = prediction.get(TARGET_WAKEWORD_KEY, 0.0)

    # Uncomment for debugging
    # print(f"Zeno Score ({TARGET_WAKEWORD_KEY}): {score:.4f}")

    if score > 0.30 and not is_busy:

        # Prevent repeated triggers
        if time.time() - last_detection < 5:
            return

        last_detection = time.time()
        is_busy = True

        print("\n🚀 HEY ZENO DETECTED!")

        threading.Thread(
            target=handle_zeno,
            daemon=True
        ).start()


with sd.InputStream(
    samplerate=SAMPLE_RATE,
    blocksize=CHUNK_SIZE,
    device=1,
    channels=4,
    dtype="int16",
    callback=audio_callback
):
    while True:
        sd.sleep(1000)