# -*- coding: utf-8 -*-
# Librarys
from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

# from PIL import image, ImageDraw


import os

# Variables
app = Flask(__name__)

IMG_FOLDER = os.path.join("static", "IMG")
app.config["UPLOAD_FOLDER"] = IMG_FOLDER

# Settings
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "secret"
login = LoginManager()
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# la base db
class Users(db.Model):
    __tablename__ = "Inscription"
    id = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String())
    date_naissance = db.Column(db.String())
    nationalite = db.Column(db.String(50))
    sexe = db.Column(db.String(1), unique=True)
    CNI = db.Column(db.String(), unique=True)
    telephone = db.Column(db.String(100))
    photo_pp = db.Column(db.String(100))
    statut = db.Column(db.String())

    def password(self):
        raise AttributeError("password is not a readable attribute!")

    # @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"data_test( '{self.name}','{self.email,}','{self.tel}')"


@app.before_first_request
def create_all():
    # db.drop_all()
    db.create_all()


# route index
@app.route("/", methods=("GET", "POST"))
def index():
    return render_template("index.html")


# route login
@app.route("/login", methods=("GET", "POST"))
def login():
    return render_template("login.html")


# route register
@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        nom = request.form["name"]
        prenom = request.form["lastname"]
        username = request.form["username"]
        email = request.form["email"]
        password_hash = request.form["password"]
        date_naissance = request.form["date_naiss"]
        nationalite = request.form["nationalite"]
        sexe = request.form["sexe"]
        CNI = request.form["cni"]
        telephone = request.form["tel"]
        register = Users(
            nom=name,
            prenom=lastname,
            username=username,
            email=email,
            password_hash=password_hash,
            date_naissance=date,
            nationalite=nationalite,
            sexe=sexe,
            cni=cni,
            tel=tel,
        )
        print("Les Données du Formulaire sont enrégistrées avec succès")
        print("---------------")
        print(
            f"nom : {name},prenom:{lastname} ,username:{username},email :{email} ,password_hash: {password},date_naissance:{date},nationalite:{nationalite},sexe:{sexe},cni:{cni},telephone: {tel} "
        )
        return redirect(url_for("login"))
    else:
        return render_template("register.html")


# route accueil
@app.route("/accueil", methods=("GET", "POST"))
def accueil():
    return render_template("accueil.html")


# Run
if __name__ == "__main__":
    app.run()
