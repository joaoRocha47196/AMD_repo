from collections import defaultdict
import Orange

class OneR:
    def __init__(self, filename):
        self.dataset, self.attributes, self.target, self.domains = self.load_data(filename)
        self.freq_tables, self.total_per_atr_val = None, None
        self.hypotheses, self.attr_accuracy, self.best_rules = None, None, None

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
        hypotheses, attr_accuracy,  best_rules = [], {}, {}

        for atr in self.attributes:
            rules = {}
            errors = {}
            for atr_val in self.domains[atr]:
                best_target_val = None
                max_freq = -1

                for target_val in self.domains[self.target]:
                    curr_freq = self.freq_tables[atr].get((atr_val, target_val), 0)
                    if curr_freq > max_freq:
                        max_freq = curr_freq
                        best_target_val = target_val

                rules[atr_val] = best_target_val
                errors[atr_val] = self.total_per_atr_val[atr][atr_val] - max_freq
                hypotheses.append((atr, atr_val, best_target_val, errors[atr_val], self.total_per_atr_val[atr][atr_val]))

            total_error = sum(errors.values())
            attr_accuracy[atr] = (total_error, len(self.dataset))

            # Determine the best attribute based on least error
            best_attribute = min(attr_accuracy.keys(), key=lambda atr: attr_accuracy[atr][0])
            best_rules = [(best_attribute, atr_val, rules[atr_val], errors[atr_val], self.total_per_atr_val[atr][atr_val]) for atr_val in rules.keys()]

            self.hypotheses = hypotheses
            self.attr_accuracy = attr_accuracy
            self.best_rules = best_rules




    def print_hypotheses(self):
        print("- HYPOTHESES")
        for entry in self.hypotheses:
            print(f"({entry[0]}, {entry[1]}, {entry[2]}) : ({entry[3]}, {entry[4]})")

    def print_attr_accuracy(self):
        print("\n- attrACCURACY")
        for attr, acc in self.attr_accuracy.items():
            print(f"{attr} : ({acc[0]}, {acc[1]}) # {acc[0] / acc[1]:.4f}")

    def print_best_rules(self):
        print("\n- One-R")
        for entry in self.best_rules:
            print(f"({entry[0]}, {entry[1]}, {entry[2]}) : ({entry[3]}, {entry[4]})")



# Usage
filename = 'd01_lenses.tab'
one_r_classifier = OneR(filename)
one_r_classifier.compute_frequency_tables()
one_r_classifier.compute_rules_and_errors()
one_r_classifier.print_hypotheses()
one_r_classifier.print_attr_accuracy()
one_r_classifier.print_best_rules()
