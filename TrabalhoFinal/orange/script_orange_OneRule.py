import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Example dataset (assuming ';' as a separator)
data = pd.read_csv('../scripts/view_export.csv', sep=';')

# Replace path_to_your_dataset.csv with the actual path to your CSV file

# A basic 1R implementation
def oneR(data, target_variable):
    error_rates = {}
    
    for feature in data.columns:
        if feature != target_variable:
            contingency_table = pd.crosstab(index=data[feature], columns=data[target_variable])
            error_rate = 0
            for idx, row in contingency_table.iterrows():
                error_rate += sum(row) - max(row)
            error_rates[feature] = error_rate
    
    best_feature = min(error_rates, key=error_rates.get)
    
    rules = {}
    contingency_table = pd.crosstab(index=data[best_feature], columns=data[target_variable])
    for idx, row in contingency_table.iterrows():
        rules[idx] = row.idxmax()
    
    return best_feature, rules

# Example usage
target_variable = 'lenses'  # replace with your actual target variable
best_feature, rules = oneR(data, target_variable)

# Predictions and Accuracy Calculation
predictions = data[best_feature].map(rules)
accuracy = accuracy_score(data[target_variable], predictions)

print(f"Best feature to predict {target_variable}: {best_feature}")
print(f"Rules: {rules}")
print(f"Accuracy: {accuracy}")
