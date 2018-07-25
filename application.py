import os

from flask import Flask, session, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import json


#key: vhneXzU3MarEL32SDgrw
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

#import requests
#res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "vhneXzU3MarEL32SDgrw", "isbns": "9781632168146"})
#print(res.json())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        login = request.form['login']
        print(login)
        password = request.form['password']
        print(f"Login:{login} Password:{password}")
    return render_template("register.html")
