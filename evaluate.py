# required libraries
import pandas as pd
import numpy as np
from recommender import SHLRecommender   # custom recommender system

def recall_at_k(preds: list[str], gold: list[str], k: int) -> float:
    """
    Computing recall@k for a single query.
    - preds: list of predicted assessment names
    - gold: list of ground-truth (correct) assessment names
    - k: number of top predictions to consider

    Recall@k = (# of relevant items retrieved in top-k) / (total # of relevant items)
    """
    if not gold:  # If no ground-truth labels, recall is 0
        return 0.0
    topk = preds[:k]  # Taking top-k predictions
    # Normalizing strings (strip whitespace, lowercase) and compute intersection
    hits = len(set(x.strip().lower() for x in topk) & set(x.strip().lower() for x in gold))
    return hits / len(gold)  # Fraction of relevant items retrieved

def main(k: int = 10):
    """
    Evaluating the recommender system on a labeled dataset using recall@k.
    """
    # Initializing recommender
    reco = SHLRecommender()

    # Loading labeled training data (contains queries and ground-truth assessments)
    df = pd.read_csv("labeled_train.csv")

    recalls = []  # storing recall scores for each query

    # Iterating through each row in the dataset
    for _, row in df.iterrows():
        query = row["Query"]  # recruiter/job description query
        # Ground-truth assessments are stored as '|' separated URLs
        gold = [x for x in str(row["Assessment_url"]).split("|") if x.strip()]

        # Get recommender predictions for this query
        res = reco.recommend(query, k=k, diversify=True)
        preds = res["Name"].tolist()  # predicted assessment names

        # Compute recall@k for this query
        r = recall_at_k(preds, gold, k)
        recalls.append(r)

    # Compute mean recall across all queries
    mean_recall = float(np.mean(recalls)) if recalls else 0.0
    print(f"Mean Recall@{k}: {mean_recall:.4f}")

# Entry point: runing evaluation when script is executed directly
if __name__ == "__main__":
    main(10)
