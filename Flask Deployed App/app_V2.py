import os
import logging
from flask import Flask, request, jsonify, send_from_directory, render_template, redirect
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import secure_filename
from deep_translator import GoogleTranslator
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd

# === CONFIGURATION ===
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024

# === SETUP ===
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# === LOAD MODEL & DATA ===
disease_info = pd.read_csv('disease_info.csv' , encoding='cp1252')
supplement_info = pd.read_csv('supplement_info.csv',encoding='cp1252')

model = CNN.CNN(39)
model.load_state_dict(torch.load("plant_disease_model_1_latest.pt"))
model.eval()

# === SWAGGER UI ===
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "DocFarm API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# === HELPERS ===
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prediction(image_path):
    image = Image.open(image_path).resize((224, 224))
    input_data = TF.to_tensor(image).view((-1, 3, 224, 224))
    output = model(input_data).detach().numpy()
    index = np.argmax(output)
    return index

def translate_text(text):
    try:
        return GoogleTranslator(source='auto', target='fr').translate(text)
    except Exception as e:
        print("Erreur de traduction :", e)
        return text


# === ROUTES: API ===
@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        logging.warning("No file part in request")
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        logging.warning("No selected file")
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        logging.warning(f"File type not allowed: {file.filename}")
        return jsonify({"error": "File type not allowed"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    pred = prediction(file_path)
    title = translate_text(disease_info['disease_name'][pred])
    description = translate_text(disease_info['description'][pred])
    prevent = translate_text(disease_info['Possible Steps'][pred])
    supplement_name = translate_text(supplement_info['supplement name'][pred])
    supplement_buy_link = supplement_info['buy link'][pred]

    try:
        return jsonify({
            "title": title,
            "description": description,
            "prevention": prevent,
            "supplement_name": supplement_name,
            "supplement_buy_link": supplement_buy_link
        }), 200
    except Exception as e:
        logging.error(f"Error saving file: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# === ROUTES: Web App ===
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/index')
def ai_engine_page():
    return render_template('index.html')

@app.route('/mobile-device')
def mobile_device_detected_page():
    return render_template('mobile-device.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        image = request.files['image']
        filename = secure_filename(image.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(file_path)

        pred = prediction(file_path)
        title = disease_info['disease_name'][pred]
        description = disease_info['description'][pred]
        prevent = disease_info['Possible Steps'][pred]
        image_url = disease_info['image_url'][pred]
        supplement_name = supplement_info['supplement name'][pred]
        supplement_image_url = supplement_info['supplement image'][pred]
        supplement_buy_link = supplement_info['buy link'][pred]

        return render_template('submit.html', title=title, desc=description, prevent=prevent,
                               image_url=image_url, pred=pred,
                               sname=supplement_name, simage=supplement_image_url,
                               buy_link=supplement_buy_link)

@app.route('/market', methods=['GET', 'POST'])
def market():
    return render_template('market.html',
                           supplement_image=list(supplement_info['supplement image']),
                           supplement_name=list(supplement_info['supplement name']),
                           disease=list(disease_info['disease_name']),
                           buy=list(supplement_info['buy link']))

# === MAIN ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
