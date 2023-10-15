import Orange
import pandas as pd
from collections import Counter
from sklearn.metrics import accuracy_score

class OneRClassifier(Orange.classification.Learner):
    """A basic 1R classifier for Orange."""
    
    name = "oneR"
    
    def fit_storage(self, data):
        """Create rules from the input data."""
        data = pd.DataFrame(data.X, columns=[var.name for var in data.domain.attributes])
        data['target'] = data.Y.astype(int)
        
        best_feature, rules = self.oneR(data, 'target')
        return OneRClassifier.RuleClassifier(domain=data.domain, feature=best_feature, rules=rules)
    
    class RuleClassifier(Orange.classification.Model):
        """Classifier: stored rules and applies them to new data."""
        def __init__(self, domain, feature, rules):
            super().__init__(domain)
            self.feature = feature
            self.rules = rules
        
        def predict(self, X):
            data = pd.DataFrame(X, columns=[var.name for var in self.domain.attributes])
            predictions = data[self.feature].map(self.rules).values
            return predictions.reshape((len(predictions), 1)), None
    
    def oneR(self, data, target_variable):
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
# Load data
data = Orange.data.Table('./d01_lenses.tab')  # Replace with the path to your .tab file

# Initialize and run learner
one_r_learner = OneRClassifier()
one_r_classifier = one_r_learner(data)

# Evaluate accuracy
correct = 0
total = len(data)
for example in data:
    if one_r_classifier(example)[0] == int(example.get_class()):
        correct += 1

accuracy = correct / total

print(f"Accuracy: {accuracy}")
