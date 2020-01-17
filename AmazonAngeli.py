import pyfirmata
import time
import speech_recognition as sr
import pyowm
from gtts import gTTS
import os
from playsound import playsound
import time

command_num = 0

r = sr.Recognizer()
mic = sr.Microphone()
mic1 = sr.Microphone()

board = pyfirmata.Arduino('COM4')
servo_pin = board.get_pin("d:9:s")

#GTTS Variables
language = 'en'

#Set pieces of text
#Sorry didn't catch
didnt = gTTS(text="I did not quite catch that, please repeat your last statement", lang=language, slow=False)
didnt.save("sorry_didnt_catch.mp3")

#lights on
lights_on_speech = gTTS(text="Turning Lights On", lang=language, slow=False)
lights_on_speech.save("lights_on.mp3")

#lights off
lights_off_speech = gTTS(text="Turning Lights Off", lang=language, slow=False)
lights_off_speech.save("lights_off.mp3")

#garage door open
garage_close = gTTS(text="Closing the garage", lang=language, slow=False)
garage_close.save("garage_close.mp3")

#garage door close
garage_open = gTTS(text="Opening the gate", lang=language, slow=False)
garage_open.save("garage_open.mp3")

#garage door close
note_name = gTTS(text="What would you like to call this note", lang=language, slow=False)
note_name.save("note_name.mp3")

what_note = gTTS(text="what note would you like me to read", lang=language, slow=False)
what_note.save("what_note.mp3")

def sorry():
    #Playing the sound 
    playsound('sorry_didnt_catch.mp3')

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
                playsound('welcome.mp3')
                os.remove('welcome.mp3')
                


            # This bit will turn the lights on, change it such that it will literally turn the lights on (using Raspberry Pi)
            elif "lights" and "on" in command:
                #lights_on_speech = gTTS(text=lights_on, lang=language, slow=False)
                #lights_on_speech.save("lights_on.mp3")

                #Playing the sound 
                playsound('lights_on.mp3')
                #os.remove('lights_on.mp3')
                

            # This bit will turn the lights off
            elif "lights" and "off" in command:

                lights_off_speech = gTTS(text=lights_off, lang=language, slow=False)
                #lights_off_speech.save("lights_off.mp3")

                #Playing the sound 
                playsound('lights_off.mp3')
                os.remove('lights_off.mp3')

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

                    #garage_close = gTTS(text=garage_close_text, lang=language, slow=False)
                    #garage_close.save("garage_close.mp3")

                    #Playing the sound 
                    playsound('garage_close.mp3')
                    #os.remove('garage_close.mp3')

                    for x in range(130, 0, -1):
                        servo_pin.write(x)
                        time.sleep(0.01)
                    
                elif "open" in command:

                    #garage_open = gTTS(text=garage_open, lang=language, slow=False)
                    #garage_open.save("garage_open.mp3")

                    #Playing the sound 
                    playsound('garage_open.mp3')
                    #os.remove('garage_open.mp3')

                    for x in range(0, 130):
                        servo_pin.write(x)
                        time.sleep(0.01)
                        
                    
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
                playsound('joke.mp3')
                os.remove('joke.mp3')

                
            else:
                print ("I did not quite catch that. Please try again. ")
                sorry()
