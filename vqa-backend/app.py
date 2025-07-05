from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import BlipProcessor, BlipForQuestionAnswering
from PIL import Image
import torch
import requests
import os

# 🧠 Landmark recognizer logic
from recognizer import get_closest_landmark

# 🔍 Vague terms that need override
vague_terms = {
    "tower", "temple", "statue", "building", "structure",
    "monument", "skyscraper", "bridge", "mosque", "church"
}

# 📚 Map from folder names to proper Wikipedia-compatible names
LANDMARK_NAME_MAP = {
    "borobudur": "Borobudur",
    "eiffel tower": "Eiffel Tower",
    "giza": "Great Pyramid of Giza",
    "liberty": "Statue of Liberty",
    "stonehenge": "Stonehenge",
    "sydney": "Sydney Opera House",
    "tajmahal": "Taj Mahal",
    "thanjavur": "Brihadeeswarar Temple",
    "the colosseum": "Colosseum",
    "velankanni": "Basilica of Our Lady of Good Health"
}

# 🌐 Wikipedia cultural fact fetcher
def get_fact_from_wikipedia(place):
    try:
        formatted = place.strip().replace(" ", "_")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "No fact found."), data["content_urls"]["desktop"]["page"]
        else:
            return "No Wikipedia summary found.", f"https://en.wikipedia.org/wiki/{formatted}"
    except Exception as e:
        print("Wikipedia Error:", e)
        return "No fact found.", f"https://en.wikipedia.org/wiki/{place.replace(' ', '_')}"

# 🚀 Flask app setup
app = Flask(__name__)
CORS(app)

# 🧠 Load BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 📸 VQA API endpoint
@app.route('/api/vqa', methods=['POST'])
def handle_vqa():
    try:
        if 'image' not in request.files or 'question' not in request.form:
            return jsonify({'error': 'Image or question missing'}), 400

        image_file = request.files['image']
        question = request.form['question']

        print(f"📥 Image: {image_file.filename}")
        print(f"❓ Question: {question}")

        # Save uploaded image temporarily
        os.makedirs("uploads", exist_ok=True)
        image_path = os.path.join("uploads", image_file.filename)
        image_file.save(image_path)

        # Run BLIP VQA
        image = Image.open(image_path).convert('RGB')
        inputs = processor(image, question, return_tensors="pt").to(device)

        with torch.no_grad():
            output = model.generate(**inputs)

        answer = processor.decode(output[0], skip_special_tokens=True).strip().lower()
        print(f"🔎 BLIP Answer: {answer}")

        # Override vague answer with CLIP-based recognition
        if answer in vague_terms:
            landmark_name = get_closest_landmark(image_path)
            print(f"⚠️ Vague answer '{answer}' overridden with: {landmark_name}")
            answer = LANDMARK_NAME_MAP.get(landmark_name.lower(), landmark_name.title())
        else:
            print("✅ Answer is specific enough")

        # Get fact and Wikipedia link
        fact, wiki_link = get_fact_from_wikipedia(answer)

        return jsonify({
            'answer': answer,
            'fact': fact,
            'link': wiki_link
        })

    except Exception as e:
        print("❌ Server Error:", e)
        return jsonify({'error': 'Failed to process image/question', 'details': str(e)}), 500

# 🏁 Start server
if __name__ == '__main__':
    app.run(debug=True)
