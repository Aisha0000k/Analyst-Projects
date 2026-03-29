"""
SpaceX Falcon 9 Landing Prediction Machine Learning Module

I build and evaluate machine learning models to predict whether
the Falcon 9 first stage will land successfully. I test multiple
classification algorithms including Logistic Regression, SVM,
Decision Trees, and K-Nearest Neighbors.

Author: Yaseen
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report


DATASET_PART_2_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
DATASET_PART_3_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv"


def load_datasets():
    """
    I load both datasets: one with outcomes for labels,
    one with engineered features for training.

    Returns:
        tuple: (data DataFrame, X features DataFrame)
    """
    data = pd.read_csv(DATASET_PART_2_URL)
    X = pd.read_csv(DATASET_PART_3_URL)
    return data, X


def extract_labels(data):
    """
    I extract the Class column as the target variable.

    Args:
        data: DataFrame with Class column

    Returns:
        ndarray: Label array (0 = no landing, 1 = successful landing)
    """
    Y = data["Class"].to_numpy()
    return Y


def standardize_features(X):
    """
    I standardize the features using StandardScaler for
    better model performance.

    Args:
        X: Feature matrix

    Returns:
        ndarray: Standardized features
    """
    transform = preprocessing.StandardScaler()
    X = transform.fit_transform(X)
    return X


def split_data(X, Y, test_size=0.2, random_state=2):
    """
    I split the data into training and testing sets.

    Args:
        X: Feature matrix
        Y: Labels
        test_size: Proportion for testing
        random_state: Random seed for reproducibility

    Returns:
        tuple: (X_train, X_test, Y_train, Y_test)
    """
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, Y_train, Y_test


def plot_confusion_matrix(y_true, y_pred):
    """
    I create a heatmap visualization of the confusion matrix.

    Args:
        y_true: Actual labels
        y_pred: Predicted labels
    """
    cm = confusion_matrix(y_true, y_pred)
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax)
    ax.set_xlabel("Predicted labels")
    ax.set_ylabel("True labels")
    ax.set_title("Confusion Matrix")
    ax.xaxis.set_ticklabels(["did not land", "land"])
    ax.yaxis.set_ticklabels(["did not land", "landed"])
    plt.show()


def train_logistic_regression(X_train, Y_train):
    """
    I train a Logistic Regression model with hyperparameter tuning
    using GridSearchCV.

    Args:
        X_train: Training features
        Y_train: Training labels

    Returns:
        GridSearchCV: Fitted model with best parameters
    """
    parameters = {"C": [0.01, 0.1, 1], "penalty": ["l2"], "solver": ["lbfgs"]}

    lr = LogisticRegression()
    logreg_cv = GridSearchCV(lr, parameters, cv=10)
    logreg_cv.fit(X_train, Y_train)

    return logreg_cv


def train_svm(X_train, Y_train):
    """
    I train a Support Vector Machine model with hyperparameter tuning.

    Args:
        X_train: Training features
        Y_train: Training labels

    Returns:
        GridSearchCV: Fitted model with best parameters
    """
    parameters = {"C": [0.1, 1, 10], "kernel": ["rbf"], "gamma": ["auto", "scale"]}

    svm = SVC()
    svm_cv = GridSearchCV(svm, parameters, cv=10)
    svm_cv.fit(X_train, Y_train)

    return svm_cv


def train_decision_tree(X_train, Y_train):
    """
    I train a Decision Tree classifier with hyperparameter tuning.

    Args:
        X_train: Training features
        Y_train: Training labels

    Returns:
        GridSearchCV: Fitted model with best parameters
    """
    parameters = {"criterion": ["gini", "entropy"], "max_depth": [2, 4, 6, 8]}

    tree = DecisionTreeClassifier()
    tree_cv = GridSearchCV(tree, parameters, cv=10)
    tree_cv.fit(X_train, Y_train)

    return tree_cv


def train_knn(X_train, Y_train):
    """
    I train a K-Nearest Neighbors classifier with hyperparameter tuning.

    Args:
        X_train: Training features
        Y_train: Training labels

    Returns:
        GridSearchCV: Fitted model with best parameters
    """
    parameters = {"n_neighbors": [3, 5, 7, 9]}

    knn = KNeighborsClassifier()
    knn_cv = GridSearchCV(knn, parameters, cv=10)
    knn_cv.fit(X_train, Y_train)

    return knn_cv


def evaluate_model(model, X_test, Y_test, model_name):
    """
    I evaluate a trained model on test data and print results.

    Args:
        model: Trained model
        X_test: Test features
        Y_test: Test labels
        model_name: Name for display

    Returns:
        float: Test accuracy
    """
    accuracy = model.score(X_test, Y_test)
    print(f"\n=== {model_name} ===")
    print(f"Best Parameters: {model.best_params_}")
    print(f"Training Accuracy: {model.best_score_:.4f}")
    print(f"Test Accuracy: {accuracy:.4f}")

    y_pred = model.predict(X_test)
    print(f"\nClassification Report:")
    print(classification_report(Y_test, y_pred))

    plot_confusion_matrix(Y_test, y_pred)

    return accuracy


def run_machine_learning():
    """
    I orchestrate the complete ML pipeline:
    load data, train multiple models, and compare performance.
    """
    print("=== Loading Data ===")
    data, X = load_datasets()
    print(f"Data shape: {data.shape}")
    print(f"Features shape: {X.shape}")

    print("\n=== Preparing Labels ===")
    Y = extract_labels(data)
    print(f"Labels: {len(Y)} samples")

    print("\n=== Standardizing Features ===")
    X = standardize_features(X)

    print("\n=== Splitting Data ===")
    X_train, X_test, Y_train, Y_test = split_data(X, Y)
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")

    print("\n=== Training Models ===")

    lr_model = train_logistic_regression(X_train, Y_train)
    lr_accuracy = evaluate_model(lr_model, X_test, Y_test, "Logistic Regression")

    svm_model = train_svm(X_train, Y_train)
    svm_accuracy = evaluate_model(svm_model, X_test, Y_test, "SVM")

    tree_model = train_decision_tree(X_train, Y_train)
    tree_accuracy = evaluate_model(tree_model, X_test, Y_test, "Decision Tree")

    knn_model = train_knn(X_train, Y_train)
    knn_accuracy = evaluate_model(knn_model, X_test, Y_test, "KNN")

    print("\n=== Model Comparison ===")
    results = {
        "Logistic Regression": lr_accuracy,
        "SVM": svm_accuracy,
        "Decision Tree": tree_accuracy,
        "KNN": knn_accuracy,
    }

    for model_name, accuracy in sorted(
        results.items(), key=lambda x: x[1], reverse=True
    ):
        print(f"  {model_name}: {accuracy:.4f}")

    best_model = max(results, key=results.get)
    print(f"\nBest Model: {best_model} with {results[best_model]:.4f} accuracy")


if __name__ == "__main__":
    run_machine_learning()
