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

# Dictionary that will contain the notes
notes = {}
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

jokesFile = open("Jokes.txt", "w+")


def sorry():
    #Playing the sound 
    playsound('sorry_didnt_catch.mp3')

# Add TTS here to signify the machine is ready to listen
print ("ready to listen")

# To-do:
# Surround the entire program in a try-catch statement such that if the microphone picks up something that either didn't make sense, or it didn't pick up anything at all
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
                elif "lights" in command:
                   if "on" in command:
                        playsound('lights_on.mp3')
                        board.digital[3].write(1)
                   elif "off" in command:
                        playsound('lights_off.mp3')
                        board.digital[3].write(0)
        
                elif "oven" in command:
                    if "on" in command:
                        # TTS here
                        board.digital[6].write(1)
                    elif "off" in command:
                        board.digital[6].write(0)

                elif "intruder" in command:
                    board.digital[4].write(1)
                    sleep(2)
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
                        
                    randomLine = randint(0, len(jokes))
                
                    joke_text = (jokes[randomLine-1])
                    
                    #Playing the sound 
                    playsound('joke.mp3')


                elif "note" in command:
                    # If they want to add notes
                    # TTS is here to say please speak now
                    if "take" in command:
                        while True:
                            allNotes = ""
                            
                            with mic1 as source1:
                                # Add TTS here to ask the user for their title
                                r.adjust_for_ambient_noise(source1)
                                audio = r.listen(source1)
                                title = r.recognize_google(audio)

                                while True:
                                    with mic1 as source1:
                                        # TTS here for add your note

                                        r.adjust_for_ambient_noise(source1)
                                        audio = r.listen(source1)
                                        note = r.recognize_google(audio)

                                        if note != "stop":
                                            allNotes += note + " "
                                        else:
                                            break

                                notes["+" + title] = allNotes

                                # Add TTS here if they would like to take another note

                                with mic1 as source1:
                                    r.adjust_for_ambient_noise(source1)
                                    audio = r.listen(source1)
                                    choice = r.recognize_google(audio)

                                    if choice == "yes":
                                        continue
                                    else:
                                        break
    
                    elif "read"in command:

                        with mic1 as source1:
                            playsound('what_note.mp3')
                            r.adjust_for_ambient_noise(source1)
                            audio = r.listen(source1)
                            what_note = r.recognize_google(audio)

                            if ("+" + what_note) in notes:
                                # Add TTS here that will read the key value pair, it is all stored in one string, so don't worry about having to check until the next title
                                # you can access the variable through notes["+" + titleChoice] and then putting that into a playsound
                            else:
                                # TTS that will tell the user that the note underneath that title does not exist

                                
                        with mic1 as source1:
                                playsound('what_note.mp3')
                                r.adjust_for_ambient_noise(source1)
                                audio = r.listen(source1)
                                what_note = r.recognize_google(audio)
                        
                        with notesFile as f:
                            lineNumber = 0
                            note_read = ""
                            for line in f:
                                lineNumber += 1
                                if line == "+" + what_note:

                                    startLine = lineNumber + 1
                                    
                                    while "+" not in notesFile[startLine]:
                                        note_read = note_read + "and" + notesFile[startLine]

                                    note_to_read = gTTS(text=note_read, lang=language, slow=False)
                                    note_to_read.save("note_to_read" + command_num + ".mp3")

                                    playsound('note_to_read' + command_num + '.mp3')
                                    os.remove('note_to_read' + command_num + '.mp3')
                                    command_num += 1


               

                else:
                    print ("I did not quite catch that. Please try again. ")
                    sorry()

                    
        except sr.RequestError:
            print ("I did not quite catch that. Please try again. ")
            sorry()

        except sr.UnknownValueError:
            print ("I did not quite catch that. Please try again. ")
            sorry()

                
         
