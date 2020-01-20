import pyfirmata
import time
import speech_recognition as sr
import pyowm
from gtts import gTTS
import os
from playsound import playsound
import time
import random

command_num = 0

owm = pyowm.OWM('a6d5cc8fdb1b567018fbf3da00181d9a')
r = sr.Recognizer()
mic = sr.Microphone()
mic1 = sr.Microphone()
mic2 = sr.Microphone()

board = pyfirmata.Arduino('COM4')
servo_pin = board.get_pin("d:9:s")

# Dictionary that will contain the notes
notes = {}
#GTTS Variables
language = 'en'

#Set pieces of text

#Opening 
opening = gTTS(text="I'm Listening", lang=language, slow=False)
opening.save("opening.mp3")

#Sorry didn't catch
didnt = gTTS(text="I did not quite catch that, please repeat your last statement", lang=language, slow=False)
didnt.save("sorry_didnt_catch.mp3")

#lights on
lights_on_speech = gTTS(text="Turning Lights On", lang=language, slow=False)
lights_on_speech.save("lights_on.mp3")

#lights off
lights_off_speech = gTTS(text="Turning Lights Off", lang=language, slow=False)
lights_off_speech.save("lights_off.mp3")

#garage door close
garage_close = gTTS(text="Closing the garage", lang=language, slow=False)
garage_close.save("garage_close.mp3")

#garage door open
garage_open = gTTS(text="Opening the garage", lang=language, slow=False)
garage_open.save("garage_open.mp3")

#oven on
oven_on = gTTS(text = "Preheating the oven", lang = language, slow = False)
oven_on.save("oven_on.mp3")

#oven off
oven_off = gTTS(text = "turning of the oven", lang = language, slow = False)
oven_off.save("oven_off.mp3")

#calling cops
police = gTTS(text = "calling the police", lang = language, slow = False)
police.save("police.mp3")

            


#Notes snippits
note_name = gTTS(text="What would you like to call this note", lang=language, slow=False)
note_name.save("note_name.mp3")

note_speech = gTTS(text = "Please tell me your note", lang = language, slow = False)
note_speech.save('note_speech.mp3')

another_note = gTTS(text = "Would you like to take another note", lang = language, slow = False)
another_note.save("another_note.mp3")

what_note = gTTS(text="what note would you like me to read", lang=language, slow=False)
what_note.save("what_note.mp3")

note_sorry = gTTS(text = 'Sorry a note with that title does not exist', lang = language, slow = False)
note_sorry.save('note_sorry.mp3')

jokesFile = open("Jokes.txt", "r+")


def sorry():
    #Playing the sound 
    playsound('sorry_didnt_catch.mp3')

print ("ready to listen")
playsound('opening.mp3')



with mic as source:
    # Continuous while loop that will keep taking commands from the user
    while True:
        try:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            command = r.recognize_google(audio)
            print (command)
            
            # If the user says stop, the program will terminate, maybe change this so that it will stop after a certain duration of silence
            if command == "stop":
                jokesFile.close()
                break
            else:
                # This will print the weather, incorporate text-to-speech here
                if "weather" in command:
                    to = owm.weather_at_place('Toronto, CA')
                    weather = to.get_weather()
                    temp_in_celsius =  round(weather.get_temperature('celsius')['temp'])

                    #Saving the temperature as a string to be converted into an mp3
                    weather_text = ("The temperature currently is " + str(temp_in_celsius) + " degrees Celsius")

                    #Doing the conversion and saving
                    weather_speech = gTTS(text=weather_text, lang=language, slow=False)
                    weather_speech.save("welcome.mp3")

                    #Playing the sound 
                    playsound('welcome.mp3')
                    os.remove('welcome.mp3')
                    

                # This bit will turn the lights on, change it such that it will literally turn the lights on (using Raspberry Pi)
                elif "lights" in command:
                   if "on" in command:

                        playsound('lights_on.mp3')
                        board.digital[3].write(1)
                   elif "off" in command:
                        playsound('lights_off.mp3')
                        board.digital[3].write(0)

                #Part of code that will turn the oven on and off

                elif "oven" in command:
                    if "on" in command:
                        playsound('oven_on.mp3')
                        board.digital[6].write(1)

                    elif "off" in command:
                        playsound('oven_off.mp3')
                        board.digital[6].write(0)

                elif "intruder" in command:

                    playsound('police.mp3')

                    for i in range(8):
                        board.digital[4].write(1)
                        time.sleep(2)
                        board.digital[4].write(0)

                elif "safe" in command:
                    board.digital[4].write(0)
                    
                # This bit wil check if the user wants to close or open their garage
                elif "garage" in command:
                    if "close" in command:

                        playsound('garage_close.mp3')
              

                        for x in range(95, 0, -1):
                            servo_pin.write(x)
                            time.sleep(0.01)
                        
                    elif "open" in command:


                        #Playing the sound 
                        playsound('garage_open.mp3')

                        for x in range(0, 95):
                            servo_pin.write(x)
                            time.sleep(0.01)
                                
                    else:
                        sorry()

                # This will allow the user to take some notes        
                elif "joke" in command:

                    jokes = []

                    

                    for line in jokesFile:
                        jokes.append(line.strip())
                        
                    randomLine = random.randint(0, len(jokes))
                
                    joke_text = (jokes[randomLine-1])
                                        
                    #Playing the sound

                    joke = gTTS(text = joke_text, lang = language, slow= False)
                    joke.save('joke.mp3')
                    playsound('joke.mp3')
                    os.remove('joke.mp3')


                elif "note" in command and ("take" in command or "read" in command):
                    # If they want to add notes

                    if "take" in command:
                        while True:
                            allNotes = ""
                            
                            with mic1 as source1:
                                playsound('note_name.mp3')
                                r.adjust_for_ambient_noise(source1)
                                audio = r.listen(source1)
                                title = r.recognize_google(audio)
                                

                                while True:
                                    with mic2 as source2:
                                        playsound('note_speech.mp3')
                                        r.adjust_for_ambient_noise(source1)
                                        audio = r.listen(source1)
                                        note = r.recognize_google(audio)

                                        if note != "stop":
                                            allNotes += note + " "
                                        else:
                                            break

                                notes["+" + title] = allNotes

                                playsound('another_note.mp3')

                                with mic2 as source2:
                                    r.adjust_for_ambient_noise(source1)
                                    audio = r.listen(source1)
                                    choice = r.recognize_google(audio)

                                    if choice == "yes":
                                        continue
                                    else:
                                        break
    
                    elif "read"in command:

                        with mic2 as source2:
                            playsound('what_note.mp3')
                            r.adjust_for_ambient_noise(source1)
                            audio = r.listen(source1)
                            what_note = r.recognize_google(audio)

                            if ("+" + what_note) in notes:
                                titleChoice = "+" + titleChoice

                                note_value = notes[titleChoice]

                                note_read = gTTS(text = note_value, lang = language, slow = False)
                                note_read.save('note.mp3')

                                playsound('note.mp3')
                                os.remove('note.mp3')

                            else:
                                playsound('note_sorry.mp3')

                    
        except sr.RequestError:
            print ("I did not quite catch that. Please try again. ")
            sorry()

        except sr.UnknownValueError:
            print ("I did not quite catch that. Please try again. ")
            sorry()


