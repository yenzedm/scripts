from gtts import gTTS
import os

# create audio with miss
tts = gTTS(text="miss", lang='ru')
tts.save("miss.mp3")
