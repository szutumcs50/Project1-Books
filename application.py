import os

from flask import Flask, session, request, render_template, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

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

@app.route("/login")
def login():
    if request.method == 'POST':
        pass
    return render_template('login.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        hash = generate_password_hash(password)
        print(f"Username: {login} Password: {password}\nHash: {hash}")
        db.execute("INSERT INTO users (login, password) VALUES (:login,:password)", {'login':login, 'password':hash})
        db.commit()
    return render_template("register.html")

@app.route("/books")
def books():
    rows = db.execute("SELECT * FROM books LIMIT 50")
    return render_template('list.html', rows=rows)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == 'POST':
        q = request.form['search']
        q = "%" + q + "%"
        rows = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn OR title LIKE :title OR author LIKE :author OR year LIKE :year",
                            {'isbn':q, 'title':q, 'author':q, 'year':q})
        #rows = db.execute("SELECT * FROM books WHERE title LIKE :title", {'title':qq})
        return render_template("list.html", rows=rows)
    return render_template('search.html')
