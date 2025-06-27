# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
import base64

app = Flask(__name__)
CORS(app)

def extract_text_from_image(img_data):
    image = Image.open(io.BytesIO(img_data))
    text = pytesseract.image_to_string(image)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    content_type = file.content_type
    extracted_lines = []

    if 'pdf' in content_type:
        images = convert_from_bytes(file.read())
        for img in images:
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            lines = extract_text_from_image(buf.read())
            extracted_lines.extend(lines)
    else:
        extracted_lines = extract_text_from_image(file.read())

    return jsonify({'lines': extracted_lines})
