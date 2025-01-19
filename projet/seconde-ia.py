import re
import csv
import glob
import os
import sys


input_files = sys.argv[1]
output_file = 'lorem-lipsum.txt'


frame_pattern = re.compile(r'Frame count: (\d+)')
detection_pattern = re.compile(r'Detection: person (\d\.\d+)')
point_pattern = re.compile(r'(\w+): x: (\d+\.\d+) y: (\d+\.\d+)')


header = [str(i) for i in range(0, 36)]


with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)


    csvwriter.writerow(header)

    for input_file in glob.glob(input_files):
        with open(input_file, 'r') as infile:
            frame_data = []
            for line in infile:
                line = line.strip()


                frame_match = frame_pattern.match(line)
                if frame_match:
                    if frame_data:  
                        csvwriter.writerow([0] + frame_data[1:]) 
                    frame_data = [frame_match.group(1)]  
                    continue

                detection_match = detection_pattern.match(line)
                if detection_match:
                    frame_data.append(detection_match.group(1))
                    continue

                point_match = point_pattern.match(line)
                if point_match:
                    frame_data.extend([point_match.group(2), point_match.group(3)])

            if frame_data:
                csvwriter.writerow([1] + frame_data[1:])

from sklearn.model_selection import cross_val_score, train_test_split
import pickle
import pandas as pd


with open('/home/pi/Git/hailo-rpi5-examples/projet/model_RF.pickle', mode='rb') as f:
    model = pickle.load(f)


df_test = pd.read_csv(output_file)


df_test = df_test.drop(df_test.columns[0], axis=1)



print(model.predict(df_test).mean())
if model.predict(df_test).mean() < 0.3:
    print("la posture est mauvaise")
else:
    print("la posture est correcte")
