import sounddevice as sd

for i, device in enumerate(sd.query_devices()):
    if device['max_input_channels'] > 0:
        print(f"{i}: {device['name']} | IN={device['max_input_channels']}")