import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from detect import detect_objects
from nlp.keywords import extract_keywords
import json
import re  # For price extraction


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

upload_folder = app.config['UPLOAD_FOLDER']
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# Allowed file type check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return jsonify({"error": "No image part"}), 400
    image = request.files['image']
    caption = request.form['caption']
    
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if image and allowed_file(image.filename):
        # Secure the filename and save the image
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        # Process the image and caption
        detected_objects = detect_objects(image_path)  # Assuming this returns a list of detected objects
        keywords = extract_keywords(caption)  # Assuming this returns a list of keywords

        # Generate the product listing
        product_listing = generate_product_listing(detected_objects, keywords, caption, image_path)
        
        # Return the result to the front-end
        return render_template('index.html', result=product_listing)



def generate_product_listing(detected_objects, keywords, caption, image_path):
    # Extract the price from caption
    price_match = re.search(r"₹\s?(\d+)", caption)
    price = f"Rs {price_match.group(1)}" if price_match else "Price not available"

    # Remove irrelevant words from the keywords list
    irrelevant_words = {"price", "rs", "₹", "starts", "at", "whose", "is", "and"}
    features = [kw.lower() for kw in keywords if kw.lower() not in irrelevant_words]

    # Set the product name and description
    product_name = f"{detected_objects[0].capitalize()} Product" if detected_objects else "Unknown Product"
    description = f"{product_name} available on Amazon"

    # Generate the product listing
    product_listing = {
        "product_name": product_name,
        "category": "Sample Category",
        "price": price,
        "description": description,
        "features": features,
        "image": image_path
    }

    return product_listing  # Return the product listing as a dictionary


if __name__ == '__main__':
    app.run(debug=True)
