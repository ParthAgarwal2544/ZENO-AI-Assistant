from actions.app_launcher import execute_command
import requests
import pyttsx3


def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("Speech Error:", e)

def ask_zeno(message):

    command_result = execute_command(message)

    if command_result:
        speak(command_result)
        return command_result

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": message,
            "stream": False
        }
    )

    answer = response.json()["response"]

    speak(answer)

    return answer

# Backward compatibility alias
ask_jarvis = ask_zeno