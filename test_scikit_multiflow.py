from skmultiflow.data import SEAGenerator

stream = SEAGenerator()      # create a stream
stream.prepare_for_use()     # prepare the stream for use

X,Y = stream.next_sample()

from skmultiflow.trees import HoeffdingTree

tree = HoeffdingTree()

nb_iters = 10000

correctness_dist = []
for i in range(nb_iters):
    X, Y = stream.next_sample()  # get the next sample
    prediction = tree.predict(
        X)  # predict Y using the tree        if Y == prediction:                # check the prediction
    correctness_dist.append(1)
else:
    correctness_dist.append(0)

tree.partial_fit(X, Y)  # update the tree

import matplotlib.pyplot as plt

time = [i for i in range(1, nb_iters)]
accuracy = [sum(correctness_dist[:i])/len(correctness_dist[:i]) for i in range(1, nb_iters)]

plt.plot(time, accuracy)