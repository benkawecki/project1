import os

from flask import Flask, session, request, render_template, flash
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


@app.route('/login')
def login():
    name = request.form.get("Name")
    pw = request.form.get("Password")
    db.execute(f"SELECT ")
    return 'login'


@app.route('/register')
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if username is None:
            error = 'username is required'
        elif password is None:
            error = 'password is requred'
        elif db.execute("SELECT id IN users WHERE username = (?) ", (username,)) is not None:
            error = f"username {username} already registered"

        if error is None:
            db.execute("INSERT INTO users (username, pw) VALUES (?, ?)",
                      (username, generate_password_hash(password)))


    return render_template('register.html')
