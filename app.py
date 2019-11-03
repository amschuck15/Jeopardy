# imports needed for Flask web app and SQL databases
import os
import json
import requests
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

# Initializing paths, databases, and other Flask/SQL setup things
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "categorydatabase.db"))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)


# The Category class used for the database. Each Category has an id (integer) and a category (String) attribute
# Both the category id and name must be unique to add a Category to the database
class Category(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    category = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)

    def __repr__(self):
        return "<Category: {}>".format(self.category)


# The search function which takes user input and loads the appropriate form (either results.html or search.html).
# Expects GET or POST methods, checks for blank search fields to narrow down on the search in the API call. Due to the
# API of the Jeopardy clues taking an ID for a category instead of a String, I had to add all categories to a database
# to retrieve the ID of a given category (I don't think it was doable given the API from the Jeopardy site)
@app.route('/', methods=['GET', 'POST'])
def search():
    # If the user clicked the search button
    if request.method == "POST":
        # checking if at least one field is completed and submitted
        if request.form['value'] != '' or request.form['category'] != '' or request.form['min_date'] != '':
            value = None  # parameters for API default to None
            category = None  # parameters for API default to None
            min_date = None  # this variable actually represents the upper bound of the date. The API is wrong
            max_date = None  # this variable actually represents the lower bound of the date. The API is wrong

            # Checking if user filled out the "value" option in the search field
            if request.form['value'] != '':
                value = request.form['value']
            # Checking if user filled out the "category" option in the search field
            if request.form['category'] != '':
                category_input = request.form['category']
                # Accessing the database to check if the category is actually a category
                if Category.query.filter_by(category=category_input).first() is None:
                    category = -1  # this will ensure that the results come back empty because category doesn't exist
                else:
                    # Category exists, so the category parameter being used in API is set to category ID from database
                    category = Category.query.filter_by(category=category_input).first().id
            # Checking if user filled out the "min_date" option in the search field
            if request.form['min_date'] != '':
                min_date = request.form['min_date']
            # Checking if user filled out the "max_date" option in the search field
            if request.form['max_date'] != '':
                max_date = request.form['max_date']

            # Setting the parameters for the API call to the entries in the search boxes
            parameters = {
                "value": value,
                "category": category,
                "min_date": max_date,  # this is purposefully switched because the API is incorrectly documented
                "max_date": min_date  # this is purposefully switched because the API is incorrectly documented
            }
            # response from the Jeopardy API
            response = requests.get("http://jservice.io/api/clues", params=parameters)
            # Render the html template for results, making sure to pass the response.text to the Jinja formatting
            return render_template('results.html', clues=json.loads(response.text))
    return render_template('search.html') # rendering the search page again for compilation of code


# Required for FLASK app
if __name__ == "__main__":
    app.run(debug=True)


# Adding all the categories to a database
# I ONLY USED THIS CODE ONCE TO GET MY DATABASE, DOESN'T NEED TO RUN EVERY TIME
# I AM LEAVING THIS CODE JUST TO SHOW HOW I ADDED CATEGORIES TO MY SQLLITE DATABASE
'''
parameters = {
        'count': 100,
        'offset': 0
}
db.create_all()
while True:
    response = requests.get("http://jservice.io/api/categories", params=parameters)
    if response.text == "[]": # if the JSON is empty (meaning at the end of categories) break out of loop
        break
    for categories in response.json():
        if categories["id"] is not None and categories["title"] is not None:
            db.session.add(Category(id=categories["id"], category=categories["title"]))
            db.session.commit()

    parameters['offset'] = parameters.get('offset', 0) + 100 # get next 100 categories
'''