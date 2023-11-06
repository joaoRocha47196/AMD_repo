import sys
import Orange as DM
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree


class ModelID3:

    def __init__(self, fileName):
        self.model = DecisionTreeClassifier(criterion="entropy")
        self.dataset = self.load(fileName)

        print("Original Dataset")
        print(self.dataset)

        # all rows and columns except the last column
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
    id3_model = ModelID3(filename)
    id3_model.fit()
    id3_model.predict(id3_model.X)
    tree_plot = plot_tree(id3_model.model, feature_names=id3_model.dataset.domain.attributes, class_names=['hard', 'none', 'soft'])
    print("\n:: Plot Tree ::")
    for line in tree_plot:
        print(line)


if __name__ == "__main__":
    main()
