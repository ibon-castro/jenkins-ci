from flask import Flask, render_template, request, redirect, url_for
from models import User, db

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Logic to add user to DB
        return redirect(url_for('success'))
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)

