import math
import os

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense


class ANN:

    def __init__(self, dataset_path):

        self.dataset = pd.read_csv(dataset_path, header=0)

        self.X = self.dataset.iloc[:, :-1]
        self.Y = self.dataset.iloc[:, -1]
        self.X = StandardScaler().fit_transform(self.X)

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.X, self.Y, test_size=0.3,
                                                                                random_state=20)



    def get_new_features(self, parent):
        
        par_x_train = np.empty([self.x_train.shape[0], 1])
        par_x_test = np.empty([self.x_test.shape[0], 1])

        for i, feature_bit in enumerate(parent):
            if feature_bit == 1:
                par_x_train = np.column_stack((par_x_train, self.x_train[:, i]))
                par_x_test = np.column_stack((par_x_test, self.x_test[:, i]))

        par_x_train = par_x_train[:, 1:]
        par_x_test = par_x_test[:, 1:]

        return par_x_train, par_x_test

    def train_net(self, x_train, x_test):
        m = x_train.shape[1]
        
        NN = Sequential()
        NN.add(Dense(max(m*2/3, 20), activation='relu', kernel_initializer='random_normal', input_dim=m))
        # Second Layer
        NN.add(Dense(max(m/9, 10), activation='relu', kernel_initializer='random_normal'))
        # Third Layer
        NN.add(Dense(max(m/27, 5), activation='relu', kernel_initializer='random_normal'))
        # Output Layer
        NN.add(Dense(1, activation='sigmoid', kernel_initializer='random_normal'))

        NN.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        NN.fit(x_train, self.y_train, batch_size=10, epochs=10, verbose=False)

        perf = NN.evaluate(x_test, self.y_test)
        loss = perf[0]
        loss = math.exp((-10*loss))

        return loss

    def get_fitness(self, population):
        pop_fitness = []

        for parent in population:
            new_x_train, new_x_test = self.get_new_features(parent)
            fitness = self.train_net(new_x_train, new_x_test)
            pop_fitness.append(fitness)

        return pop_fitness
