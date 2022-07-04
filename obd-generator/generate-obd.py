import numpy as np
import bezier
import csv
import random

def write_rpm_and_time(csvwriter, rpm, time):
  speed = 0.0
  load = 0.0
  throttle = 0.0
  csvwriter.writerow([str(round(rpm)) + '.0', speed, load, throttle, time])

def write_pull(csvwriter, is_accelerating, from_rpm, from_time):
  time = from_time
  pull_time = round(random.uniform(4.0, 10.0), 1)
  to_rpm = round(random.uniform(3000, 6000) if is_accelerating else random.uniform(1000, 2500))

  pull_bezier_point = random.uniform(1.0, pull_time - 1.0)
  pull_rpm_point = round(random.uniform(from_rpm + 100, to_rpm - 100) if is_accelerating else random.uniform(from_rpm - 100, to_rpm + 100))
   
  nodes = np.asfortranarray([
    [0.0, pull_bezier_point, pull_time],
    [from_rpm, pull_rpm_point, to_rpm]
  ])

  curve = bezier.Curve(nodes, degree=2)
  for progress_time in np.arange(0, pull_time, 0.1):
    #print(progress_time)
    progress = progress_time / pull_time
    rpm = curve.evaluate(progress)[1][0]
    write_rpm_and_time(csvwriter, rpm, time)
    time = time + 100
  
  return (not is_accelerating, to_rpm, time)
    
def make_dataset(csvwriter):
  is_accelerating = True
  rpm = 1000
  time = 0
  while time < 3600000: 
    is_accelerating, rpm, time = write_pull(csvwriter, is_accelerating, rpm, time)
  
def main():
  with open('dataset.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    make_dataset(csvwriter)

if __name__ == "__main__":
  main()
