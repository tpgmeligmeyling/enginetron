import argparse
from hparams import hparams, hparams_debug_string
import os
from synthesizer import Synthesizer
import csv


synthesizer = Synthesizer()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--checkpoint', required=True, help='Full path to model checkpoint')
  parser.add_argument('--port', type=int, default=9000)
  parser.add_argument('--hparams', default='',
    help='Hyperparameter overrides as a comma-separated list of name=value pairs')
  parser.add_argument('--csv', required=True, help='Full path to metadata', type=str)
  args = parser.parse_args()
  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
  hparams.parse(args.hparams)
  print(hparams_debug_string())
  synthesizer.load(args.checkpoint)
  print('Serving on port %d' % args.port)
  with open(args.csv, newline='') as csvfile:
    csvReader = csv.reader(csvfile, delimiter='|')
    for row in csvReader:
      data = synthesizer.synthesize(row[1])
      f = open("outdir/" + row[0] + ".wav", 'wb')
      f.write(data)
      f.close()
      
  
  #synthesizer.synthesize(req.params.get('text'))
  

else:
  synthesizer.load(os.environ['CHECKPOINT'])
