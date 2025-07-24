from flask import Flask, render_template, redirect, url_for
import cv2
import tensorflow as tf
import numpy as np
from datetime import datetime
import os

app = Flask(__name__)

# Load pre-trained model (MobileNetV2)
model = tf.keras.applications.MobileNetV2(weights='imagenet')
decode_predictions = tf.keras.applications.mobilenet_v2.decode_predictions
input_size = (224, 224)

result_label = ""

def take_and_classify_photo():
    global result_label

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        # Save photo
        filepath = "static/latest.jpg"
        cv2.imwrite(filepath, frame)

        # Preprocess for model
        img = cv2.resize(frame, input_size)
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

        # Predict
        predictions = model.predict(img_array)
        decoded = decode_predictions(predictions, top=1)[0][0]
        result_label = f"{decoded[1]} ({decoded[2]*100:.2f}%)"
    else:
        result_label = "Camera Error"
    cap.release()

@app.route('/')
def index():
    return render_template('index.html', result=result_label)

@app.route('/snap', methods=['POST'])
def snap():
    take_and_classify_photo()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
