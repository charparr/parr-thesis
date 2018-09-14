import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


class Perceptron(object):
    """Perceptron classifier.

    Parameters
    ______________
    eta: float
        Learning rate (between 0.0 and 1.0)
    n_iter: int
        Passes over the training set (Epochs)

    Attributes
    _______________
    w_ : 1d-array
        Weights after fitting
    errors_ : list
        Number of mis-classifications in every epoch

    """
    def __init__(self, eta=0.01, n_iter=10):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        """Fit training data.

        Paramters
        ___________
        X : {array-like}, shape = [n_samples, n_features]
            Training vectors, where N_samples is the number of samples and
            n_features is the number of features.
        y : array-like, shape = [n_samples]
            Target values (labels)

        Returns
        _________
        self : object

        """
        self.w_ = np.zeros(1 + X.shape[1])
        self.errors_ = []

        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X, y):
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self

    def net_input(self, X):
        """Caclulate net input."""
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
            """Returns class label after unit step"""
            return np.where(self.net_input(X) >= 0.0, 1, -1)


df = pd.read_csv('test_data/labeled_drift_or_not.csv')
print(df.shape)
print(df.columns)

new_df = pd.DataFrame()
new_df['normal max. depth'] = df['normed_depth_max_intensity']
new_df['normal min. depth'] = df['normed_depth_min_intensity']
new_df['label'] = df['label']
print(new_df.shape)

y = new_df.iloc[::, 2].values
y = np.where(y == 'drift', -1, 1)
X = new_df.iloc[::, [0, 1]].values

plt.figure()
plt.scatter(X[:18, 0], X[:18, 1],
            color='red', marker='o', label='drift')
plt.scatter(X[18::, 0], X[18::, 1],
            color='blue', marker='x', label='NOT drift')
plt.xlabel('normal max. depth')
plt.ylabel('normal min. depth')
plt.legend()
plt.show()


ppn = Perceptron(eta=0.1, n_iter=5)
ppn.fit(X, y)
plt.figure()
plt.plot(range(1, len(ppn.errors_) + 1), ppn.errors_, marker='o')
plt.xlabel('Epochs')
plt.ylabel('Number of mis-classifications')
plt.show()


