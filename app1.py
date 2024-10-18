from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

# Load your pre-trained deepfake detection model
model = load_model('deepfake_cnn_model.h5')

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_video(file_path, fps_target=1):
    cap = cv2.VideoCapture(file_path)
    video_fps = int(cap.get(cv2.CAP_PROP_FPS))  # Get the frame rate of the video
    frame_interval = video_fps // fps_target  # Calculate how many frames to skip
    
    predictions = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frames at the target FPS rate
        if frame_count % frame_interval == 0:
            # Preprocess the frame
            frame = cv2.resize(frame, (128, 128))
            frame = frame.astype("float") / 255.0
            frame = img_to_array(frame)
            frame = np.expand_dims(frame, axis=0)
            
            # Get prediction
            prediction = model.predict(frame)
            predictions.append(prediction[0][0])
        
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    # Compute average prediction
    avg_prediction = np.mean(predictions)
    return avg_prediction

@app.route('/')
def index():
    return render_template('sih1.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['video']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the video and get the prediction
        avg_prediction = process_video(file_path)
        
        # Determine if it's a deepfake
        is_deepfake = avg_prediction > 0.5
        confidence_score = avg_prediction * 100

        # Define analysis details (example placeholders)
        if is_deepfake:
            analysis_details = [
                "Spatial Analysis: Anomalies detected in facial regions, suggesting manipulations.",
                "Temporal Analysis: Discrepancies found across frames, indicative of frame tampering.",
                "Audio-Visual Sync: Audio does not match lip movements at certain timestamps."
            ]
        else:
            analysis_details = [
                "Spatial Analysis: No anomalies detected in facial regions.",
                "Temporal Analysis: Frame sequences appear consistent.",
                "Audio-Visual Sync: Audio matches lip movements without discrepancies."
            ]
        
        return jsonify({
            'fakeStatus': "Yes" if is_deepfake else "No",
            'confidenceScore': f"{confidence_score:.2f}%",
            'analysisDetails': analysis_details
        })
    else:
        flash('File not allowed')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
