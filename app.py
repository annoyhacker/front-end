from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import logging

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)

def send_aceplus_welcome(parent_name, mobile, email):
    try:
        # Render HTML template with dynamic content
        html_content = render_template(
            'aceplus_email.html',
            parent_name=parent_name,
            mobile=mobile,
            email=email
        )

        # Configure email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Welcome to ACEplus"
        msg['From'] = os.getenv('GMAIL_USER')
        msg['To'] = email

        msg.attach(MIMEText(html_content, 'html'))

        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(os.getenv('GMAIL_USER'), os.getenv('GMAIL_PASSWORD'))
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        
        logging.info(f"ACEplus welcome email sent to {email}")
        return True

    except Exception as e:
        logging.error(f"Email sending error: {str(e)}")
        return False

@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    parent_name = data.get('name')
    mobile = data.get('mobile')
    email = data.get('email')
    
    if send_aceplus_welcome(parent_name, mobile, email):
        return jsonify({
            'status': 'success',
            'message': 'Registration successful! Check your email.'
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Failed to send welcome email'
        }), 500

@app.route('/')
def home():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(  port=5000, host ='0.0.0.0' , debug=True)