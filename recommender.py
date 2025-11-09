# required libraries
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from utils import clean_text, categorize_query   # custom utility functions

class SHLRecommender:
    def __init__(self,
                 catalog_path="shl_assessments.csv",
                 index_path="assessments.index",
                 model_name="all-MiniLM-L6-v2"):
        """
        Initializing the recommender system.
        - catalog_path: path to the catalog CSV containing assessments
        - index_path: path to the FAISS index file
        - model_name: sentence transformer model for embeddings
        """
        # Loading catalog of assessments
        self.df = pd.read_csv(catalog_path)
        # Loading prebuilt FAISS index
        self.index = faiss.read_index(index_path)
        # Loading sentence transformer model
        self.model = SentenceTransformer(model_name)

        # Precomputing category lookup for convenience
        self.categories = self.df["Category"].tolist()

    def _encode(self, text: str) -> np.ndarray:
        """
        Encoding a query string into a normalized embedding vector.
        """
        emb = self.model.encode([text], convert_to_numpy=True)
        faiss.normalize_L2(emb)  # normalizing for cosine similarity
        return emb

    def _diversify(self, rows: pd.DataFrame, desired_mix: dict, k: int = 10) -> pd.DataFrame:
        """
        Diversifying recommendations based on desired category mix.
        - rows: candidate recommendations with scores
        - desired_mix: dict specifying how many items per category (e.g. {"Coding": 4, "Behavior": 3})
        - k: total number of recommendations to return
        """
        picked = []  # list of selected rows
        counts = {cat: 0 for cat in desired_mix.keys()}  # track counts per category

        # First pass: honor desired category counts
        for _, r in rows.iterrows():
            cat = r["Category"]
            if cat in desired_mix and counts[cat] < desired_mix[cat]:
                picked.append(r)
                counts[cat] += 1
                if len(picked) == k:
                    break

        # Second pass: filling remaining slots with best-scoring leftovers
        if len(picked) < k:
            existing_ids = {id(x) for x in picked}
            for _, r in rows.iterrows():
                if id(r) not in existing_ids:
                    picked.append(r)
                    if len(picked) == k:
                        break

        # Returns diversified DataFrame
        return pd.DataFrame(picked)

    def recommend(self, query: str, k: int = 10, diversify: bool = True) -> pd.DataFrame:
        """
        Generating top-k recommendations for a given query.
        - query: input text (job description, recruiter query, etc.)
        - k: number of recommendations to return
        - diversify: whether to balance recommendations across categories
        """
        # Cleaning query text
        query = clean_text(query)
        # Encoding query into embedding
        emb = self._encode(query)
        # Searching FAISS index for nearest neighbors
        scores, idxs = self.index.search(emb, max(k * 3, 30))  # retrieve more candidates for diversification

        # Retrieving candidate rows from catalog
        candidates = self.df.iloc[idxs[0]].copy()
        candidates["Score"] = scores[0]

        # If diversification is disabled, return top-k directly
        if not diversify:
            return candidates.head(k)[["Name", "URL", "Category", "Score"]]

        # Determining desired category mix based on query intents
        intents = categorize_query(query)
        desired_mix = {}

        if intents["technical"]:
            desired_mix["Coding"] = 4
            desired_mix["Knowledge & Skills"] = desired_mix.get("Knowledge & Skills", 2)
        if intents["behavioral"]:
            desired_mix["Personality & Behavior"] = 3
        if intents["cognitive"]:
            desired_mix["Cognitive Ability"] = 3
        if intents["language"]:
            desired_mix["Language"] = 2
        if intents["domain"]:
            desired_mix["Domain-Specific"] = 2

        # Default mix if no signals found
        if not desired_mix:
            desired_mix = {"Coding": 3, "Personality & Behavior": 3,
                           "Cognitive Ability": 2, "Knowledge & Skills": 2}

        # Applying diversification strategy
        diversified = self._diversify(candidates, desired_mix, k=k)
        return diversified[["Name", "URL", "Category", "Score"]]
