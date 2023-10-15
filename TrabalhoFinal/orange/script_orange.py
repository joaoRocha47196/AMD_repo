import Orange

# Load data
data = Orange.data.Table("../scripts/view_export.csv")
# data = Orange.data.Table("./d01_lenses.tab")

# Make a new variable based on 'lenses' but make sure it's discrete
new_lenses = Orange.data.DiscreteVariable('lenses', values=list(map(str, data.domain['lenses'].values)))

# Make a new domain with 'lenses' as a discrete class_var
new_domain = Orange.data.Domain(data.domain.attributes, new_lenses)

# Associate the new domain with data
data = Orange.data.Table(new_domain, data)

# Initialize a learner
learner = Orange.classification.MajorityLearner()

# Train a classifier
classifier = learner(data)

# Evaluate the model
res = Orange.evaluation.testing.CrossValidation(data, [learner], k=5)
acc = Orange.evaluation.CA(res)
print("Accuracy: %.3f" % acc[0])