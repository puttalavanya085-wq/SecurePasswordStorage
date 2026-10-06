from flask import Flask, render_template, request, redirect, url_for
import hashlib
import os
import json

app = Flask(__name__)

file = "users.json"

def load_users():
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(file, "w") as f:
        json.dump(users, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        if username in users:
            message = "Username already exists!"
        else:
            salt = os.urandom(16).hex()
            hashed = hashlib.sha256((password + salt).encode()).hexdigest()

            users[username] = {
                "salt": salt,
                "hash": hashed
            }

            save_users(users)
            message = "Registration successful!"

    return render_template("register.html", message=message)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        if username in users:
            salt = users[username]["salt"]
            hashed = hashlib.sha256((password + salt).encode()).hexdigest()

            if hashed == users[username]["hash"]:
                message = "Login successful!"
            else:
                message = "Invalid password!"
        else:
            message = "User not found!"

    return render_template("login.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)