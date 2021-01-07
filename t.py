import os
import wave

infiles = os.listdir('static')
outfile = "result.wav"

data = []
for infile in infiles:
    w = wave.open(os.path.join('static' , infile), 'rb')
    data.append([w.getparams(), w.readframes(w.getnframes())])
    w.close()

output = wave.open(outfile, 'wb')
output.setparams(data[0][0])
for i in range(len(data)):
    output.writeframes(data[i][1])
output.close()
