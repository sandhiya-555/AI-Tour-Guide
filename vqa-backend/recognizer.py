import torch
import pickle
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch.nn.functional as F

# Load model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")

# Load landmark embeddings
with open("landmark_embeddings.pkl", "rb") as f:
    landmark_embeddings = pickle.load(f)

# Preprocess and extract feature of uploaded image
def extract_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        features = model.get_image_features(**inputs)
        features = F.normalize(features, p=2, dim=-1)
    return features.cpu().squeeze().numpy()

# Compare against dataset embeddings
def get_closest_landmark(image_path):
    input_embedding = extract_embedding(image_path)

    best_match = None
    best_score = -1

    for landmark, embeddings_list in landmark_embeddings.items():
        for emb in embeddings_list:
            sim = np.dot(input_embedding, emb)  # cosine similarity
            if sim > best_score:
                best_score = sim
                best_match = landmark

    return best_match
