from flask import Flask, render_template, redirect, url_for
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2
import os

app = Flask(__name__)

# Load Food101 classification model from TensorFlow Hub
model = hub.load("https://tfhub.dev/google/food101/mobilenet_v2_100_224/classification/1")
input_size = (224, 224)

# Load class labels
with open("food_labels.txt", "r") as f:
    food_labels = [line.strip() for line in f.readlines()]

latest_prediction = {}

def take_photo_and_classify():
    global latest_prediction

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        latest_prediction = {"label": "Camera Error", "confidence": 0.0}
        return

    # Save captured image
    filepath = "static/latest.jpg"
    cv2.imwrite(filepath, frame)

    # Resize & normalize image
    img = cv2.resize(frame, input_size)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
