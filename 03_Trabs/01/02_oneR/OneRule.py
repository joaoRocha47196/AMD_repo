from collections import defaultdict
import Orange
import json
import random

class OneR:
    def __init__(self, filename):
        self.dataset, self.attributes, self.target, self.domains = self.load_data(filename)
        self.freq_tables, self.total_per_atr_val = None, None
        self.hypotheses, self.attr_accuracy, self.best_rules, self.best_attribute = None, None, None, None

    def load_data(self, filename):
        data = Orange.data.Table(filename)
        attributes = [var.name for var in data.domain.attributes]
        target = data.domain.class_var.name
        domains = {attr.name: list(attr.values) for attr in data.domain}

        return data, attributes, target, domains

    def compute_frequency_tables(self):
        freq_tables = {}
        total_per_atr_val = defaultdict(lambda: defaultdict(int))

        for atr in self.attributes:
            freq_table = defaultdict(int)

            for row in self.dataset:
                atr_val, target_val = str(row[atr]), str(row[self.target])
                freq_table[(atr_val, target_val)] += 1
                total_per_atr_val[atr][atr_val] += 1

            freq_tables[atr] = dict(freq_table)

        self.freq_tables = freq_tables
        self.total_per_atr_val = total_per_atr_val

    def compute_rules_and_errors(self):
        self.hypotheses, self.attr_accuracy = [], {}

        for atr in self.attributes:
            rules = {}
            errors = {}
            for atr_val in self.domains[atr]:
                best_target_val = None
                max_freq = -1

                for target_val in self.domains[self.target]:
                    curr_freq = self.freq_tables[atr].get((atr_val, target_val), 0)
                    if curr_freq > max_freq:
                        max_freq, best_target_val = curr_freq, target_val

                if best_target_val is not None:  #rule was actually found
                    rules[atr_val] = best_target_val
                    errors[atr_val] = self.total_per_atr_val[atr][atr_val] - max_freq
                    self.hypotheses.append((atr, atr_val, best_target_val, errors[atr_val]))

            self.attr_accuracy[atr] = (sum(errors.values()), len(self.dataset))

        # best attributes based on the lowest error rate
        lowest_error = min(self.attr_accuracy.values(), key=lambda x: x[0])[0]
        self.best_attributes = [atr for atr, (errors, _) in self.attr_accuracy.items() if errors == lowest_error]

        # hypotheses with the lowest error rate
        best_hypotheses = {}
        for atr, atr_val, target_val, error in self.hypotheses:
            if atr in self.best_attributes:
                total_instances = self.total_per_atr_val[atr][atr_val]
                if atr not in best_hypotheses:
                    best_hypotheses[atr] = {atr_val: (target_val, error, total_instances)}
                elif atr_val not in best_hypotheses[atr]:
                    best_hypotheses[atr][atr_val] = (target_val, error, total_instances)
                elif error < best_hypotheses[atr][atr_val][1]:
                    best_hypotheses[atr][atr_val] = (target_val, error, total_instances)

        # best rules from the best hypotheses
        self.best_rules = {atr: {atr_val: (target_val, error, total_instances) for atr_val, (target_val, error, total_instances) in atr_vals.items()}
                        for atr, atr_vals in best_hypotheses.items()}
        print("best_rules:",self.best_rules)
        
    
    def predict(self, instance):
        print("\n- PREDICT")
        class_votes = {target_class: 0 for target_class in self.domains[self.target]}

        for atr in self.best_attributes:
            atr_val = instance.get(atr)
            if atr_val and atr_val in self.best_rules[atr]:
                predicted_class = self.best_rules[atr][atr_val][0]  #  get the target_class
                print("predicted_class:", predicted_class)
                class_votes[predicted_class] += 1

        # In case of ties or no rules applied, use a random prediction
        most_votes = max(class_votes.values())
        most_probable_classes = [cls for cls, votes in class_votes.items() if votes == most_votes]
        
        if not most_probable_classes or most_votes == 0:
            return random.choice(list(self.domains[self.target]))

        return random.choice(most_probable_classes)


    def print_hypotheses(self):
        print("- HYPOTHESES")
        for entry in self.hypotheses:
            print(f"({entry[0]}, {entry[1]}, {entry[2]}) : {entry[3]}")

    def print_attr_accuracy(self):
        print("\n- ATTRIBUTE ACCURACY")
        for attr, acc in self.attr_accuracy.items():
            print(f"{attr} : {acc[0]} errors out of {acc[1]} instances # Error rate: {acc[0] / acc[1]:.4f}")

    def print_best_rules(self):
        print("\n- BEST RULES:")
        for atr in self.best_attributes:
            print(f"For attribute '{atr}':")
            for atr_val, (target_class, error, total) in self.best_rules[atr].items():
                error_probability = f"{error}/{total}"
                print(f"If {atr} is {atr_val}, then lenses = {target_class} # Error Probability: {error_probability}")


    def save_model(self, file_path):
        json_compatible_best_rules = {atr: {atr_val: list(values) for atr_val, values in atr_vals.items()}
                                    for atr, atr_vals in self.best_rules.items()}
        
        with open(file_path, 'w') as f:
            json.dump(json_compatible_best_rules, f, indent=4)


def main():
    filename = 'd01_lenses.tab'
    one_r_classifier = OneR(filename)
    one_r_classifier.compute_frequency_tables()
    one_r_classifier.compute_rules_and_errors()
    one_r_classifier.print_hypotheses()
    one_r_classifier.print_attr_accuracy()
    one_r_classifier.print_best_rules()

    # Prediction:
    new_instance = {'age': 'young', 'prescription': 'myope', 'astigmatic': 'yes', 'tear_rate': 'normal'}
    prediction = one_r_classifier.predict(new_instance)
    print(f"Prediction for the input values: {prediction}")

    # Save Best Rules
    one_r_classifier.save_model('one_r_model.json')
if __name__ == "__main__":
    main()


