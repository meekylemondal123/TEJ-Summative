import vlc, pafy, time
# need to download youtube_dl
# need to install vlc
# maybe make it so that if the user says stop, it will stop the video
url = "https://www.youtube.com/watch?v=1yNfzVABvCM"

video = pafy.new(url)

print (video.title)
print (video.rating)
print (video.description)


best = video.getbest()

media = vlc.MediaPlayer(best.url)
media.play()


