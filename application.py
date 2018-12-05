import os

from flask import Flask, session, request, render_template, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login', methods=("GET", "POST"))
def login():
    # TODO: logic for if a user is already in session
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        error = ''
        if username is None:
            error = 'username is required'
        elif password is None:
            error = 'password is requred'
        elif db.execute("SELECT id FROM users WHERE username = :un and pw = :pw;",
                        {'un': username,
                         'pw': generate_password_hash(password)
                         }).fetchone() is not None:
            error = f"Welcome back {username}"
            flash(f'Welcome back {username}!')
            return redirect(url_for('index'))
        flash(error)
    return render_template('login.html')


@app.route('/register', methods=("GET", "POST"))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if username is None:
            error = 'username is required'
        elif password is None:
            error = 'password is requred'
        elif db.execute("SELECT id FROM users WHERE username = :un;",
                        {'un': username}).fetchone() is not None:
            error = f"username {username} already registered"

        if error is None:
            db.execute("INSERT INTO users (username, pw) VALUES (:un, :pw)",
                       {'un': username, 'pw': generate_password_hash(password)})
            db.commit()
            return redirect(url_for('login'))

        flash(error)
    return render_template('register.html')
