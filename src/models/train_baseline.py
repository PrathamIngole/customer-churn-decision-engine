from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
from pathlib import Path

from data.load_data import load_raw_data

from data.column_audit import (
    IDENTIFIER_COLUMNS,
    LEAKAGE_COLUMNS,
    LOCATION_METADATA_COLUMNS,
    VALID_FEATURE_COLUMNS
)

def prepare_dataset() :
    """
    Prepare feature matrix (X) and target vector (y)
    for baseline modeling.
    """

    df = load_raw_data()

    # Ensure correct dtypes
    df["Tenure Months"] = df["Tenure Months"].astype(int)
    df["Monthly Charges"] = df["Monthly Charges"].astype(float)

    # Total Charges (Convert to numeric and handle blanks)
    df["Total Charges"] = pd.to_numeric(df["Total Charges"], errors = "coerce")
    # Drop rows where Total Charges become NaN
    df["Total Charges"] = df["Total Charges"].fillna(0)

    # Drop identifiers, leakage, and location 
    columns_to_drop = (
        IDENTIFIER_COLUMNS 
        + LEAKAGE_COLUMNS
        + LOCATION_METADATA_COLUMNS 
    )

    df = df.drop(columns = columns_to_drop)



    # Target Variable 
    y = df["Churn Label"]

    # Feature Matrix (explicitly controlled)
    X = df[VALID_FEATURE_COLUMNS]

    return X, y

def split_dataset(X, y, test_size = 0.2, random_state = 42) :
    """
    Split dataset into train and test sets.
    """
    X_train , X_test, y_train, y_test = train_test_split(
        X, 
        y, 
        test_size= test_size,
        random_state=random_state,
        stratify=y # Important for Imbalanced Data
    )

    return  X_train, X_test, y_train, y_test

def build_baseline_model(X_train) :
    """
        Build baseline Logistic Regression pipeline.
    """

    # Identify categorical and numeric columns
    categorical_cols = X_train.select_dtypes(include = "str").columns.tolist()  
    numerical_cols = X_train.select_dtypes(exclude = "str").columns.tolist()

    # preprocessing 
    preprocessor = ColumnTransformer(
        transformers = [
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("num", StandardScaler(), numerical_cols)
        ]
    )

    # Logistic Regression model 
    model = LogisticRegression(max_iter = 1000)

    # Full pipeline
    pipeline = Pipeline(
        steps = [
            ("preprocessor", preprocessor),
            ("classifier", model)
        ]
    )

    return pipeline

def build_baseline_tree() :
    """
        Build a simple Decision Tree classifier.
    """
    
    model = DecisionTreeClassifier(
        max_depth=None, 
        random_state=42
    )

    return model

def build_tree_pipeline(X_train) :

    categorical_cols = X_train.select_dtypes(include = "str").columns.tolist()
    numeric_cols = X_train.select_dtypes(exclude = "str").columns.tolist()

    preprocessor = ColumnTransformer(
        transformers = [
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("num", "passthrough", numeric_cols)
        ]
    )

    tree = DecisionTreeClassifier(
        max_depth=5, 
        random_state=42
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", tree)
        ]
    )

    return pipeline

def build_random_forest_pipeline(X_train) : 

    categorical_cols = X_train.select_dtypes(include = "str").columns.tolist()
    numeric_cols = X_train.select_dtypes(exclude = "str").columns.tolist()

    preprocessor = ColumnTransformer(
        transformers= [
            ("cat", OneHotEncoder(handle_unknown='ignore'), categorical_cols),
            ("num", "passthrough", numeric_cols)

        ]
    )

    rf = RandomForestClassifier(
        n_estimators=200, 
        max_depth=7,
        random_state=42,
        n_jobs=-1
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", rf)
        ]
    )

    return pipeline

def train_and_save_model(model_path : str = "models/logistic_churn_model.joblib") :
    """
    Docstring for train_and_save_model
    
    :param model_path: Description
    :type model_path: str

             =    Train Logistic Regression on full training data and save the trained pipeline.

    """

    X, y = prepare_dataset()

    X_train, X_test, y_train, y_test = split_dataset(X, y)

    model = build_baseline_model(X_train)

    model.fit(X_train, y_train)

    # Ensure models directory exists

    model_path = Path(model_path)
    model_path.parent.mkdir(parents = True, exist_ok = True)

    joblib.dump(model, model_path)

    return model




if __name__ == "__main__" : 
    train_and_save_model()