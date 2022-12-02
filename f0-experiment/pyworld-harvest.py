import numpy as np
import math
import librosa
import csv
import pyworld as pw


def process(filename, transcription, in_predicted, in_expected):
  y, sr = librosa.load(filename, dtype=np.double)
  _f0, timeaxis =  pw.harvest(y, sr, f0_floor=50.0, f0_ceil=600, frame_period=100) 
  predicted = [(int(round(a[1] * 1000, -2)), a[0]) for a in filter(lambda a: a[0] != 0.0, zip(_f0, timeaxis))]
  predicted_intervals = [tuple[0] for tuple in predicted]

  expected = [(index * 100, (ord(item) - 192) * 25 / 15) for index, item in enumerate(transcription)]
  expected_filtered = list(filter(lambda a: a[0] in predicted_intervals, expected))

  if len(predicted) != len(expected_filtered): 
    raise Exception('Comparing lists of different sizes for RMSE. This should not happen. Len predicted = ' + str(len(predicted)) + ' and len expteded = ' + str(len(expected_filtered)))
  
  
  #MSE = np.square(np.subtract(expected_filtered, predicted)).mean()
  #RMSE = math.sqrt(MSE)
  #print(RMSE)
  return (in_predicted + predicted, in_expected + expected_filtered)

def main():
  with open('LJSpeech-1.1/metadata.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='|')
    predicted = []
    expected = []
    for row in csvreader: 
      filename = 'LJSpeech-1.1/wavs/' + row[0] + '.wav'
      transcription = row[1]
      predicted, expected = process(filename, transcription, predicted, expected)
    MSE = np.square(np.subtract(expected, predicted)).mean()
    RMSE = math.sqrt(MSE)
    print('RMSE: ' + str(RMSE))
if __name__ == "__main__":
  main() 
