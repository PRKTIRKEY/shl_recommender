# required libraries
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from cleaner import validate_and_clean   # custom function to clean dataset

def main():
    # Step 1: Clean the raw dataset before building the index
    # validate_and_clean takes the raw CSV and outputs a cleaned version
    clean_path = validate_and_clean("shl_assessments.csv", "shl_assessments_clean.csv")
    
    # Load the cleaned dataset into a DataFrame
    df = pd.read_csv(clean_path)

    # Step 2: Load a pre-trained sentence transformer model
    # "all-MiniLM-L6-v2" is a lightweight model for generating embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Step 3: Prepare text inputs for embedding
    # Concatenate Name, Category and Description fields for each assessment
    texts = (df["Name"] + " " + df["Category"] + " " + df["Description"]).tolist()

    print("Encoding assessments...")

    # Step 4: Generate embeddings for all assessments
    # convert_to_numpy=True → returns NumPy array
    # show_progress_bar=True → displays progress bar during encoding
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    # Step 5: Normalize embeddings to unit length (L2 norm)
    # This ensures cosine similarity can be computed via inner product
    faiss.normalize_L2(embeddings)

    # Step 6: Build FAISS index
    dim = embeddings.shape[1]               # dimensionality of embeddings
    index = faiss.IndexFlatIP(dim)          # Index using Inner Product (cosine similarity after normalization)
    index.add(embeddings)                   # Adding all embeddings to the index

    # Step 7: Save the index and embeddings for later use
    faiss.write_index(index, "assessments.index")   # saves FAISS index to file
    np.save("embeddings.npy", embeddings)           # saves embeddings as NumPy array

    print("Index built using cleaned catalog.")

# Entry point: runs main() if script is executed directly
if __name__ == "__main__":
    main()
