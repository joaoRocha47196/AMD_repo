import csv
from collections import defaultdict

def load_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    return data

def oneR(data):
    headers = data[0]
    data = data[1:]
    min_error_feature = None
    min_error = float("inf")
    best_rules = {}
    
    for feature_idx in range(len(headers) - 1):  # Excluding the class variable
        # Counting how many times a feature value and class value occur together
        freq_table = defaultdict(lambda: defaultdict(int))
        
        for row in data:
            feature_value = row[feature_idx]
            class_value = row[-1]
            freq_table[feature_value][class_value] += 1
        
        # Finding the most frequent class for each feature value
        rules = {}
        feature_error = 0
        for feature_idx in range(len(headers) - 1):  # Excluding the class variable
            freq_table = defaultdict(lambda: defaultdict(int))
            
            for row in data:
                feature_value = row[feature_idx]
                class_value = row[-1]
                freq_table[feature_value][class_value] += 1

            print(f"Freq Table for {headers[feature_idx]}: {dict(freq_table)}")  # Debugging line

        # Updating the best rule if this feature has fewer errors
        if feature_error < min_error:
            min_error = feature_error
            min_error_feature = headers[feature_idx]
            best_rules = rules
            
    print(f"Best 1R feature: {min_error_feature}")
    print(f"Rules: {best_rules}")
    return min_error_feature, best_rules

data = load_data('../scripts/view_export.csv')
feature, rules = oneR(data)
