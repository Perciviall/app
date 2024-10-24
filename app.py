from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

app.secret_key = os.urandom(24)  # Set a secret key for session management

app = Flask(__name__)

# Use environment variable for database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Hashed password


@app.route('/')
def index():
    users = User.query.all()  # Fetch data from the database
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()  # Save to the database
    return redirect('/')

from werkzeug.security import check_password_hash
from flask import session

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user id in session
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to home page

        flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

if __name__ == '__main__':
    app.run()
