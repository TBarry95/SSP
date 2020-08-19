############################################
# DES:
# BY:
###########################################

###########################################
# libraries:
###########################################

import sys
import csv
import numpy as np
from skmultiflow.trees import HoeffdingTreeRegressor
from skmultiflow.data import DataStream
import pandas as pd

###########################################
# model:
###########################################

model = HoeffdingTreeRegressor()

###########################################
# Mapper:
###########################################

correctness_dist = []

for line in csv.reader(sys.stdin):
    try:

        if len(line) == 14 and line[0] != 'DATE_TIME' and line[0][0:4] == "2020":
            df = pd.DataFrame()
            df['covid'] = [float(line[13])]
            df['sent'] = [float(line[3])]
            #print(df)
            stream = DataStream(df)
            #X,Y = stream.current_sample_x, stream.current_sample_y
            X, Y = stream.next_sample()

            # covid = X, sent = Y
            # covid, sent  = float(line[13]), float(line[3])
            # data = tuple([np.array([[covid]]), np.array([sent])])

            prediction = model.predict(X)
            if Y == prediction:
                correctness_dist.append(1)
            else:
                correctness_dist.append(0)
            model.partial_fit(X,Y)
            print("Predictions vs Actual:", prediction,Y)
    except IndexError:
        continue
