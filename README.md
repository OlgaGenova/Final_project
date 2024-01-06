# Daily Calorie Intake Calculator
#### Video Demo:  <https://youtu.be/01MlDAKkFuw>
#### Description: 
This is my final project for conclude the CS50 Introduction to Computer Sciense course.
The Calorie Calculator can be used to estimate the number of calories a person needs to consume each day.
Also it allows you to look up calorie information in a food database or even add your own product into the database, which allow you to log and track your daily calorie consumption.

  ## Tech used:
  - Python (Flask)
  - SQL
  - HTML
  - CSS
  - JavaScript

### Download & Installation
1. Clone the repository: `git clone https://github.com/`
1. Install the required dependencies using pip: `$ pip install -r requirements.txt`
1. Run `flask run` in your terminal
1. Access the application at http://localhost:5000/.

### Files content 
`app.py` a python program that allowing to create dynamically web pages;  
`helpers.py` helper functions(login_required(), apology()) for the application are defined here;  
`requirements.txt` that file simply prescribes the packages on which this app will depend;  
`calories.db` SQL database;  
`styles.css` styling of all the frontend;  
`food_calorie_chart` caloric content of food;  
`apology.html` this file appears inc ase if: username is already taken, you haven't choosen a product or your daily calorie intake has been exceeded;  
`contacts.html` for receiving a feedback;  
`eat.html` add food into your food consumption (note, how Remaining calorie balance will decrease;  
`history.html` view the history of your consumptions;  
`index.html` landing page. The main page tracking your daily calorie consumption and remaining calorie balance;  
`layout.html` HTML layout file from which all pages are built. Contains the head of each html page and the navbar;  
`login.html` login page. Contains the form to log in;  
`register.html` register page. Contains the form to sign up;  
`your_menu.html` you have a possibility to add the product if it isn't in the database by entering the product and how many calories 100 grams of this item contain.

## SQL
All the changes of the program happen in the file calories.db.  
There are the main tables here.
# users  
`CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, calorie_intake INTEGER, remaining_calorie_balance INTEGER);` 
This table is updated upon registration: username, hash(the function for securely entering a password), calorie_intake determined according to the formula above.  
# transactions  
`CREATE TABLE transactions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, userid INTEGER NOT NULL, product TEXT NOT NULL, grams INTEGER, cal_100gr REAL, time DATETIME);` 
Data updates when a user add some food or reset the counter (by clicking on the button `Reset Start From Scratch`)when he is going to start a new day for exemple.  
# calories  
`CREATE TABLE calories (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, product TEXT NOT NULL, cal_100gr INTEGER);` 
The list of products with calorie content per hundred grams of product.

### Usage
When registering, you must indicate your physical parameters (height, weight, age, gender) to determine the required daily calorie intake. This rate is calculated using the Harris Benedict Equation (BMR Formula).

Men:
`BMR = 88.362 + (13.397 × weight [kg]) + (4.799 × height [cm]) – (5.677 × age [years])`

Women:
`BMR = 447.593 + (9.247 × weight [kg]) + (3.098 × height [cm]) – (4.330 × age [years])`

- After logging in you will see your required daily calorie intake.  
- You can first take a look at the caloric content of food (`Food Calorie Chart` tab)
- During the day, add food that you have eaten or are going to eat (`Eat some calories` tab).  
- If this product is not in the database, you can add it yourself (`Create Your Menu` tab).  
- As you add products to your consumption list, your balance will decrease. If you exceed your daily calorie intake, the program will notify you about it.  
- When you start a new day, don't forget to do a reset to update your BMR's counter (`Reset (Start From Scratch)` button).  
- You can also view the history of your food consumption (`History` tab)
> [!NOTE]
> There are age restrictions (only 18+).
