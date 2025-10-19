from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import os
import re
import ast
from dotenv import load_dotenv

# --- AI Model Imports ---
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# --- Load Environment Variables ---
load_dotenv(dotenv_path="../.env") 

pinecone_api_key = os.getenv("PINECONE_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

# --- Initialize AI Clients (Global) ---
print("Loading AI models and connecting to services...")

pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("product-recommendations")
print("Pinecone client initialized.")

embed_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Text embedding model loaded.")

genai.configure(api_key=google_api_key)
genai_model = genai.GenerativeModel('gemini-2.5-flash')
print("Generative AI model loaded.")

try:
    products_df = pd.read_pickle("../products_df.pkl")
    products_df = products_df.set_index('uniq_id')
    print("Product DataFrame loaded.")
except FileNotFoundError:
    print("ERROR: products_df.pkl not found. Make sure it's in the root folder.")
    products_df = None

print("--- AI Models and Data Loaded. Server is ready. ---")

# --- Helper Functions ---

def clean_price(price):
    """
    Converts a price string (e.g., '$24.99') or NaN to a float.
    """
    if pd.isna(price):
        return 0.0
    if isinstance(price, (int, float)):
        return float(price)
    if isinstance(price, str):
        price_str = re.sub(r"[^0-9.]", "", price)
        if price_str:
            return float(price_str)
    return 0.0

def get_first_image_url(image_str):
    """Cleans the 'images' column string and gets the first URL."""
    try:
        image_list = ast.literal_eval(image_str)
        if image_list and isinstance(image_list, list) and len(image_list) > 0:
            return image_list[0]
    except Exception:
        pass
    return "https://example.com/default-image.jpg" # A default image

# --- REAL AI Functions ---

def get_semantic_recommendations(query: str, top_k: int = 5):
    """Gets recommendations from Pinecone based on a text query."""
    try:
        query_embedding = embed_model.encode(query).tolist()
        query_results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=False
        )
        result_ids = [match['id'] for match in query_results['matches']]
        recommended_products = products_df.loc[result_ids]
        
        recommended_products['uniq_id'] = recommended_products.index
        
        return recommended_products.to_dict('records')
    except Exception as e:
        print(f"Pinecone query error: {e}")
        return []

def generate_description_direct(title: str):
    """Generates a creative description using the Gemini API."""
    try:
        prompt = f"""You are a creative marketing assistant.
        Write a short, appealing product description (max 2 sentences) for: {title}"""
        response = genai_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"GenAI error: {e}")
        return f"This is a fantastic, high-quality {title}. It's the perfect addition to any modern home!"

# --- FastAPI App Initialization ---

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---

class RecommendationQuery(BaseModel):
    query: str

class Product(BaseModel):
    id: str
    title: str
    image: str
    price: float
    description: str

class RecommendationResponse(BaseModel):
    products: list[Product]

class AnalyticsData(BaseModel):
    message: str
    
# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Product Recommendation API! (Real Models Loaded)"}

@app.post("/recommend", response_model=RecommendationResponse)
def recommend_products(query: RecommendationQuery):
    """
    The main recommendation endpoint (NOW WITH REAL AI)
    """
    if products_df is None:
        raise HTTPException(status_code=500, detail="Server error: Product data not loaded.")
        
    try:
        recommended_products = get_semantic_recommendations(query.query)
        
        products_list = []
        for item in recommended_products:
            
            creative_desc = generate_description_direct(item["title"])
            
            product = Product(
                id=item["uniq_id"],
                title=item["title"],
                image=get_first_image_url(item["images"]),
                price=clean_price(item["price"]),
                description=creative_desc
            )
            products_list.append(product)
            
        return RecommendationResponse(products=products_list)
    
    except Exception as e:
        print(f"Server Error in /recommend: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/analytics", response_model=AnalyticsData)
def get_analytics():
    """Endpoint to serve analytics data."""
    return AnalyticsData(message="Analytics data will go here.")