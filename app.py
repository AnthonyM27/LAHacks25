
from flask import Flask, render_template, redirect, url_for, request, session, flash
import re
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from finalAI.fetchCoverLetter import FetchBairAgent
from finalAI.fetchRelevantLabs import FetchLabsAgent
from finalAI.fetchLabDetails import FetchLabDetailsAgent
from pdfCreator import PDFGenerator
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from finalAI.fetchCoverLetter import FetchBairAgent
from finalAI.fetchRelevantLabs import FetchLabsAgent
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from pdfCreator import PDFGenerator
from bs4 import BeautifulSoup
from io import BytesIO
import requests
import time
import re
import os


app = Flask(__name__)
app.secret_key = 'LAHACKS2025'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Store applications in memory for now (later use a database)
applications = []



# Landing Page -> Option for Register/Login
@app.route('/')
def landing():
    return render_template('landing.html')


# Login Page -> Prompt user for email, password
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        session['user'] = email
        return redirect(url_for('home'))
    
    return render_template('login.html')


# Register Page -> prompts user for email password, confirmation. 
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


# Dashboard -> Application tracker, how-to videos, get help with writing a cover letter
@app.route('/home', methods=['GET', 'POST'])
def home():

    if 'weekly_goal' not in session:
        session['weekly_goal'] = 5  # Default goal

    if 'applications_submitted' not in session:
        session['applications_submitted'] = 0

    if 'last_reset' not in session:
        session['last_reset'] = datetime.now().isoformat()

    if request.method == 'POST':
        if 'set_goal' in request.form:
            goal = request.form.get('weekly_goal')
            if goal and goal.isdigit():
                session['weekly_goal'] = int(goal)
                session['applications_submitted'] = 0  # reset on new goal set
                flash('Goal updated successfully!', 'success')

            else:
                flash('Please enter a valid number.', 'error')

        if 'log_application' in request.form:
            session['applications_submitted'] += 1

    progress = 0
    if session['weekly_goal'] > 0:
        progress = int((session['applications_submitted'] / session['weekly_goal']) * 100)

    # Motivational messages
    if progress == 0:
        motivation = "Let's get started!"
    elif progress < 50:
        motivation = "Keep going, you got this!"
    elif progress < 100:
        motivation = "Almost there!"
    else:
        motivation = "Amazing work! Goal reached!"

    return render_template('home.html', progress=progress, motivation=motivation)


# Prompts user for research position, lab, and relevant experience to generate a cover letter
@app.route('/cover_letter', methods=['GET', 'POST'])
def cover_letter():
    cover_letter = None

    if request.method == 'POST':
        position = request.form['position']
        lab = request.form['lab']
        experiences = request.form['experiences']
        agent = FetchBairAgent()
        cover_letter = agent.run_once(position_title=position, lab_name=lab, past_experiences=experiences)

    return render_template('cover_letter.html', cover_letter=cover_letter)


# Generates a downloadable pdf cover letter based on /cover_letter inputs
@app.route('/download_cover_letter', methods=['POST'])
def download_cover_letter():
    content = request.form['cover_letter_content']
    buffer = BytesIO()
    print(content)
    doc = SimpleDocTemplate(buffer,pagesize=letter,rightMargin=72,leftMargin=72,topMargin=72,bottomMargin=18)
    Story=[]

    # Create a PDF in memory
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 10)
    styles=getSampleStyleSheet()

    for line in content.split('\n'):
        Story.append(Paragraph(line, styles["Normal"]))
        Story.append(Paragraph("\xa0", styles["Normal"]))
    doc.build(Story)
    margin = 10

    # Define a function to wrap the text
    text_object = c.beginText(margin, height - margin)
    text_object.setFont("Helvetica", 10)
    text_object.setTextOrigin(margin, height - margin)

    # Wrap text to fit within the page width
    text_object.textLines(content)

    # Add the text to the canvas
    c.drawText(text_object)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='cover_letter.pdf', mimetype='application/pdf')



# General list of open lab positions
@app.route('/find_positions', methods=['GET'])
def find_positions():
    search_query = request.args.get('search_query', '').lower()

    # Example static list for now
    all_positions = [
        {'title': 'Research Assistant - AI and Robotics', 'lab': 'Berkeley AI Research Lab', 'link': 'https://example.com/ai-lab'},
        {'title': 'Climate Data Analyst Intern', 'lab': 'Berkeley Climate Lab', 'link': 'https://example.com/climate-lab'},
        {'title': 'Legal Research Fellow', 'lab': 'Berkeley Center for Law and Business', 'link': 'https://example.com/law-lab'},
        {'title': 'Machine Learning Researcher', 'lab': 'BAIR (Berkeley Artificial Intelligence Research)', 'link': 'https://example.com/bair'},
    ]

    if search_query:
        positions = [pos for pos in all_positions if search_query in pos['title'].lower()]
    else:
        positions = all_positions

    return render_template('find_positions.html', positions=positions)



# Route for find_research_groups page
@app.route('/find_research_groups', methods=['GET', 'POST'])
def find_research_groups():
    labs = []

    if request.method == 'POST':
        topic = request.form['topic']
        # Get the relevant labs based on the topic of interest
        agent = FetchLabsAgent()
        labs = agent.run_once(topic=topic)

    return render_template('find_research_groups.html', labs=labs)


# Route for application_tracker page
@app.route('/application_tracker', methods=['GET'])
def application_tracker():
    return render_template('application_tracker.html', applications=applications)


# Add a new application entry to application_tracker
@app.route('/add_application', methods=['POST'])
def add_application():
    applied = request.form.get('applied')
    status = request.form.get('status')
    date = request.form.get('date')
    position = request.form.get('position')
    lab = request.form.get('lab')

    new_application = {
        'applied': applied,
        'status': status,
        'date': date,
        'position': position,
        'lab': lab
    }
    applications.append(new_application)

    return redirect(url_for('application_tracker'))


# Update the application_tracker status entry
@app.route('/update_status', methods=['POST'])
def update_status():
    index = int(request.form.get('index'))
    new_status = request.form.get('status')

    if 0 <= index < len(applications):
        applications[index]['status'] = new_status

    return redirect(url_for('application_tracker'))


# Sign out of your account, redirect to login. 
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been signed out.', 'info')
    return redirect(url_for('login'))



# Route for profile page. 
@app.route('/profile', methods=['GET', 'POST'])
def profile():

    if not 'user' in session:
        return redirect(url_for('login'))
    
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user'])
    os.makedirs(user_folder, exist_ok=True)
    uploaded_files = []

    if os.path.exists(user_folder):
        uploaded_files = os.listdir(user_folder)

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        url = request.form.get('url')

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



# Helper to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to scrape labs based on the topic of interest
def scrape_labs_by_topic(topic):
    base_url = 'https://vcresearch.berkeley.edu'
    url = base_url + '/research-units/centers-and-institutes-by-subject-area'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all the labs in the 'main-content' section
    labs = soup.find('div', {'class': 'main-content'})
    lab_links = labs.find_all('a', href=True)
    filtered_labs = []

    for lab in lab_links:
        lab_name = lab.text.strip()
        lab_url = lab['href']

        # If the URL is relative, prepend the base URL
        if not lab_url.startswith('http'):
            lab_url = base_url + lab_url

        # Check if the topic is present in the lab name (case-insensitive)
        if re.search(topic, lab_name, re.IGNORECASE):
            filtered_labs.append({'name': lab_name, 'url': lab_url})

    return filtered_labs


if __name__ == '__main__':
    app.run(debug=True)