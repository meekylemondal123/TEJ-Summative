import speech_recognition as sr
# pyowm is the Python friendly version of the OWM API
import pyowm

# This is the API key for the OpenWeatherMap API
owm = pyowm.OWM('2360e244ea17b8c36148779867365372')

r = sr.Recognizer()
mic = sr.Microphone()
mic1 = sr.Microphone()

notesFile = open("C:\\Users\\meeky\\Desktop\\notes.txt", 'w')

with mic as source:
    while True:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        command = r.recognize_google(audio)

        if command == "stop":
            break
        else:
            if "weather" in command:
                to = owm.weather_at_place('Toronto, CA')
                weather = to.get_weather()
                print (weather.get_temperature('celsius')['temp'])
            elif "light" and "on" in command:
                print ("Lights are now on")
            elif "light" and "off" in command:
                print ("Lights are now off")
            elif "note" in command:
                print ("Please speak now")

                while True:
                    with mic1 as source1:
                        r.adjust_for_ambient_noise(source1)
                        audio = r.listen(source1)
                        note = r.recognize_google(audio)

                        if "stop" in note:
                            print ("Stopped taking notes")
                            notesFile.close()
                            break
                        else:
                            print ("Note added")
                            notesFile.write(note)
            elif "garage" and "open" in command:
                print ("Opening the garage")
            elif "garage" and "close" in command:
                print ("Closing the garage")


