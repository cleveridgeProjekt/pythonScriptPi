from flask import Flask, request, jsonify
import cv2
import time
import requests

app = Flask(__name__)

# Laravel endpoint to receive the image
LARAVEL_UPLOAD_URL = 'https://your-laravel-app.com/api/upload-photo'  # <-- update this

@app.route('/capture', methods=['POST'])
def capture():
    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            return jsonify({'status': 'error', 'message': 'Camera not accessible'}), 500

        time.sleep(1)
        ret, frame = cam.read()
        cam.release()

        if not ret:
            return jsonify({'status': 'error', 'message': 'Failed to capture image'}), 500

        filename = f"/tmp/photo_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)

        with open(filename, 'rb') as img_file:
            files = {'photo': img_file}
            response = requests.post(LARAVEL_UPLOAD_URL, files=files)

        return response.json(), response.status_code

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
