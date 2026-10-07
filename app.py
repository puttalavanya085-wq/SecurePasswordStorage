from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
import os
import json

app = Flask(__name__)
app.secret_key = "secure_password_storage_key"

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
    message = ""

    if request.args.get("registered") == "1":
        message = "Registration successful!"

    return render_template("index.html", message=message)


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        if username in users:
            return render_template(
                "register.html",
                message="Username already exists!"
            )

        salt = os.urandom(16).hex()

        hashed = hashlib.sha256(
            (password + salt).encode()
        ).hexdigest()

        users[username] = {
            "salt": salt,
            "hash": hashed
        }

        save_users(users)

        return redirect(url_for("home", registered="1"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        if username in users:

            salt = users[username]["salt"]

            hashed = hashlib.sha256(
                (password + salt).encode()
            ).hexdigest()

            if hashed == users[username]["hash"]:

                session["username"] = username

                return redirect(url_for("welcome"))

            else:
                message = "Invalid password!"

        else:
            message = "User not found!"

    return render_template("login.html", message=message)


@app.route("/welcome")
def welcome():

    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    return render_template(
        "welcome.html",
        username=username
    )


@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
