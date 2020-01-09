import pyfirmata
import time
import speech_recognition as sr
import pyowm

r = sr.Recognizer()
mic = sr.Microphone()
mic1 = sr.Microphone()

board = pyfirmata.Arduino('COM4')

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
                    print ("Lights are now on")
                    E
                elif "lights" in command and "off" in command:
                    board.digital[2].write(0)
                    print ("Lights are now off")
                elif "garage" in command:
                    if "open" in command:
                        servo_pin.write(180)
                    elif "close" in command:
                        servo_pin.write(1)
                elif "weather" in command:
                    to = owm.weather_at_place('Toronto, CA')
                    weather = to.get_weather()
                    temp_in_celsius =  round(weather.get_temperature('celsius')['temp'])
                elif "note" in command:
                    # If they want to add notes
                    # TTS is here to say please speak now
                    if "take" in command or "write" in command:
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

                    elif "read" or "tell" in command:
                        
                        with notesFile as f:
                            notes = []
                            for line in f:
                                notes.append(line)

                        while i < len(notes):
                            # TTS here reading each index from the notes array
                            
                    # If they want to read the notes
                    
        except sr.RequestError:
            print ("I did not quite catch that. Please try again. ")

        except sr.UnknownValueError:
            print ("I did not quite catch that. Please try again. ")
     
