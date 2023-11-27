import pandas as pd
import numpy as np

# Create attribute domain header 
discreteHeader = np.full((1, 23), "discrete")

# Create attibute class header 
classHeader = np.append(np.array(["class"]), np.full((1, 22), " "))

# Read original csv file
df = pd.read_csv('dataset_long_name_ORIGINAL.csv')

# Concatenate the headers with the data (1st: domain header, 2nd: class header, 3rd: data)
finalDataset = pd.DataFrame(discreteHeader, columns=df.columns)ithz
finalDataset.loc[1] = classHeader.T
finalDataset = pd.concat([finalDataset, df])

# Drop the last line filled with "-"
finalDataset = finalDataset.drop([len(df.index) - 1])

# Saves dataset with headers in .tab file
finalDataset.to_csv('dataset_long_name_ORIGINAL.tab', sep='\t', index=False)
