import subprocess
import webbrowser


def execute_command(command):
    command = command.lower()

    # Websites
    if "youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."

    if "google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google."

    if "chatgpt" in command:
        webbrowser.open("https://chatgpt.com")
        return "Opening ChatGPT."

    # Applications
    if "chrome" in command:
        subprocess.Popen(
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )
        return "Opening Chrome."

    if "vscode" in command or "visual studio code" in command:
        subprocess.Popen("code")
        return "Opening VS Code."

    return None