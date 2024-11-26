from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from ocr import getresponse
from openai import OpenAI
import os
import base64

client = OpenAI(
    api_key = os.environ["OPENAI_API_KEY"],
)

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

app = Flask(__name__)
cors = CORS(app)

@cross_origin()
@app.route('/')
def home():
    return jsonify(message="Hello, World!")

@cross_origin()
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    try:
        img_bytes = file.read()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        response = getresponse(img_base64, client)
        return jsonify({'message': response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)