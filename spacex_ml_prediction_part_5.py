"""SpaceX Falcon 9 first stage landing prediction.

This script is a runnable Python version of the notebook exported as HTML.
"""

# I am predicting whether the Falcon 9 first stage lands successfully.
# I care about this because reusability affects launch cost, and that cost matters
# when comparing SpaceX with other launch providers.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
)
FEATURES_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv"
)


# I use this helper to visualize how each model performs on the test set.
def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, title: str) -> None:
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(5, 4))
    ax = sns.heatmap(cm, annot=True, fmt="d")
    ax.set_xlabel("Predicted labels")
    ax.set_ylabel("True labels")
    ax.set_title(title)
    ax.xaxis.set_ticklabels(["did not land", "land"])
    ax.yaxis.set_ticklabels(["did not land", "landed"])
    plt.tight_layout()
    plt.show()


# I load the response column and the engineered feature set from the course dataset.
data = pd.read_csv(DATA_URL)
X = pd.read_csv(FEATURES_URL)

print("data shape:", data.shape)
print("feature shape:", X.shape)
print("\nFirst rows of target dataframe:")
print(data.head())
print("\nFirst rows of feature dataframe:")
print(X.head())


# I convert the landing outcome into a NumPy array so I can train models with it.
Y = data["Class"].to_numpy()

# I standardize the feature matrix before fitting the models.
scaler = preprocessing.StandardScaler()
X = scaler.fit_transform(X)

# I split the data into training and test sets and keep 20% for testing.
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=2
)
print("\nTest set shape:", Y_test.shape)


results = {}

# I start with logistic regression and tune a small grid of hyperparameters.
logreg_parameters = {
    "C": [0.01, 0.1, 1],
    "penalty": ["l2"],
    "solver": ["lbfgs"],
}
logreg = LogisticRegression(max_iter=1000)
logreg_cv = GridSearchCV(logreg, logreg_parameters, cv=10)
logreg_cv.fit(X_train, Y_train)

print("\nLogistic Regression")
print("best parameters:", logreg_cv.best_params_)
print("cross-validation accuracy:", logreg_cv.best_score_)
print("test accuracy:", logreg_cv.score(X_test, Y_test))
results["Logistic Regression"] = logreg_cv.score(X_test, Y_test)
plot_confusion_matrix(
    Y_test,
    logreg_cv.predict(X_test),
    "Logistic Regression Confusion Matrix",
)

# I note that the test set is small, so I should not over-interpret any one score.
# I also use the confusion matrix to see whether the model makes false positives or false negatives.

# I train a support vector machine with a grid over kernels, C, and gamma.
svm_parameters = {
    "kernel": ["linear", "rbf", "poly", "sigmoid"],
    "C": np.logspace(-3, 3, 5),
    "gamma": np.logspace(-3, 3, 5),
}
svm = SVC()
svm_cv = GridSearchCV(svm, svm_parameters, cv=10)
svm_cv.fit(X_train, Y_train)

print("\nSupport Vector Machine")
print("best parameters:", svm_cv.best_params_)
print("cross-validation accuracy:", svm_cv.best_score_)
print("test accuracy:", svm_cv.score(X_test, Y_test))
results["SVM"] = svm_cv.score(X_test, Y_test)
plot_confusion_matrix(
    Y_test,
    svm_cv.predict(X_test),
    "SVM Confusion Matrix",
)

# I train a decision tree and search over several structure-related hyperparameters.
tree_parameters = {
    "criterion": ["gini", "entropy"],
    "splitter": ["best", "random"],
    "max_depth": [2 * n for n in range(1, 10)],
    "max_features": [None, "sqrt", "log2"],
    "min_samples_leaf": [1, 2, 4],
    "min_samples_split": [2, 5, 10],
}
tree = DecisionTreeClassifier(random_state=2)
tree_cv = GridSearchCV(tree, tree_parameters, cv=10)
tree_cv.fit(X_train, Y_train)

print("\nDecision Tree")
print("best parameters:", tree_cv.best_params_)
print("cross-validation accuracy:", tree_cv.best_score_)
print("test accuracy:", tree_cv.score(X_test, Y_test))
results["Decision Tree"] = tree_cv.score(X_test, Y_test)
plot_confusion_matrix(
    Y_test,
    tree_cv.predict(X_test),
    "Decision Tree Confusion Matrix",
)

# I train KNN and tune the number of neighbors, search algorithm, and distance metric.
knn_parameters = {
    "n_neighbors": list(range(1, 11)),
    "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
    "p": [1, 2],
}
knn = KNeighborsClassifier()
knn_cv = GridSearchCV(knn, knn_parameters, cv=10)
knn_cv.fit(X_train, Y_train)

print("\nK Nearest Neighbors")
print("best parameters:", knn_cv.best_params_)
print("cross-validation accuracy:", knn_cv.best_score_)
print("test accuracy:", knn_cv.score(X_test, Y_test))
results["KNN"] = knn_cv.score(X_test, Y_test)
plot_confusion_matrix(
    Y_test,
    knn_cv.predict(X_test),
    "KNN Confusion Matrix",
)

# I compare the final test accuracies to see which method performs best on this split.
print("\nFinal test accuracies")
for model_name, score in results.items():
    print(f"{model_name}: {score:.4f}")

best_model_name = max(results, key=results.get)
print("\nBest method:", best_model_name)
