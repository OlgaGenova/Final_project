# Daily Calorie Intake Calculator
#### Video Demo:  <https://youtu.be/oJe5tnWf3TU>
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
