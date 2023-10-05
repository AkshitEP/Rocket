from flask import Flask, render_template, redirect, url_for, request
import cv2
import utils
import time
import numpy as np
import tensorflow as tf

app = Flask(__name__)

tabs = ['Dashboard', 'Launchpad', 'VibeCheck', 'Customize']
gaming_mode = "Off"
accent_color = "#ff0000"
model = tf.keras.models.load_model("finalest_model.h5")
score = 0
score_exists = False
games = ["Chess", "CyberPunk", "Far Cry", "GTA 5", "PUBG", "Rocket League", "Watch Dogs", "World War Z"]
game_paths = ["chess.com"]

@app.route('/')
def index():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', tabs = tabs, gaming_mode=gaming_mode, clr = accent_color)

@app.route('/launchpad')
def launchpad():
    return render_template('launchpad.html', paths = game_paths, n = len(games), tabs = tabs, games=games, clr = accent_color, filepaths=[url_for('static', filename=f'thumbnails/{game}.jpg') for game in games])

@app.route('/vibecheck')
def vibecheck():
    return render_template('vibecheck.html', tabs = tabs, clr = accent_color, score = score, score_exists = score_exists)

@app.route('/customize')
def customize():
    print(accent_color)
    return render_template('customize.html', tabs = tabs, clr = accent_color)


@app.route('/dnd', methods=['POST'])
def dnd():
    global gaming_mode

    if gaming_mode == 'Off':
        gaming_mode = 'On'
        utils.disable_windows_notifications()
    else:
        gaming_mode = 'Off'
        utils.enable_windows_notifications()
    
    return redirect('/dashboard')


@app.route('/setaccent', methods=['POST'])
def set_accent():
    global accent_color
    accent_color = request.form['color']
    return redirect('/customize')


@app.route('/ml', methods=['POST'])
def ml():
    global score, score_exists

    duration = int(request.form['vibe-time'])
    init_time = time.time()
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    frames = 0
    val = 0

    while time.time() - init_time < duration:
        ret, frame = cap.read()
        frames += 1
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))

        for (x, y, w, h) in faces:
            roi = frame[y:y+h, x:x+w]
            roi = cv2.resize(roi, (80, 80))
            roi = roi.reshape((1, 80, 80, 1))

            predictions = model.predict(roi)
            expr = np.argmax(predictions)
            weights = [0, 0.1, 0.5, 1]

            val += weights[expr]

            break
    
    cap.release()
    
    score = int(100 * val / frames)
    score_exists = True

    return redirect('/vibecheck')




if __name__ == "__main__":
    app.run()
