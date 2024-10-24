from flask import Flask, request, jsonify
import os
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
import numpy as np


import cv2 
from flask_cors import CORS
from dotenv import load_dotenv
import time
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# Load the .env file where your API key is stored
load_dotenv()

# Load EfficientNet model
model = EfficientNetB0(weights='imagenet')

def process_image(file_path):
    try:
        # Load and preprocess the image
        img = image.load_img(file_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # Predict the image's class
        predictions = model.predict(img_array)
        decoded_predictions = decode_predictions(predictions, top=3)[0]

        # Extract the most probable class label
        top_label = decoded_predictions[0][1]  # ImageNet label

        # Custom mapping of ImageNet label to muscle group
        muscle_group = imagenet_to_muscle_group.get(top_label, "unknown")

        return muscle_group, file_path
    except Exception as e:
        return None, None, str(e)


# Load the Hugging Face model pipeline for text generation
generator = pipeline('text-generation', model='gpt2')  # You can choose a different model if needed

# Function to generate dynamic workout using Hugging Face
def generate_workout(muscle_group):
    prompt = f"Suggest a workout routine for the {muscle_group} muscle group. Provide three exercises suitable for beginners, intermediates, and advanced levels."

    # Generate text using the Hugging Face model
    output = generator(prompt, max_length=100, num_return_sequences=1, temperature=0.7)

    # Parse the response
    workout_suggestions = output[0]['generated_text'].strip()
    return workout_suggestions

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Gym Workout API!"

# Function to limit requests (implementation as needed)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Implement your rate limiting logic here

    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    # Log the file upload
    print(f"Received file: {file.filename}")

    upload_folder = 'uploads/'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    print(f"File saved to: {file_path}")

    # Process the image and get the muscle group
    muscle_group = process_image(file_path)

    # Generate dynamic workout suggestions using GPT
    workout_suggestions = generate_workout(muscle_group)

    return jsonify({
        "file_path": file_path,
        "message": "File uploaded and processed successfully!",
        "muscle_group": muscle_group,
        "suggestions": workout_suggestions
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)
