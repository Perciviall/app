from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host/dbname'  # Replace with Render connection details
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

if __name__ == '__main__':
    app.run()
