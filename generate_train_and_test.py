# Importing pandas for data manipulation
import pandas as pd

def generate_train_and_test(dataset_path="Gen_AI Dataset.csv",
                            train_path="labeled_train.csv",
                            test_path="test_queries.csv",
                            train_ratio=0.8):
    """
    Spliting a dataset into training and test sets for recommender evaluation.

    Parameters:
    - dataset_path: path to the full dataset CSV
    - train_path: path to save the training set
    - test_path: path to save the test set
    - train_ratio: proportion of data to use for training (default 0.8)
    """

    # Step 1: Loading the dataset from CSV
    df = pd.read_csv(dataset_path)

    # Step 2: Shuffling the dataset for randomness
    # frac=1 → shuffling all rows
    # random_state=42 → ensures reproducibility
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Step 3: Spliting into train and test sets
    train_size = int(len(df) * train_ratio)   # number of rows for training
    train_df = df.iloc[:train_size]           # first part → training set
    test_df = df.iloc[train_size:]            # remaining part → test set

    # Step 4: Saving labeled training set
    # Includes both queries and their relevant assessment URLs
    train_df[["Query", "Assessment_url"]].to_csv(train_path, index=False)

    # Step 5: Saving test set
    # Only queries are saved (no labels) for evaluation
    test_df[["Query"]].to_csv(test_path, index=False)

    # Step 6: Printing summary of saved files
    print(f"Saved {len(train_df)} rows to {train_path}")
    print(f"Saved {len(test_df)} rows to {test_path}")

# Entry point: runing function if script is executed directly
if __name__ == "__main__":
    generate_train_and_test()
    