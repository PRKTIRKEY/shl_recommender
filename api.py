# FastAPI framework and Query helper
from fastapi import FastAPI, Query
# Pydantic BaseModel for request validation
from pydantic import BaseModel
# custom recommender class
from recommender import SHLRecommender
# utility functions for fetching and cleaning text
from utils import fetch_text_from_url, clean_text

# FastAPI application with a title
app = FastAPI(title="SHL Assessment Recommender API")

# recommender system
reco = SHLRecommender()

# request body schema using Pydantic
class RecommendationRequest(BaseModel):
    # Either raw text input
    text: str | None = None
    # Or a URL to fetch text from
    url: str | None = None
    # Number of recommendations requested (default 10)
    k: int = 10
    # Whether to diversify recommendations (default True)
    diversify: bool = True

# POST endpoint for recommendations
@app.post("/recommend")
def recommend(req: RecommendationRequest):
    # Case 1: If text is provided, clean it
    if req.text:
        query = clean_text(req.text)
    # Case 2: If URL is provided, fetch and clean text
    elif req.url:
        query = clean_text(fetch_text_from_url(req.url))
        # If extracted text is too short, return error
        if len(query) < 200:
            return {"error": "Could not extract sufficient text from URL."}
    # Case 3: Neither text nor URL provided → return error
    else:
        return {"error": "Provide either 'text' or 'url'."}

    # Clamp k between 1 and 10 to avoid invalid values
    k = max(1, min(10, req.k))

    # Call the recommender system with the query
    df = reco.recommend(query, k=k, diversify=req.diversify)

    # Format the response as JSON
    return {
        "count": len(df),  # number of recommendations
        "items": [
            {
                "name": row["Name"],       # recommended item name
                "url": row["URL"],         # link to item
                "category": row["Category"], # item category
                "score": float(row["Score"]) # relevance score
            }
            for _, row in df.iterrows()  # iterate over DataFrame rows
        ]
    }
