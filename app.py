
from flask import Flask, render_template, redirect, url_for, request, session, flash
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'LAHACKS2025'

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        session['user'] = email
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        email_regex = r'^\S+@\S+\.\S+$'
        if not re.match(email_regex, email):
            flash('Invalid email address.', 'error')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('register'))

        session['user'] = email
        session['profile_complete'] = False

        return redirect(url_for('profile'))

    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/find-positions')
def find_positions():
    return render_template('find-positions.html')

@app.route('/application-tracker')
def application_tracker():
    return render_template('application-tracker.html')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user'])
    os.makedirs(user_folder, exist_ok=True)

    uploaded_files = []
    if os.path.exists(user_folder):
        uploaded_files = os.listdir(user_folder)

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')

        if full_name:  # Only update name if it's provided
            session['full_name'] = full_name

        # Save email and phone number to session or database if needed
        session['email'] = email
        session['phone_number'] = phone_number

        resume = request.files.get('resume')
        if resume and allowed_file(resume.filename):
            resume.save(os.path.join(user_folder, secure_filename('resume.pdf')))

        transcript = request.files.get('transcript')
        if transcript and allowed_file(transcript.filename):
            transcript.save(os.path.join(user_folder, secure_filename('transcript.pdf')))

        letters = request.files.getlist('letters')
        for idx, letter in enumerate(letters):
            if letter and allowed_file(letter.filename):
                letter.save(os.path.join(user_folder, secure_filename(f'letter_{idx+1}.pdf')))

        writing_samples = request.files.getlist('writing_samples')
        for idx, sample in enumerate(writing_samples):
            if sample and allowed_file(sample.filename):
                sample.save(os.path.join(user_folder, secure_filename(f'writing_sample_{idx+1}.pdf')))

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', uploaded_files=uploaded_files)




if __name__ == '__main__':
    app.run(debug=True)