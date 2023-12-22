import cs50
import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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


    transactions = db.execute("SELECT symbol, SUM(shares), price FROM transactions WHERE userid = ? GROUP BY symbol", session["user_id"])
        #transactions [{'symbol': 'a', 'SUM(shares)': 6, 'price': 127.2}, {'symbol': 'b', 'SUM(shares)': 1, 'price': 28.5}]
    balance = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
        #balance [{'cash': 6452.07}]

    """Show portfolio of stocks"""
    return render_template("index.html", transactions=transactions, balance=balance)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    if lookup(request.form.get("symbol"))==None:
        return apology("missing symbol", 400)

    balance_old = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    balance_new = (balance_old[0]['cash']) - int(request.form.get("shares"))*(lookup(request.form.get("symbol"))["price"])
    if balance_new < 0:
        return apology("can't afford", 400)
    db.execute("UPDATE users SET cash = ? WHERE id = ?", balance_new, session["user_id"])
    date = datetime.datetime.now()
    db.execute("INSERT INTO transactions (userid, symbol, shares, price, time) VALUES(?,?,?,?,?)", session["user_id"],request.form.get("symbol"), int(request.form.get("shares")), lookup(request.form.get("symbol"))["price"], date)

    flash("Bought!")
    return redirect("/")

@app.route("/history")
@login_required
def history():

    """Show history of transactions"""
    transactions = db.execute("SELECT symbol, shares, price, time FROM transactions WHERE userid = ?", session["user_id"])
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    if lookup(request.form.get("symbol"))==None:
        return apology("symbol is invalid", 400)

    symboll_name=lookup(request.form.get("symbol"))["name"]
    symboll_price=lookup(request.form.get("symbol"))["price"]
    symboll_symbol=lookup(request.form.get("symbol"))["symbol"]

    return render_template("quoted.html", symboll_name=symboll_name, symboll_price=symboll_price, symboll_symbol=symboll_symbol)


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
            #db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), hash)
            gender = request.form.get("gender")
            print(gender)
            if gender=='Male':
                Calorie_Intake = int(88.36 + 13.4*(int(request.form.get("Weight"))) + 4.8*(int(request.form.get("Height"))) -5.7*int((request.form.get("Age"))))
                print("Calorie_Intake_Male", Calorie_Intake)
            else:
                Calorie_Intake = int(447.6 + 9.2*(int(request.form.get("Weight"))) + 3.1*(int(request.form.get("Height"))) - 4.3*int((request.form.get("Age"))))
                print("Calorie_Intake_Female", Calorie_Intake)
            db.execute("INSERT INTO users (username, hash, calorie_intake) VALUES(?, ?, ?)", request.form.get("username"), hash, Calorie_Intake)

            return redirect("/")

    else:
        """Register user"""
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        transactions = db.execute("SELECT symbol, SUM(shares), price FROM transactions WHERE userid = ? GROUP BY symbol", session["user_id"])
        return render_template("sell.html", transactions=transactions)

    tr=db.execute("SELECT SUM(shares) FROM transactions WHERE userid = ? AND symbol=?", session["user_id"], request.form.get("symbol"))
    if tr[0]["SUM(shares)"]<int(request.form.get("shares")):
        return apology("Too many shares", 400)

    balance_old = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    balance_new = balance_old[0]['cash'] + int(request.form.get("shares"))*(lookup(request.form.get("symbol"))["price"])
    db.execute("UPDATE users SET cash = ? WHERE id = ?", balance_new, session["user_id"])
    date = datetime.datetime.now()
    db.execute("INSERT INTO transactions (userid, symbol, shares, price, time) VALUES(?,?,?,?,?)", session["user_id"],request.form.get("symbol"), -1*(int(request.form.get("shares"))), lookup(request.form.get("symbol"))["price"], date)

    flash("Sold!")

    return redirect("/")
