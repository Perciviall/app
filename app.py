from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')  # Replace with Render connection details
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model for your database (example table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    users = User.query.all()  # Fetch data from the database
    return render_template('index.html', users=users)

with app.app_context():
    db.create_all()  # This will create the tables based on the models

if __name__ == '__main__':
    app.run()