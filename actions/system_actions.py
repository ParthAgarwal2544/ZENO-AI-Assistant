import webbrowser
import os

def run_command(command):

    command = command.lower()

    if "youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    if "google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google"

    if "github" in command:
        webbrowser.open("https://github.com")
        return "Opening GitHub"

    if "spotify" in command:
        os.system("start spotify")
        return "Opening Spotify"

    if "chrome" in command:
        os.system("start chrome")
        return "Opening Chrome"

    return None