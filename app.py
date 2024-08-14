from flask import Flask, render_template, request, redirect, url_for, Response
import cv2
import os
import threading
from modules.processors.frame.face_swapper import process_frame
from modules.face_analyser import get_one_face

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Global variables
uploaded_face_path = None
recording = False
out = None  # Video writer object

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_face', methods=['POST'])
def upload_face():
    global uploaded_face_path
    if 'face' not in request.files:
        return redirect(request.url)
    file = request.files['face']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        uploaded_face_path = file_path
    return redirect(url_for('index'))

@app.route('/live')
def live():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/record/start', methods=['POST'])
def start_record():
    global recording, out
    recording = True
    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'X264'), 20.0, (640, 480))
    return '', 204  # No content response

@app.route('/record/stop', methods=['POST'])
def stop_record():
    global recording, out
    recording = False
    if out:
        out.release()
    return '', 204  # No content response

def generate_frames():
    global uploaded_face_path, recording, out
    if uploaded_face_path is None:
        print("No face image uploaded.")
        return

    cap = cv2.VideoCapture(0)  # Open the webcam
    if not cap.isOpened():
        print("Could not open webcam.")
        return

    source_face = get_one_face(cv2.imread(uploaded_face_path))
    if source_face is None:
        print("No face detected in the uploaded image.")
        return

    print("Starting live stream...")
    
    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to capture frame from webcam.")
            break

        # Process the frame with the selected face
        processed_frame = process_frame(source_face, frame)

        if recording and out:
            out.write(processed_frame)  # Write frame to video file

        ret, buffer = cv2.imencode('.jpg', processed_frame)
        if not ret:
            print("Failed to encode frame.")
            break
        
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    if recording and out:
        out.release()
    print("Live stream ended.")

if __name__ == '__main__':
    app.run(debug=True)
