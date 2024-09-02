from flask import Flask, render_template, request, redirect, url_for, session
import cv2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Teacher credentials
teachers = {
    '1234': '1234',
    'teacher2': 'mypassword',
    'teacher3': 'adminpass'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        teacher_id = request.form['teacher_id']
        password = request.form['password']
        if teacher_id in teachers and teachers[teacher_id] == password:
            session['teacher_id'] = teacher_id  # Store teacher ID in session
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid ID or password')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'teacher_id' not in session:
        return redirect(url_for('login'))

    # Load the webcam.py script here
    # Example: You can put your webcam attendance code here
    video_capture = cv2.VideoCapture(0)
    # Process video, capture attendance, etc.

    return render_template('dashboard.html', teacher_id=session['teacher_id'])

@app.route('/logout')
def logout():
    session.pop('teacher_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)