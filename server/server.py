import flask
import io
import string
import time
import os
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, jsonify, request
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

model = ResNet50(weights='imagenet')


def prepare_image(img):
    img = Image.open(io.BytesIO(img))
    img = img.resize((224, 224))
    img = np.array(img)
    img = np.expand_dims(img, 0)
    img = preprocess_input(img)
    return img

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def infer_image():
    if 'file' not in request.files:
        return jsonify(Error="Please try again. The Image doesn't exist")
    
    file = request.files.get('file')

    if not file:
        return jsonify(Error="Not file")

    img_bytes = file.read()
    img = prepare_image(img_bytes)
    preds = model.predict(img)

    raw_pred = decode_predictions(preds, top=3)[0]
    object_names = []
    for i in raw_pred:
        object_names.append(i[1])
    print('Predicted:', object_names)
    return jsonify(prediction=','.join(object_names))
    

@app.route('/', methods=['GET'])
def index():
    return 'Machine Learning Inference'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')