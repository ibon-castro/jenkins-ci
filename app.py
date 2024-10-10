from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from models import User, db

app = Flask(__name__)

# Set a secret key for CSRF protection
app.config['SECRET_KEY'] = '24300128ab'  # Make sure to use a strong, secure key

# Enable CSRF protection
csrf = CSRFProtect(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Example with SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

@app.route('/')
def home():
    return redirect(url_for('register'))  # Redirect to the register page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Logic to add user to DB
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('success'))
    
    return render_template('register.html')

@app.route('/success')
def success():
    return "Registration successful!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
    app.run(host='127.0.0.1', port=5000, debug=False)
