from skmultiflow.data.file_stream import FileStream
from skmultiflow.data import DataStream
import sys
import pandas as pd

data = pd.read_csv("/home/tiernan/PycharmProjects/SSP_3/output/job_2/part-00000.csv")
data = data[data['DATE_TIME'].str.startswith("2020")]
del data['DATE_TIME']
del data[' SOURCE']
data = data[[' MEAN_SENT_CATG', ' COVID_COUNT\t']]
data.columns = ['MEAN_SENT_CATG', 'COVID_COUNT']

#data.to_csv("/home/tiernan/Documents/test_stream.csv", index=False)
#stream = FileStream("/home/tiernan/Documents/test_stream.csv", allow_nan = True)
#test = stream.next_sample()

from skmultiflow.trees import HoeffdingTree
tree = HoeffdingTree()

correctness_dist = []

for i in range(len(data)):

    df = pd.DataFrame()
    df['covid'] = data['COVID_COUNT'][i]
    df['SENT_CATG'] = data['MEAN_SENT_CATG'][i]

    print(df)

    '''nb_iters = 1
    stream = DataStream(data.head(1))

    for i in range(nb_iters):

        X, Y = stream.next_sample()

        prediction = tree.predict(X)  # predict Y using the tree
        if Y == prediction:                # check the prediction
            correctness_dist.append(1)
        else:
            correctness_dist.append(0)

        tree.partial_fit(X, Y)  # update the tree
        print("Prediction v ActuaL: ", prediction, Y)'''