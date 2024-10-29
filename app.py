from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
from werkzeug.security import check_password_hash
import io

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('/login'))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)

app.secret_key = os.urandom(24)  # Set a secret key for session management

# Use environment variable for database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Ensure this column is defined
    password = db.Column(db.String(128), nullable=False)  # Hashed password

class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Save the file with the original filename
    new_file = FileUpload(name=file.filename, file_data=file.read())
    db.session.add(new_file)
    db.session.commit()

    return redirect(url_for('search'))  # Change this to the name of the route you want to redirect to


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    
    # If a query is provided, filter the results based on the name
    if query:
        results = FileUpload.query.filter(FileUpload.name.ilike(f'%{query}%')).all()  # Use ilike for case-insensitive search
    else:
        results = FileUpload.query.all()  # If no query, return all files

    # Render the results in the template
    return render_template('results.html', results=results)  # Adjust according to your template

@app.route('/')
@login_required
def index():
    user = User.query.get(session['user_id'])  # Get the logged-in user
    users = User.query.all()  # Get all users for the list
    return render_template('index.html', user=user, users=users)

@app.route('/download/<int:file_id>')
def download_file(file_id):
    file = FileUpload.query.get(file_id)
    if file:
        # Assuming file.name includes the full filename with extension
        return send_file(
            io.BytesIO(file.file_data),
            download_name=file.name,  # This should include the extension, e.g., 'example.pdf'
            as_attachment=True
        )
    return "File not found", 404

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.before_request
def create_tables():
    if not hasattr(create_tables, 'initialized'):
        with app.app_context():
            db.create_all()
        create_tables.initialized = True  # Mark as initialized

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Clear the session
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))  # Redirect to login page


# Use the application context to access the database
#with app.app_context():
#    db.drop_all()   # Drop all tables
#    db.create_all() # Recreate all tables


if __name__ == '__main__':
    #app.run()
    app.run(debug=True)
