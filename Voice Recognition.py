
import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    audio = r.listen(source)

command =  r.recognize_google(audio)


myFile = open("C:\\Users\\hp\\Desktop\\commands.txt", 'w')
myFile.write(command)
myFile.close()
