"""
Configuration settings for the ZENO AI Desktop Assistant.
"""

# Branding & Identity
ASSISTANT_NAME = "ZENO"
ASSISTANT_DISPLAY_NAME = "Zeno"
WAKE_WORD = "Hey Zeno"

# Whisper-based wake word triggers & phonetically similar matches
WAKE_WORDS = [
    "zeno",
    "hey zeno",
    "xeno",
    "zeeno",
    "ceno",
    "zino",
    "zeena",
]

# Audio settings
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280

# OpenWakeWord configuration
OPENWAKEWORD_MODEL = "hey_zeno"
