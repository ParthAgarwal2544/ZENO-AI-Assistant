import pyttsx3

engine = pyttsx3.init()

while True:
    text = input("Say something: ")
    engine.say(text)
    engine.runAndWait()