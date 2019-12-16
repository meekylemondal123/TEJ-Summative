import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone()


with mic as source:
    while True:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        command = r.recognize_google(audio)

        if command == "stop":
            break
        else:
            if "weather" in command:
                print ("1 degrees C")
    
