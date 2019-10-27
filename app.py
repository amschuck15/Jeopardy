import os
import json
import requests
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "categorydatabase.db"))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    category = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)

    def __repr__(self):
        return "<Category: {}>".format(self.category)


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        # checking if at least one field is completed and submitted
        if request.form['value'] != '' or request.form['category'] != '' or request.form['min_date'] != '':
            value = None  # parameters for API default to None
            category = None  # parameters for API default to None
            min_date = None  # this variable actually represents the upper bound of the date. The API is wrong
            max_date = None  # this variable actually represents the lower bound of the date. The API is wrong

            if request.form['value'] != '':
                value = request.form['value']
            if request.form['category'] != '':
                category_input = request.form['category']
                if Category.query.filter_by(category=category_input).first() is None:
                    category = -1  # this will ensure that the results come back empty
                else:
                    category = Category.query.filter_by(category=category_input).first().id
            if request.form['min_date'] != '':
                min_date = request.form['min_date']
            if request.form['max_date'] != '':
                max_date = request.form['max_date']

            parameters = {
                "value": value,
                "category": category,
                "min_date": max_date,  # this is purposefully switched because the API is incorrectly documented
                "max_date": min_date  # this is purposefully switched because the API is incorrectly documented
            }
            response = requests.get("http://jservice.io/api/clues", params=parameters)
            return render_template('results.html', clues=json.loads(response.text))
    return render_template('search.html')


if __name__ == "__main__":
    app.run(debug=True)


# Adding all the categories to a database
# I ONLY USED THIS CODE ONCE TO GET MY DATABASE, DOESN'T NEED TO RUN EVERY TIME
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