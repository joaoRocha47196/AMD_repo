import sys
import Orange as DM
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier, plot_tree

class ModelID3:

    def __init__(self, fileName):
        self.model = DecisionTreeClassifier(criterion="entropy")
        self.dataset = self.load(fileName)

        print("Original Dataset")
        print(self.dataset)

        # all rows and all columns except the last column
        self.X = pd.DataFrame(self.dataset).values[:, 0:-1]

        # all rows and just the last column
        self.y = pd.DataFrame(self.dataset).values[:, -1]

        print("X")
        print(self.X)
        print("y")
        print(self.y)

    def load(self, fileName):
        try:
            dataset = DM.data.Table(fileName)
        except:
            print("--->>> error - can not open the file: %s" % fileName)
            sys.exit()
        return dataset

    def fit(self):
        accuracy_score_list = list()
        precision_score_list = list()
        recall_score_list = list()
        f1_score_list = list()

        for (train_index, test_index) in StratifiedShuffleSplit(n_splits=5, test_size=1.0 / 2.0, random_state=None).split(self.X, self.y):
            X_train, y_train = self.X[train_index], self.y[train_index]
            X_test, y_test = self.X[test_index], self.y[test_index]

            # fit (build) model using classifier, X_train and y_train (training dataset)
            self.model.fit(X_train, y_train)

            # predict using the model and X_test (testing dataset)
            y_predict = self.model.predict(X_test)

            print("X_train")
            print(X_train)
            print("y_train")
            print(y_train)
            print("X_test")
            print(X_test)
            print("y_test")
            print(y_test)
            print("y_predict")
            print(y_predict)

            # score the model using y_test (expected) and y_predict (predicted by the model)
            score_accuracy = accuracy_score(y_test, y_predict)

            accuracy_score_list.append(score_accuracy)

            score_precision = precision_score(y_test, y_predict, average="weighted")

            precision_score_list.append(score_precision)

            score_recall = recall_score(y_test, y_predict, average="weighted")

            recall_score_list.append(score_recall)

            score_f1 = f1_score(y_test, y_predict, average="weighted")

            f1_score_list.append(score_f1)

            print("Confusion Matrix:\n {}".format(confusion_matrix(y_test, y_predict)))

        print("Model accuracy: {}".format(accuracy_score_list))

        print("Model precision: {}".format(precision_score_list))

        print("Model recall: {}".format(recall_score_list))

        print("Model f1 score: {}".format(f1_score_list))




def main():
    filename = 'd01_lenses.tab'
    id3_model = ModelID3(filename)
    id3_model.fit()
    class_names = ['hard', 'none', 'soft']
    plot_tree(id3_model.model, class_names=class_names)

if __name__ == "__main__":
    main()