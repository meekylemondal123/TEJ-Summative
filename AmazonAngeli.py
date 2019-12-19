import speech_recognition as sr
# pyowm is the Python friendly version of the OWM API
import pyowm

#gTTS or google text to speech just a text reading api
from gtts import gTTS

#The os Module
import os

#A simple on fuction module that can play an mp3
from playsound import playsound

#
#
#f= open("guru99.txt","w+")
#
#

from random import randint
# This is the API key for the OpenWeatherMap API
owm = pyowm.OWM('2360e244ea17b8c36148779867365372')

# Setting up the microphones and Recognizer
r = sr.Recognizer()
mic = sr.Microphone()
mic1 = sr.Microphone()

#Declaring the various text files to be played
language = 'en'
weather_text = ""

#The Sorry didnt catch text
didnt = gTTS(text="I did not quite catch that, please repeat your last statement", lang=language, slow=False)
didnt.save("sorry_didnt_catch.mp3")


#Lights on and off text placeholdr, changeable
lights_on = "Truning Lights On"
lights_off = "Turning Lights Off"

#We should definatley have a varaible that cheaks if the user already has the door open/ closed and tell them that if already open/closed if thats the case
garage_open_text = "Opening the garage"
garage_close_text = "Closing the gate"



# Put the two files in the same directory as the python file
notesFile = open("C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\notes.txt", 'w')
jokesFile = open("C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\jokes.txt", 'r')


# Change the colour of the lights through voice commands?
# Tell me the news
# Add trivia, mad libs, add jokes

def sorry():
    #Playing the sound 
    playsound('C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\sorry_didnt_catch.mp3')

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

                #Saving the temperateu as a string to be converted into an mp3
                weather_text = ("The temperature currently is " + str(temp_in_celsius) + " degrees Celsius")

                #Doing the conversion and saving
                weather_speech = gTTS(text=weather_text, lang=language, slow=False)
                weather_speech.save("welcome.mp3")

                #Playing the sound 
                playsound('C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\welcome.mp3')
                os.remove('C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\welcome.mp3')
                


            # This bit will turn the lights on, change it such that it will literally turn the lights on (using Raspberry Pi)
            elif "lights" and "on" in command:
                lights_on_speech = gTTS(text=lights_on, lang=language, slow=False)
                lights_on_speech.save("lights_on.mp3")

                #Playing the sound 
                playsound('C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\lights_on.mp3')
                os.remove('C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\lights_on.mp3')
                

            # This bit will turn the lights off
            elif "lights" and "off" in command:

                lights_off_speech = gTTS(text=lights_off, lang=language, slow=False)
                lights_off_speech.save("lights_off.mp3")

                #Playing the sound 
                playsound('C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\lights_off.mp3')
                os.remove('C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\lights_off.mp3')

            # This will allow the user to take some notes
            elif "note" in command:
                print ("Please speak now")
                print (command)

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

                    garage_close = gTTS(text=garage_close_text, lang=language, slow=False)
                    garage_close.save("garage_close.mp3")

                    #Playing the sound 
                    playsound('C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\garage_close.mp3')
                    os.remove('C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\garage_close.mp3')
                    
                elif "open" in command:

                    garage_open = gTTS(text=garage_open_text, lang=language, slow=False)
                    garage_open.save("garage_open.mp3")

                    #Playing the sound 
                    playsound('C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\garage_open.mp3')
                    os.remove('C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\garage_open.mp3')

                    
                else:
                    sorry()

                    
            elif "joke" in command:

                jokes = []

                

                for line in jokesFile:
                    jokes.append(line.strip())
                    
                randomLine = randint(0, len(jokes))
            
                joke_text = (jokes[randomLine-1])
                
                joke = gTTS(text=joke_text, lang=language, slow=False)
                joke.save("joke.mp3")

                #Playing the sound 
                playsound('C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\joke.mp3')
                os.remove('C:\\Users\\jayzf\\Desktop\\TEJFinalProject\\joke.mp3')

                
            else:
                print ("I did not quite catch that. Please try again. ")
                sorry()
                    
