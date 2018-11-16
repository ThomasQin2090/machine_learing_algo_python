import numpy as np
from scipy.stats import multivariate_normal

class gaussian_discriminant_analysis:
    def fit(self, X, y):
        data_number, feature_number = X.shape
        self.__classes = np.unique(y)
        self.__class_number = len(self.__classes)
        
        self.__phi = np.zeros((self.__class_number, 1))
        self.__means = np.zeros((self.__class_number, feature_number))
        self.__sigma = 0
        for i in range(self.__class_number):
            self.__phi[i] = np.mean(y == self.__classes[i])

            indexes = np.where(y == self.__classes[i])[0]

            self.__means[i] = np.mean(X[indexes], axis=0)

            diff1 = (X[indexes] - self.__means[i])[:,:,np.newaxis]
            diff2 = np.transpose(diff1, axes=(0, 2, 1))
            self.__sigma += np.tensordot(diff1, diff2, axes=(0, 0)).reshape((feature_number, feature_number))

        self.__sigma /= data_number

    def predict(self, X):
        pdf = lambda mean: multivariate_normal.pdf(X, mean=mean, cov=self.__sigma)
        y_probs = np.apply_along_axis(pdf, 1, self.__means) * self.__phi

        return self.__classes[np.argmax(y_probs, axis=0)].reshape((-1, 1))