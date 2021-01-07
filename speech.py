import soundfile as sf
import librosa.display
import numpy as np
import librosa
from pydub import AudioSegment
from bangla_tts import generate
import os

f = open('sentence.txt' , 'r' , encoding='utf-8')
text = f.read()
text = text.split(' ')
window = 15
sentences = []
for i in range(0,len(text),window):
    sentence = ''
    word = text[i:i+window]
    for w in word:
        sentence = sentence + ' ' + w
    sentences.append(sentence)

# will be saved to static folder
file_names = generate(sentences, save_path="static")


# Assuming there is a folder in current directory named "static" that contains the .wav files
# This will join all the files in the default sorting order and create "result.wav"
# I believe the sample rate should be the same for each file

files = file_names

z = None

for file in files:
    x, sr = librosa.load(file)
    if z is None:
        z = x
    else:
        z = np.append(z, x)

sf.write('static/result.wav', z, sr)
