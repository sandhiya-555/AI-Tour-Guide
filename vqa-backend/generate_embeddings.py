import os
import torch
from PIL import Image
from torchvision import transforms
from transformers import CLIPProcessor, CLIPModel
import pickle

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")

# Path to dataset
DATASET_DIR = "./dataset"

# Image preprocessing
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.4815, 0.4578, 0.4082), std=(0.2686, 0.2613, 0.2758)),
])

# Dictionary to hold embeddings
embeddings = {}

# Iterate through each landmark folder
for landmark in os.listdir(DATASET_DIR):
    landmark_dir = os.path.join(DATASET_DIR, landmark)
    if not os.path.isdir(landmark_dir):
        continue

    embeddings[landmark] = []

    for img_name in os.listdir(landmark_dir):
        img_path = os.path.join(landmark_dir, img_name)
        image = Image.open(img_path).convert("RGB")

        # Process and encode
        inputs = processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
            image_features /= image_features.norm(p=2, dim=-1, keepdim=True)  # Normalize

        embeddings[landmark].append(image_features.cpu().squeeze().numpy())

# Save to disk
with open("landmark_embeddings.pkl", "wb") as f:
    pickle.dump(embeddings, f)

print("✅ Embeddings saved to landmark_embeddings.pkl")
