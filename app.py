import cs50
import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True

Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///calories.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    transactions = db.execute("SELECT product, SUM(grams), cal_100gr FROM transactions WHERE userid = ? GROUP BY product", session["user_id"])
    calorie_intake = db.execute("SELECT calorie_intake FROM users WHERE id=?", session["user_id"])
    remaining_calorie_balance = db.execute("SELECT remaining_calorie_balance FROM users WHERE id = ?", session["user_id"])

    """Show how many calories the user has eaten and calories remained"""
    return render_template("index.html", transactions=transactions, calorie_intake=calorie_intake, remaining_calorie_balance=remaining_calorie_balance)


@app.route("/eat", methods=["GET", "POST"])
@login_required
def eat():

    """Eat calories"""
    if request.method == "GET":
        calories_get = db.execute("SELECT product, cal_100gr FROM calories ORDER BY product")
        return render_template("eat.html", calories_get=calories_get)
    
    if request.form.get("product")==None:
        return apology("missing product", 400)

    balance_old = db.execute("SELECT remaining_calorie_balance FROM users WHERE id = ?", session["user_id"])
    calories = db.execute("SELECT cal_100gr FROM calories WHERE product = ?", request.form. get("product"))

    balance_new = (balance_old[0]['remaining_calorie_balance']) - int(request.form.get("grams"))*(calories[0]['cal_100gr'])/100

    if balance_new < 0:
        return apology("Your daily calorie intake has been exceeded!", 400)
    db.execute("UPDATE users SET remaining_calorie_balance = ? WHERE id = ?", balance_new, session["user_id"])
    date = datetime.datetime.now()
    db.execute("INSERT INTO transactions (userid, product, grams, cal_100gr, time) VALUES(?,?,?,?,?)", session["user_id"],request.form.get("product"), int(request.form.get("grams")), calories[0]['cal_100gr'], date)

    flash("Done!")
    return redirect("/")


@app.route("/history")
@login_required
def history():

    """Show history of eating"""
    transactions = db.execute("SELECT product, grams, cal_100gr, time FROM transactions WHERE userid = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/food_calorie_chart")
@login_required
def food_calorie_chart():
    
    calories = db.execute("SELECT * FROM calories GROUP BY product")
    return render_template("food_calorie_chart.html", calories=calories)


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # Ensure all the gaps aren't blank
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Fill in all the gaps", 400)

        # Ensure passwords are equal
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("check the passwords", 400)


        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) >= 1:
            return apology("username is already taken", 400)
        else:
            hash = generate_password_hash(request.form.get("password"))
            gender = request.form.get("gender")
            if gender=='Male':
                Calorie_Intake = int(88.36 + 13.4*(int(request.form.get("Weight"))) + 4.8*(int(request.form.get("Height"))) -5.7*int((request.form.get("Age"))))
            else:
                Calorie_Intake = int(447.6 + 9.2*(int(request.form.get("Weight"))) + 3.1*(int(request.form.get("Height"))) - 4.3*int((request.form.get("Age"))))
            db.execute("INSERT INTO users (username, hash, calorie_intake, remaining_calorie_balance) VALUES(?, ?, ?, ?)", request.form.get("username"), hash, Calorie_Intake, Calorie_Intake)
            return redirect("/")

    else:
        """Register user"""
        return render_template("register.html")
    

@app.route("/your_menu", methods=["GET", "POST"])
@login_required
def your_menu():
    """Add product into food_calorie_chart"""
    if request.method == "GET":
        return render_template("your_menu.html")

    db.execute("INSERT INTO calories (product, cal_100gr) VALUES(?,?)", request.form.get("product"), int(request.form.get("cal_100gr")))
    flash("Product's added!")

    return redirect("/")

@app.route("/contacts", methods=["GET", "POST"])
@login_required
def contacts():
    """If the user want to give the feedback"""
    if request.method == "GET":
        return render_template("contacts.html")
    flash("Thanks!, I'll contact you!")
    return redirect("/")


@app.route("/reset", methods=["POST"])
@login_required
def reset():
    "Reset your eating, history of eating to start from a scratch(a new day)"
    db.execute("DELETE FROM transactions WHERE userid = ?", session["user_id"])
    db.execute("UPDATE users SET remaining_calorie_balance = calorie_intake WHERE id=?", session["user_id"])
                                                                                                 
    return redirect("/")
