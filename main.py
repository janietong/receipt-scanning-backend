from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from ocr import getresponse
from openai import OpenAI
import os
import base64

client = OpenAI(
    api_key = os.environ["OPENAI_API_KEY"],
)

image_path = "moose.jpg"

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

image = encode_image(image_path)

app = Flask(__name__)
cors = CORS(app)

@cross_origin()
@app.route('/')
def home():
    return jsonify(message="Hello, World!")

@cross_origin()
@app.route('/api/getresponse')
def get_data():
    response = getresponse(image, client)
    return jsonify(data=response)

@cross_origin()
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file.save(file.filename)
        response = getresponse(image, client)
        return jsonify({'message': response, 'filename': file.filename}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)