import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from keras.models import load_model
from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
import json

# Initialize Flask app
app = Flask(__name__)

# Load the model
model = load_model(r'D:/CROP DISEASE DETECTION/NEW TRAINED/wheat new train/model.h5')  # Ensure model.h5 is in the same directory
print('Model loaded. Check http://127.0.0.1:5003/')  # Update this port for potato app

# Define label mapping
labels = {0: 'Brown Rust', 1: 'Healthy', 2: 'Yellow Rust'}

# Set the path to the disease_info.json file
json_path = os.path.join(os.getcwd(), 'wheat new train', 'disease_info.json')

# Load disease information from the JSON file
with open(json_path, 'r') as file:
    disease_info = json.load(file)
    print(disease_info)  # To verify that the JSON file is loaded correctly
# Define upload folder in the same directory as app.py
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Function to predict image result
def getResult(image):
    x = img_to_array(image)  # Convert image to array
    x = x.astype('float32') / 255.  # Normalize
    x = np.expand_dims(x, axis=0)  # Add batch dimension
    predictions = model.predict(x)[0]  # Get predictions
    predicted_label = labels[np.argmax(predictions)]  # Get label
    confidence = round(100 * np.max(predictions), 2)  # Confidence score
    
    # Ensure confidence is at most 99.99%
    confidence = min(confidence, 99.99)
    
    return predicted_label, confidence

# Homepage route
@app.route('/')
def index():
    return render_template("index.html")

# Prediction route
@app.route('/predict', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No image uploaded", 400

    f = request.files['file']
    if f.filename == '':
        return "No file selected", 400

    filename = secure_filename(f.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(image_path)

    # Open and process image
    image = Image.open(image_path).convert("RGB")
    image = image.resize((225, 225))

    # Get prediction
    predicted_label, confidence = getResult(image)

    # Generate correct image path for display
    image_display_url = f'/uploads/{filename}'

      # Retrieve additional information for the predicted disease
    # Check if disease info exists for predicted label
    disease_details = disease_info.get(predicted_label, None)

    # If disease details are not found, return a message
    if not disease_details:
        disease_details = {
            "meaning": "No details available",
            "causes": "No details available",
            "symptoms": "No details available",
            "remedy": "No details available"
        }

    return render_template("index.html", 
                           image_path=image_display_url, 
                           predicted_label=predicted_label, 
                           confidence=confidence,
                           disease_details=disease_details)

# Serve uploaded files
from flask import send_from_directory
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Run app
if __name__ == '__main__':
    app.run(debug=True, port=5003)  # Specify the port (5001) for the potato app

