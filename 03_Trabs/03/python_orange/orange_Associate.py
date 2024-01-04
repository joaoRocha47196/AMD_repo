import Orange
from orangecontrib.associate.fpgrowth import *

Xbasket = Orange.data.Table(".\zz_dataset_2012_01.basket")
X, mapping = OneHot.encode(Xbasket)

maxR = 12
min_support = 0.01
max_support = 0.1
step_support = 0.01 
min_confidence = 0.5
max_confidence = 1.0
step_confidence = 0.1

for support in range(int(min_support * 100), int(max_support * 100), int(step_support * 100)):
    support /= 100
    itemsets = dict(frequent_itemsets(X, support))

    for confidence in range(int(min_confidence * 100), int(max_confidence * 100), int(step_confidence * 100)):
        confidence /= 100
        rules = list(association_rules(itemsets, confidence))
        print(len(rules), "- support:", support, "confidence:", confidence)
        if len(rules) <= maxR:
            print(f"\nSupport: {support}, Confidence: {confidence}, Number of Rules: {len(rules)}")
            for rule in rules:
                LHS, RHS, rule_support, rule_confidence = rule
                decoded_LHS = [var.name for _, var, _ in OneHot.decode(LHS, Xbasket, mapping)]
                decoded_RHS = [var.name for _, var, _ in OneHot.decode(RHS, Xbasket, mapping)]
                print(f"--> Rule: {decoded_LHS} -> {decoded_RHS}, Support: {rule_support}, Confidence: {rule_confidence}")
            break
