import sys
import Orange as DM
import pandas as pd
from sklearn.naive_bayes import GaussianNB

class ModelNaiveBayes:

    def __init__(self, fileName):
        self.model = GaussianNB()
        self.dataset = self.load(fileName)

        print("Original Dataset")
        print(self.dataset)

        # all rows and all columns except the last column
        self.X = pd.DataFrame(self.dataset).values[:, 0:-1]

        # all rows and just the last column
        self.Y = pd.DataFrame(self.dataset).values[:, -1]

        print("\nX")
        print(self.X)
        print("\nY")
        print(self.Y)

    def load(self, fileName):
        try:
            dataset = DM.data.Table(fileName)
        except:
            print("--->>> error - can not open the file: %s" % fileName)
            sys.exit()
        return dataset

    def fit(self):
        self.model.fit(self.X, self.Y)


    def predict(self, X):
        prediction = self.model.predict(X)
        print("\n:: Prediction of the original dataset ::")
        print(prediction)


def main():
    filename = 'd01_lenses.tab'
    naive_bayes_model = ModelNaiveBayes(filename)
    naive_bayes_model.fit()
    naive_bayes_model.predict(naive_bayes_model.X)

if __name__ == "__main__":
    main()