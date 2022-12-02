import numpy as np
import math
import librosa
import csv



def process(filename, transcription, in_predicted, in_expected):
  y, sr = librosa.load(filename)
  f0 = librosa.yin(y, frame_length=2205, hop_length=2205, fmin=100, fmax=1200)

  predicted = list(filter(lambda a: a[1] != -1.0, [(index * 100, item) for index, item in enumerate(f0)]))
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
