# Jeopardy

This project makes a simple web app using Python and the Flask framework to search for Jeopardy Clues based on air date, dollar value, and category.
* In order to search by category, currently the user must type the category exactly how it is written in the results from the below API (i.e. case sensitive)
* In the future, I would also add pagination for results. Currently if there are over 100 results, my web app only displays those 100 without an option to go to the next 100, etc. To fix this, I would add a button that makes another API call to the /clues, and the "offset" parameter would be incremented by 100 to show the next 100.

It uses the API found here: http://jservice.io/

The web app is currently hosted on Heroku and can be found here: https://andrew-jeopardy.herokuapp.com/
