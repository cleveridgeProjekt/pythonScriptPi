from flask import Flask, render_template, redirect, url_for
import cv2
import os
from datetime import datetime

app = Flask(__name__)
IMAGE_DIR = 'static'

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def take_photo():
    cam = cv2.VideoCapture(0)  # 0 = default USB camera
    if not cam.isOpened():
        raise RuntimeError("Cannot open camera")

    ret, frame = cam.read()
    cam.release()

    if not ret:
        raise RuntimeError("Failed to grab frame")

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f'fridge_{timestamp}.jpg'
    path = os.path.join(IMAGE_DIR, filename)

    cv2.imwrite(path, frame)
    return filename

@app.route('/')
def index():
    image_files = sorted(os.listdir(IMAGE_DIR), reverse=True)
    latest_image = image_files[0] if image_files else None
    return render_template('index.html', image_file=latest_image)

@app.route('/take-photo', methods=['POST'])
def capture():
    image_name = take_photo()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
