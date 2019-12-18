import speech_recognition as sr
# pyowm is the Python friendly version of the OWM API
import pyowm

from random import randint
# This is the API key for the OpenWeatherMap API
owm = pyowm.OWM('2360e244ea17b8c36148779867365372')

# Setting up the microphones and Recognizer
r = sr.Recognizer()
mic = sr.Microphone()
mic1 = sr.Microphone()

# Put the two files in the same directory as the python file
notesFile = open("C:\\Users\\meeky\\Desktop\\TEJ Summative\\notes.txt", 'w')
jokesFile = open("C:\\Users\\meeky\\Desktop\\TEJ Summative\\jokes.txt", 'r')

# Change the colour of the lights through voice commands?
# Tell me the news
# Add trivia, mad libs, add jokes 

# To-do:
# Surround the entire program in a try-catch statement such that if the microphone picks up something that either didn't make sense, or it didn't pick up anything at all
with mic as source:
    # Continuous while loop that will keep taking commands from the user
    while True:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        command = r.recognize_google(audio)
        print (command)
        
        # If the user says stop, the program will terminate, maybe change this so that it will stop after a certain duration of silence
        if command == "stop":
            break
        else:
            # This will print the weather, incorporate text-to-speech here
            if "weather" in command:
                to = owm.weather_at_place('Toronto, CA')
                weather = to.get_weather()
                temp_in_celsius =  round(weather.get_temperature('celsius')['temp'])
                print ("The temperature currently is " + str(temp_in_celsius) + " degrees Celsius")

            # This bit will turn the lights on, change it such that it will literally turn the lights on (using Raspberry Pi)
            elif "lights" and "on" in command:
                print ("Lights are now on")

            # This bit will turn the lights off
            elif "lights" and "off" in command:
                print ("Lights are now off")

            # This will allow the user to take some notes
            elif "note" in command:
                print ("Please speak now")

                # While loop that will continuously take notes from the user until the user says stop, incorporate text to speech here so that the user knows when to say the next note
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
                            notesFile.write(note + "\n")
            # This bit wil check if the user wants to close or open their garage
            elif "garage" in command:
                if "close" in command:
                    print ("Closing the garage")
                elif "open" in command:
                    print ("Opening the garage")
                else:
                    print ("I did not quite catch that")
            elif "joke" in command:
                jokes = []

                for line in jokesFile:
                    jokes.append(line.strip())
                    
                randomLine = randint(0, len(jokes))
                print (jokes[randomLine])
            else:
                print ("I did not quite catch that. Please try again. ")
                    



