# OneR

def load_data(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]

    # Extract metadata from the lines
    header = lines[0].split('\t')
    domains_line = lines[1].split('\t')

    # Identify the target
    index_of_class = lines[2].split('\t').index('class')
    target = lines[0].split('\t')[index_of_class]
    print("Target:", target)

    # Construct the domains
    domains = {header[i]: domains_line[i].split() for i in range(len(header))}
    print("Domains:", domains)

    # Extract actual data rows
    data_rows = lines[3:]
    dataset = [row.split('\t') for row in data_rows]

    return dataset, header, target, domains

def oner(data, attributes, target, domains):
    hypotheses = []
    attr_accuracy = {}
    total_data_points = len(data)
    target_index = attributes.index(target)

    for atr_idx, atr in enumerate(attributes):
        if atr == target:  # Skip the target attribute
            continue
        
        print("--------------", atr ,"--------------")
        freq_table = {}  # {(attribute_value, target_value): frequency}
        total_per_atr_val = {}  # {attribute_value: total_count}

        for row in data:
            atr_val, target_val = row[atr_idx], row[target_index]
            freq_table[(atr_val, target_val)] = freq_table.get((atr_val, target_val), 0) + 1
            total_per_atr_val[atr_val] = total_per_atr_val.get(atr_val, 0) + 1

        print("freq_table:", freq_table)
        print("total_per_atr_val:", total_per_atr_val)

        rules = {}
        errors = {}

        for atr_val in domains[atr]:
            best_target_val = None
            max_freq = -1

            for target_val in domains[target]:
                curr_freq = freq_table.get((atr_val, target_val), 0)
                if curr_freq > max_freq:
                    max_freq = curr_freq
                    best_target_val = target_val

            rules[atr_val] = best_target_val
            errors[atr_val] = total_per_atr_val[atr_val] - max_freq

            # Storing the hypotheses
            hypotheses.append((atr, atr_val, best_target_val, errors[atr_val], total_per_atr_val[atr_val]))

        print("rules:", rules)
        print("error:", errors)

        total_error = sum(errors.values())
        attr_accuracy[atr] = (total_error, total_data_points)

    print("---------------------------------\n")
    # Determine the best attribute based on least error
    best_attribute = min(attr_accuracy.keys(), key=lambda atr: attr_accuracy[atr][0])
    best_rules = [(best_attribute, atr_val, rules[atr_val], errors[atr_val], total_per_atr_val[atr_val]) for atr_val in rules.keys()]

    return hypotheses, attr_accuracy, best_rules

# Load the dataset from the file
filename = 'd01_lenses.tab'
dataset, attributes, target, domains = load_data(filename)

# Reuse the earlier OneR function with the new dataset
hypotheses, attr_accuracy, best_rules = oner(dataset, attributes, target, domains)

# Display the result
print("- HYPOTHESES")
for entry in hypotheses:
    print(f"({entry[0]}, {entry[1]}, {entry[2]}) : ({entry[3]}, {entry[4]})")

print("\n- attrACCURACY")
for attr, acc in attr_accuracy.items():
    print(f"{attr} : ({acc[0]}, {acc[1]}) # {acc[0]/acc[1]:.4f}")

print("\n- One-R")
for entry in best_rules:
    print(f"({entry[0]}, {entry[1]}, {entry[2]}) : ({entry[3]}, {entry[4]})")
