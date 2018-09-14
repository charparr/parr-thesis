import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from plots import plot_decision_regions
from numpy.random import seed

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

X_std = np.copy(X)
X_std[:, 0] = (X[:, 0] - X[:, 0].mean()) / X[:, 0].std()
X_std[:, 1] = (X[:, 1] - X[:, 1].mean()) / X[:, 1].std()


# noinspection PyPep8Naming,PyShadowingNames
class AdalineGD(object):
    """Adaptive Linear Neuron Classifier.

    Parameters
    ____________
    eta: float
        Learning rate (between 0.0 and 1.0)
    n_iter : int
        Passes over training set

    Attributes
    ____________
    w_ : 1d-array
        Weights after fitting
    errors_ : list
        Number of misclassifications per epoch

    """
    def __init__(self, eta=0.01, n_iter=50):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        """Fit training data.

        Parameters
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
        self.cost_ = []

        for i in range(self.n_iter):
            output = self.net_input(X)
            errors = (y - output)
            self.w_[1:] += self.eta * X.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()
            cost = (errors**2).sum() / 2.0
            self.cost_.append(cost)
        return self

    def net_input(self, X):
        """Calculate net input."""
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def activation(self, X):
        """Compute Linear Activation"""
        return self.net_input(X)

    def predict(self, X):
        """Return Class label after unit step"""
        return np.where(self.activation(X) >= 0.0, 1, -1)


class AdalineSGD(object):
    """Adaline with SGD.

    Parameters
    ____________
    eta: float
        Learning rate (between 0.0 and 1.0)
    n_iter : int
        Passes over training set

    Attributes
    ____________
    w_ : 1d-array
        Weights after fitting
    errors_ : list
        Number of misclassifications per epoch
    shuffle : bool (default: True)
        Shuffles training data every epoch if True to prevent cycles
    random_state : int (default: None)
        Set random state for shuffling and initializing weights.

    """
    def __init__(self, eta=0.01, n_iter=10,
                 shuffle=True, random_state=None):
        self.eta = eta
        self.n_iter = n_iter
        self.w_initialized = False
        self.shuffle = shuffle
        if random_state:
            seed(random_state)

    def fit(self, X, y):
        """Fit training data.

        Parameters
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
        self._initialize_weights(X.shape[1])
        self.cost_ = []
        for i in range(self.n_iter):
            if self.shuffle:
                X, y = self._shuffle(X, y)
            cost = []
            for xi, target in zip(X, y):
                cost.append(self._update_weights(xi, target))
            avg_cost = sum(cost) / len(y)
            self.cost_.append(avg_cost)
        return self

    def partial_fit(self, X, y):
        """ Fit training data without reinitializing the weights."""
        if not self.w_initialized:
            self._initialize_weights(X.shape[1])
        if y.ravel().shape[0] > 1:
            for xi, target in zip(X, y):
                self._update_weights(xi, target)
        else:
            self._update_weights(X, y)
        return self

    def _shuffle(self, X, y):
        """ Shuffle training data."""
        r = np.random.permutation(len(y))
        return X[r], y[r]

    def _initialize_weights(self, m):
        """INitialize weights to Zero."""
        self.w_ = np.zeros(1 + m)
        self.w_initialized = True

    def _update_weights(self, xi, target):
        """ Apply Adaline learning rule to update the weights."""
        output = self.net_input(xi)
        error = (target - output)
        self.w_[1:] += self.eta * xi.dot(error)
        self.w_[0] += self.eta * error
        cost = 0.5 * error**2
        return cost

    def net_input(self, X):
        """Calculate net input."""
        return np.dot(X, self.w_[1:]) + self.w_[0]


    def activation(self, X):
        """Compute Linear Activation"""
        return self.net_input(X)


    def predict(self, X):
        """Return Class label after unit step"""
        return np.where(self.activation(X) >= 0.0, 1, -1)


# fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
# ada1 = AdalineGD(n_iter=10, eta=0.01).fit(X, y)
#
# ax[0].plot(range(1, len(ada1.cost_) +1),
#            np.log10(ada1.cost_), marker='o')
# ax[0].set_xlabel('Epochs')
# ax[0].set_ylabel('log(SSE)')
# ax[0].set_title('Adaline Learning Rate = 0.01')
#
# ada2 = AdalineGD(n_iter=10, eta=0.0001).fit(X, y)
# ax[1].plot(range(1, len(ada2.cost_) +1),
#            np.log10(ada1.cost_), marker='o')
# ax[1].set_xlabel('Epochs')
# ax[1].set_ylabel('log(SSE)')
# ax[1].set_title('Adaline Learning Rate = 0.0001')
# plt.show()

# ada = AdalineGD(n_iter=15, eta=0.01)
# ada.fit(X_std, y)
#
# plot_decision_regions(X_std, y, xlab='max depth', ylab='min_depth',
#                       classifier=ada)
# plt.title('Adaline - Gradient Descent')
#
# plt.plot(range(1, len(ada.cost_) + 1), ada.cost_, marker='o')
# plt.xlabel('Epochs')
# plt.ylabel('SSE')
# plt.show()

###

ada_sgd = AdalineSGD(n_iter=50, eta=0.01, random_state=1)
ada_sgd.fit(X_std, y)

plot_decision_regions(X_std, y, xlab='max depth', ylab='min_depth',
                      classifier=ada_sgd)
plt.title('Adaline - Stochastic Gradient Descent')

plt.plot(range(1, len(ada_sgd.cost_) + 1), ada_sgd.cost_, marker='o')
plt.xlabel('Epochs')
plt.ylabel('Average Cost')
plt.show()