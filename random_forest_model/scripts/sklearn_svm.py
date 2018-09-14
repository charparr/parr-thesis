from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from plots import plot_decision_regions
import numpy as np


def linear_svm(X_train_std, X_test_std, y_train, y_test, xlab, ylab,
               test_idx=None):

    svm = SVC(kernel='linear', C=1.0, random_state=0)
    svm.fit(X_train_std, y_train)

    x_combined_std = np.vstack((X_train_std, X_test_std))
    y_combined = np.hstack((y_train, y_test))

    plot_decision_regions(X=x_combined_std, y=y_combined, classifier=svm,
                          xlab=xlab,
                          ylab=ylab,
                          test_idx=test_idx)

    return svm
