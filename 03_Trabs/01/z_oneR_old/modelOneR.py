from utils import Utils
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

class modelOneR:
    '''
    @param fileName: The iput file containing .tab data
    @param testPercentage: The % of error
    - Creates Utils instance 
    - Loads Input File
    - Initializes dataSets
    '''
    def __init__(self, fileName, testPercentage):
        self.utils = Utils()
        self.utils.logHeader("Staring Running OneR")
        self.rule = None
        self.minErrorAtribute = None

        # Original and Shufled DataSet
        self.utils.log("Generated DataSets:")

        self.dataset = self.utils.load(fileName)
        self.utils.print_data_set("Full DataSet", self.dataset)

        self.dataset.shuffle()
        self.utils.print_data_set("Shuffled DataSet", self.dataset)

        # Divid original DataSet in Train and Test
        test = int(len(self.dataset) * testPercentage) + 1
        train = len(self.dataset) - test

        self.datasetTest = self.dataset[train:]
        self.utils.print_data_set("Test DataSet", self.datasetTest)

        self.dataset = self.dataset[:train]
        self.utils.print_data_set("Train DataSet", self.dataset)

    '''
    '''
    def get_variableFrom_str(self, dataset, str_name):
        variable_list = dataset.domain.variables
        for variable in variable_list:
            if (variable.name == str_name): return variable
        self.utils.my_print(f">>error>> \"{str_name}\" is not a variable name in dataset!")
        return None

    def get_contingencyMatrix(self, dataset, rowVar, colVar):
        if (isinstance(rowVar, str)): rowVar = self.get_variableFrom_str(dataset, rowVar)
        if (isinstance(colVar, str)): colVar = self.get_variableFrom_str(dataset, colVar)
        if (not (rowVar and colVar)): return ([], [], None)
        if (not (rowVar.is_discrete and colVar.is_discrete)):
            self.utils.my_print(">>error>> variables are expected to be discrete")
            return ([], [], None)

        rowDomain, colDomain = rowVar.values, colVar.values
        len_rowDomain, len_colDomain = len(rowDomain), len(colDomain)
        contingencyMatrix = np.zeros((len_rowDomain, len_colDomain))
        for instance in dataset:
            rowValue, colValue = instance[rowVar], instance[colVar]
            if (np.isnan(rowValue) or np.isnan(colValue)): continue

            rowIndex, colIndex = rowDomain.index(rowValue), colDomain.index(colValue)
            contingencyMatrix[rowIndex, colIndex] += 1
        return (rowDomain, colDomain, contingencyMatrix)

    def get_conditionalProbability(self, dataset, H, E):
        if (isinstance(H, str)): H = self.get_variableFrom_str(dataset, H)
        if (isinstance(E, str)): E = self.get_variableFrom_str(dataset, E)
        if (not (H and E)): return ([], [], None)
        (rowDomain, colDomain, cMatrix) = self.get_contingencyMatrix(dataset, H, E)

        len_rowDomain, len_colDomain = len(rowDomain), len(colDomain)
        E_marginal = np.zeros(len_colDomain)
        for col in range(len_colDomain): E_marginal[col] = sum(cMatrix[:, col])

        for row in range(len_rowDomain):
            for col in range(len_colDomain):
                cMatrix[row, col] = cMatrix[row, col] / E_marginal[col]
        return (rowDomain, colDomain, cMatrix)

    def get_errorMatrix(self, dataset, feature):
        if (isinstance(feature, str)): feature = self.get_variableFrom_str(dataset, feature)
        the_class = dataset.domain.class_var
        (rowDomain, colDomain, cMatrix) = self.get_conditionalProbability(dataset, the_class, feature)
        if (not (rowDomain or colDomain)): return ([], [], None)

        errorMatrix = 1 - cMatrix
        return (rowDomain, colDomain, errorMatrix)

    def execute(self):
        self.utils.logHeader("Staring Executing OneR")
        self.utils.log("Generated 1R Error Matrix:")
        dicMinError, rule, ruleExport = {}, {}, {}

        # Iterate over each possible atribute
        for attribute in self.dataset.domain.attributes:
            self.utils.loggHeader(f"{attribute} & {self.dataset.domain.class_var}")
            
            (classDomain, featureDomain, errorMatrix) = self.get_errorMatrix(self.dataset, attribute)
            self.utils.print_variable_and_value(classDomain=classDomain, featureDomain=featureDomain, errorMatrix=errorMatrix)
            
            self.utils.print("")
            self.utils.print(f"Rule and Error for attribute {attribute}")

            self.utils.print("next")
            sumMinError = 0
            dicRule = {}
            dicRuleExport = {}
            for featureIdx in range(len(featureDomain)):
                errorFeature = errorMatrix[:, featureIdx]
                errorMin = min(errorFeature)
                errorMinIndex = errorFeature.tolist().index(errorMin)
                featureValue = featureDomain[featureIdx]
                classValue = classDomain[errorMinIndex]
                self.utils.print(f"({attribute}, {featureValue}, {classValue}) : {errorMin:.3f}")

                numberFeatureValues = len([d for d in self.dataset if d[attribute] == featureValue])
                errorValue = numberFeatureValues * errorMin
                sumMinError += errorValue

                strExportar = f"({attribute}, {featureValue}, {classValue}) : ({int(errorValue)}, {numberFeatureValues})"
                dicRuleExport[featureValue] = strExportar

                dicRule[featureValue] = classValue

            print("\nTotal attribute error: ", sumMinError / len(self.dataset))
            dicMinError[attribute] = sumMinError / len(self.dataset)
            rule[attribute] = dicRule
            ruleExport[attribute] = dicRuleExport

            self.utils.logSimpleLine()

        # After all iterations chosse the atribute with less error
        minError = min(dicMinError, key=dicMinError.get)
        self.utils.my_print(f"Attribute with the least error: {minError}")
        print("\nRule:", rule.get(minError))

        self.export(list(ruleExport.get(minError).values()))

        self.rule = rule.get(minError)
        self.minErrorAtribute = minError

    def predict(self, x_test):

        if len(x_test) != len(self.dataset.domain.attributes):
            raise Exception(f"Wrong number of attributes (Needs {len(self.dataset.domain.attributes)})")

        for i in range(len(x_test)):
            if not isinstance(x_test[i], type(self.dataset.domain.attributes[i].values[0])):
                raise Exception(f"Attributes needs to be a {type(self.dataset.domain.attributes[i].values[0])}")

            if not x_test[i] in self.dataset.domain.attributes[i].values:
                raise Exception(f"Attribute {i + 1} not in domain")

            if self.dataset.domain.attributes[i] == self.minErrorAtribute:
                return self.rule[x_test[i]]

    def predictTestDataset(self):
        y_test, y_predict = [], []

        # Scroll through the test dataset
        for i in range(len(self.datasetTest)):
            # Save the predicted labels
            y_predict.append(self.rule[str(self.datasetTest[i][self.minErrorAtribute])])

            # Save the true labels
            y_test.append(self.datasetTest[i][str(self.datasetTest.domain.class_var)].value)

        return y_test, y_predict

    def score(self, y_test, y_predict):
        score_accuracy = accuracy_score(y_test, y_predict)
        self.utils.my_print(f"Model accuracy: {score_accuracy}")

        score_precision = precision_score(y_test, y_predict, average="weighted", zero_division=0)
        self.utils.my_print(f"Model precision: {score_precision}")

        score_recall = recall_score(y_test, y_predict, average="weighted", zero_division=0)
        self.utils.my_print(f"Model recall: {score_recall}")

        score_f1 = f1_score(y_test, y_predict, average="weighted", zero_division=0)
        self.utils.my_print(f"Model f1 score: {score_f1}")

        self.utils.my_print(f"Confusion Matrix:\n {confusion_matrix(y_test, y_predict)}")

    def export(self, listLines):
        listLines.insert(0, "(attr, valueAttr, valueTarget) : (error, total)")

        with open("oneR_OUTPUT.txt", "w") as txt_file:
            for line in listLines:
                txt_file.write(line + "\n")

def main():
    fileName = "d01_lenses.tab"
    oneR = modelOneR(fileName, 0.5)
    oneR.execute()

    oneR.utils.my_print(oneR.predict(["presbyopic", "myope", "yes", "normal"]))

    y_test, y_predict = oneR.predictTestDataset()

    oneR.score(y_test, y_predict)

if __name__ == "__main__":
    main()
