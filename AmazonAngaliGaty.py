import pyfirmata
import time
import speech_recognition as sr
import pyowm
from gtts import gTTS
import os
from playsound import playsound

command_num = 0

r = sr.Recognizer()
mic = sr.Microphone()
mic1 = sr.Microphone()

board = pyfirmata.Arduino('COM4')

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




# Declaring the pin for the servo motor
# The motor is located on pin 9
servo_motor = board.get_pin("d:9:s")


# Weather API
owm = pyowm.OWM('2360e244ea17b8c36148779867365372')
notesWriteFile = open(os.path.join(sys.path[0], "notes.txt"), 'r+')

# TO DO LIST:
# Add jokes
# Add trivia and adlibs
# Add the note taking method
# Add TTS and ensure that the sound files are downloaded with different names each time, keep track of the number of commands

with mic as source:
    
    while True:

        try: 
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            command = r.recognize_google(audio)

            print (command)

            if "stop" in command:
                break
            else:
                
                if "lights" in command and "on" in command:
                    board.digital[2].write(1)

                    #playing the presaved sound
                    playsound('lights_on.mp3')

                elif "lights" in command and "off" in command:
                    board.digital[2].write(0)

                    #playing the saved sound
                    playsound('lights_off.mp3')

                elif "garage" in command:
                    if "open" in command:
                        servo_pin.write(180)

                        #Playing the presaved sound
                        playsound('garage_open.mp3')

                    elif "close" in command:
                        servo_pin.write(1)

                        #Playing the presaved sound
                        playsound('garage_close.mp3')

                elif "weather" in command:
                    to = owm.weather_at_place('Toronto, CA')
                    weather = to.get_weather()
                    temp_in_celsius =  round(weather.get_temperature('celsius')['temp'])

                    weather_text = "The weather is currently" + temp_in_celsius + "degrees celcius"
                
                    weather_speech = gTTS(text=weather_text, lang=language, slow=False)
                    weather_speech.save("current_weather.mp3")

                    #Playing the presaved sound
                    playsound('current_weather.mp3')
                    os.remove('current_weather.mp3')
                

                elif "note" in command:
                    # If they want to add notes
                    # TTS is here to say please speak now
                    if "take" in command or "write" in command:
                        while True:
                            playsound('note_.mp3')
                            with mic1 as source1:
                                r.adjust_for_ambient_noise(source1)
                                audio = r.listen(source1)
                                title = r.recognize_google(audio)

                                note_title = "taking note titled" + title
                                
                                note_title_speech = gTTS(text=note_title, lang=language, slow=False)
                                note_title_speech.save("note_title_speech.mp3")
                                notesFile.write("+" + note_title + "\n")
                                   

                        
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

                    elif "read" or "tell" in command:
                        
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

                    
        except sr.RequestError:
            print ("I did not quite catch that. Please try again. ")

        except sr.UnknownValueError:
            print ("I did not quite catch that. Please try again. ")

