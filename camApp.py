from flask import Flask, render_template, send_from_directory
from picamera import PiCamera
from datetime import datetime
import os
import time

app = Flask(__name__)
camera = PiCamera()
camera.resolution = (1024, 768)

# Create directory for images
IMAGE_DIR = 'static'
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

@app.route('/')
def index():
    # Capture image
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    image_name = f'fridge_{timestamp}.jpg'
    image_path = os.path.join(IMAGE_DIR, image_name)

    # Take the photo
    camera.start_preview()
    time.sleep(2)  # Let camera adjust
    camera.capture(image_path)
    camera.stop_preview()

    return render_template('index.html', image_file=image_name)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
