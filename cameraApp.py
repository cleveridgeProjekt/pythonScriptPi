from flask import Flask, request, jsonify
import cv2
import time
import os

app = Flask(__name__)

@app.route('/capture', methods=['POST'])
def capture():
    try:
        # Initialize USB camera (usually device 0, adjust if needed)
        cam = cv2.VideoCapture(0)

        if not cam.isOpened():
            return jsonify({'status': 'error', 'message': 'Camera not accessible'}), 500

        # Allow camera to warm up
        time.sleep(1)

        # Capture frame
        ret, frame = cam.read()
        cam.release()

        if not ret:
            return jsonify({'status': 'error', 'message': 'Failed to capture image'}), 500

        # Save the image
        timestamp = int(time.time())
        filename = f"photo_{timestamp}.jpg"
        cv2.imwrite(filename, frame)

        return jsonify({'status': 'success', 'filename': filename})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Run Flask app on all interfaces (port 5000)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
