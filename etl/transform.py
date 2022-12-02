import csv
from pydub import AudioSegment
import math

dataset = "dataset-12"
stoken = "l"
firstTime = 0
currentSegmentTime = 0
iterations = 0
audio = AudioSegment.from_wav(dataset + ".wav")
currentString = ''

def processSegments(csvReader, csvwriter):
  global firstTime
  global currentSegmentTime
  global currentString
  global iterations
  global audio
  for row in csvReader:
      iterations = iterations + 1
      rowTime = int(row[4])
      if row[0] == 'None' or row[1] == 'None' or row[2] == 'None' or row[3] == 'None':
        continue
      if firstTime == 0:
        firstTime = rowTime
      if currentSegmentTime == 0:
        currentSegmentTime = rowTime
      
      rpm = math.floor(float(row[0]))
      rpmEncode = math.floor(rpm / 25)

      currentString = currentString + str(chr(rpmEncode+192))
      if ((rowTime - currentSegmentTime) / 1000) >= 10:
        audioStart = round(currentSegmentTime - firstTime, -3)
        audioEnd = round(rowTime - firstTime, -3)
        if audioEnd > len(audio):
          break
        
        segmentAudio = audio[audioStart:audioEnd]
        segmentAudio.export('wavs/' + stoken +str(iterations)+'.wav', format='wav')
        
        csvwriter.writerow([stoken + str(iterations), currentString, currentString])

        currentSegmentTime = 0
        currentString = ''

with open(dataset + '.csv', newline='') as csvfile, open('metadata.csv', 'w', newline='') as csvoutfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
  csvwriter = csvwriter = csv.writer(csvoutfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  processSegments(spamreader, csvwriter)
