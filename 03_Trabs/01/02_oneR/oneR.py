from utils import Utils
import numpy as np
import sys
import Orange as DM
#_______________________________________________________________________________
# This class represents the implementation of oneR based on 
# lectures provided functions (with some alterations) 
class OneR:

    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #:::::::::::::::::::::::::::::::::::::Other Functions::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    #_______________________________________________________________________________
    # Loads dataset from file
    def load(self, fileName):
      print("::[Reading Input File]")
      try:
         dataset = DM.data.Table(fileName)
      except Exception as e:
         self.utils.my_print(f":: Error - cannot open the file: {fileName}")
         sys.exit(1)  # Exit with an error code
      return dataset
    
    #_______________________________________________________________________________
    # Inits object modelOneR
    def __init__(self, fileName):
        self.utils = Utils()
        print("::[Staring Running OneR]")
        self.dataset = self.load(fileName)

        print("::[Loaded DataSet]")
        self.utils.print_data_set("DataSet", self.dataset)

    #_______________________________________________________________________________
    # get the variable dataset-structure given a string with its name
    def get_variableFrom_str(self, dataset, str_name):
        variable_list = dataset.domain.variables
        for variable in variable_list:
            if (variable.name == str_name): return variable
        self.utils.my_print(f">>error>> \"{str_name}\" is not a variable name in dataset!")
        return None

    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::OnewR related Functions:::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    #_______________________________________________________________________________
    # contingencyMatrix; i.e., the joint-frequency table
    # this implementation does not account for missing-values
    # M(row, column)
    def get_frequency(self, rowVar, colVar):
        if (isinstance(rowVar, str)): rowVar = self.get_variableFrom_str(self.dataset, rowVar)
        if (isinstance(colVar, str)): colVar = self.get_variableFrom_str(self.dataset, colVar)
        if (not (rowVar and colVar)): return ([], [], None)
        if (not (rowVar.is_discrete and colVar.is_discrete)):
            self.utils.my_print(">>error>> variables are expected to be discrete")
            return ([], [], None)

        rowDomain, colDomain = rowVar.values, colVar.values
        len_rowDomain, len_colDomain = len(rowDomain), len(colDomain)
        contingencyMatrix = np.zeros((len_rowDomain, len_colDomain))
        for instance in self.dataset:
            rowValue, colValue = instance[rowVar], instance[colVar]
            if (np.isnan(rowValue) or np.isnan(colValue)): continue

            rowIndex, colIndex = rowDomain.index(rowValue), colDomain.index(colValue)
            contingencyMatrix[rowIndex, colIndex] += 1
        return (rowDomain, colDomain, contingencyMatrix)
    
    #_______________________________________________________________________________
    # compute_frequency
    def compute_frequency(self, rowVar, colVar ):    
        ( rowDomain, colDomain, cMatrix ) = self.get_frequency(rowVar, colVar )  
        self.utils.my_print( "Domain Values for: {} & {} :".format( rowVar.name, colVar.name ) )
        print( rowDomain )
        print( colDomain )
        self.utils.my_print( "Frequency Table for: {} & {} :".format( rowVar.name, colVar.name ) )
        print( cMatrix )
        for row in rowDomain:
            showStr = "<" + row + "> "
            for col in colDomain:
                showStr += col + ": " + str(cMatrix[rowDomain.index(row), colDomain.index( col )]) + " | "
            print( showStr )
        
        return ( rowDomain, colDomain, cMatrix )
    
    #_______________________________________________________________________________
    # P( H | E )
    # H means Hypothesis, E means Evidence
    # a frequency approach
    def get_probability(self, dataset, H, E):
        if (isinstance(H, str)): H = self.get_variableFrom_str(dataset, H)
        if (isinstance(E, str)): E = self.get_variableFrom_str(dataset, E)
        if (not (H and E)): return ([], [], None)
        (rowDomain, colDomain, cMatrix) = self.compute_frequency(H, E)

        len_rowDomain, len_colDomain = len(rowDomain), len(colDomain)
        E_marginal = np.zeros(len_colDomain)
        for col in range(len_colDomain): E_marginal[col] = sum(cMatrix[:, col])

        for row in range(len_rowDomain):
            for col in range(len_colDomain):
                cMatrix[row, col] = cMatrix[row, col] / E_marginal[col]
        return (rowDomain, colDomain, cMatrix)
    
    #_______________________________________________________________________________
    # P( H | E )
    # show matriz and textual description
    def compute_probability( self, dataset, H, E ):
        ( rowDomain, colDomain, cMatrix ) = self.get_probability(dataset, H, E )
        self.utils.my_print( "Probability Table for: {} & {} :".format( H, E ) )

        print( cMatrix )
        print()

        for h in rowDomain:
            for e in colDomain:
                rowIndex, colIndex = rowDomain.index( h ), colDomain.index( e )
                P_h_e = cMatrix[ rowIndex, colIndex ]
                print( "  P({} | {}) = {:.3f}".format( h, e, P_h_e ) )

        return (rowDomain, colDomain, cMatrix)


    #_______________________________________________________________________________
    # get_error
    def get_error(self, dataset, feature):
        if (isinstance(feature, str)): feature = self.get_variableFrom_str(dataset, feature)
        the_class = dataset.domain.class_var
        (rowDomain, colDomain, cMatrix) = self.compute_probability(dataset, the_class, feature)
        if (not (rowDomain or colDomain)): return ([], [], None)

        errorMatrix = 1 - cMatrix
        return (rowDomain, colDomain, errorMatrix)
    
    #_______________________________________________________________________________
    # error matrix for a given feature and considering the datatset class
    def compute_error(self, dataset, feature):
        (rowDomain, colDomain, errorMatrix) = self.get_error(dataset, feature)
        self.utils.my_print( "Error Table for: {} & {} :".format( dataset.domain.class_var, feature ) )
        print(errorMatrix)
        return (rowDomain, colDomain, errorMatrix)
    
     #_______________________________________________________________________________
    # compute_rule
    def compute_rule(self, attribute, classDomain, featureDomain, errorMatrix ):
        self.utils.my_print( "Rule and error for: {} :".format( attribute) )

        # INIT DICS IN THIS ATRIBUT IDX
        self.dicHypotheses[attribute], self.dicAttrAccuracy[attribute] = [], []
        total, error = 0, 0

        for feature in range(len(featureDomain)):
            errorFeature = errorMatrix[:, feature]
            errorMin = min( errorFeature )
            errorMinIndex = errorFeature.tolist().index( errorMin )
            featureValue = featureDomain[feature]
            classValue = classDomain[errorMinIndex]
            print(f"({attribute}, {featureValue}, {classValue}) : {errorMin:.3f}")

            numberFeatureValues = len([d for d in self.dataset if d[attribute] == featureValue])
            errorValue = numberFeatureValues * errorMin

            astr = f"({attribute}, {featureValue}, {classValue}) : ({int(errorValue)}, {numberFeatureValues})"
            self.dicHypotheses[attribute].append(astr)

            error += errorValue
            total += numberFeatureValues

        # SAVE VALUES
        attrTotalError = error / len(self.dataset)
        self.dicAttrError[attribute] = attrTotalError
        astr = f"{attribute} : ({int(error)}, {total})  # {attrTotalError}"
        self.dicAttrAccuracy[attribute].append(astr)

        print()
        print(f"Total Atribut Error: {attrTotalError}")

    #_______________________________________________________________________________
    # "Main" Function of OneR, (model entryPoint)
    def execute(self):
        print(":: [Staring Executing OneR]")

        # INIT DICS
        self.dicHypotheses = {}
        self.dicAttrAccuracy = {}
        self.dicAttrError = {}
        
        # Iterate over each possible atribute
        for attribute in self.dataset.domain.attributes:
            self.utils.loggHeader(f"{attribute} & {self.dataset.domain.class_var}")
            (classDomain, featureDomain, errorMatrix) = self.compute_error(self.dataset, attribute)
            self.compute_rule(attribute, classDomain, featureDomain, errorMatrix)

        self.minErrorAttr = min(self.dicAttrError, key = self.dicAttrError.get)

        # PRINT RESULTS
        self.utils.loggHeader("Final results:")
        self.utils.print_arr("HYPOTHESES", "- ( attr, valueAttr, valueTarget ) : ( error, total )", self.dicHypotheses)
        self.utils.print_arr("attrACCURACY", "- attr : ( error, total ) # error / total", self.dicAttrAccuracy)
        self.utils.my_print("One-R (Best Rules)")
        print(f"Atributo com menor erro: {self.minErrorAttr}, {self.dicAttrError[self.minErrorAttr]}")
        print("- Reading the rules: if attr is valueAttr then targetClass is valueTarget with x probability of error")
        print("- ( attr, valueAttr, valueTarget ) : (error, total)")
        for element in self.dicHypotheses[self.minErrorAttr]:
            print(element)

        print("\n \n:: [Finished Executing OneR]")


    #_______________________________________________________________________________
    # Export Results
    def export(self, fileName):  
        print(":: [Exporting Results]")
        with open(fileName, "w") as txt_file:
            txt_file.write("(attr, valueAttr, valueTarget) : (error, total)" + "\n")
            for element in self.dicHypotheses[self.minErrorAttr]:
                txt_file.write(element + "\n")
#_______________________________________________________________________________
# main
def main():
    inputFileName = "d01_lenses.tab"
    oneR = OneR(inputFileName)
    oneR.execute()

    outputFileName = "out_oneR.txt"
    oneR.export(outputFileName)
    
if __name__ == "__main__":
    main()
