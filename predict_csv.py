# required libraries
import pandas as pd
from recommender import SHLRecommender   # custom recommender system

def main(k: int = 10, out_path: str = "predictions.csv"):
    """
    Generating predictions for test queries using the SHLRecommender.

    Parameters:
    - k: number of recommendations to retrieve per query (default = 10)
    - out_path: path to save the predictions CSV file
    """

    # Step 1: Initializing the recommender system
    reco = SHLRecommender()

    # Step 2: Loading test queries from CSV
    tests = pd.read_csv("test_queries.csv")

    rows = []  # list to store prediction results for each query

    # Step 3: Iterating through each test query
    for _, r in tests.iterrows():
        q = r["Query"]  # extract query text

        # Step 4: Geting top-k recommendations for the query
        res = reco.recommend(q, k=k, diversify=True)

        # Step 5: Converting results (Name + URL) into a list of dictionaries
        items = res[["Name", "URL"]].to_dict("records")

        # Step 6: Format predictions and URLs as pipe-separated strings
        rows.append({
            "Query": q,
            "predictions": "|".join([x["Name"] for x in items]),
            "urls": "|".join([x["URL"] for x in items])
        })

    # Step 7: Converting results into a DataFrame
    out = pd.DataFrame(rows)

    # Step 8: Saving predictions to CSV
    out.to_csv(out_path, index=False)

    # Step 9: Print confirmation message
    print(f"Saved predictions to {out_path}")

# Entry point: runing main() if script is executed directly
if __name__ == "__main__":
    main(10, "predictions.csv")
