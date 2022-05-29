# Foodzee
Foodzee is a website created to provide users with recommendation of restaurants from where they may like ordering using content based filtering. The dataset includes almost 1300 restaurants pan India. The code has been developed using Python programming language. The website is developed using Flask. The analysis and model is developed using ScikitLearn library. 




STRUCTURE:



• app.py:
This file contains the main backend operations of the website and is 
useful for running the flask server locally.



• requirement.txt:
This file contains all the dependencies and requirements of the program.



• templates:
It contains all the HTML files:



➢ home.html: Contains home page.



➢ search.html: Displays restaurants based on the location selected 
by the user and gives the user the option to either search the 
restaurant name manually or apply filters like – sorting on the 
basis of rating, sorting on the basis of cuisine, and according to the 
budget of the user.



➢ res.html: Displays users the restaurants they searched manually in 
the search bar.



➢ rating.html: Displays users the restaurants after applying the 
selected filters.



➢ order.html: Takes the user’s age to recommend restaurants on the 
baisis of the age group of users



➢ like.html: This page recommends users the other restaurants they 
may like ordering from.



• static:
It contains the CSS file and all the images used in building the websites.


• india.csv:
It contains the dataset, i.e. basically the list of restaurants in 29 cities, 
including NCR which consists of cities like New Delhi and Gurgaon.


STEPS TO RUN THE PROJECT:


• Open the Terminal.


• Clone the submitted repository by using the git clone command.



• Ensure that Python and pip are installed on the system.



• Change the diectory to repository name using $ cd [Repository name].



• Create a virtualenv by executing the following command: virtualenv env.


• Activate the env virtual environment by executing the follwing 
command: source env/bin/activate.


• Enter the cloned repository directory and execute pip install -r 
requirements.txt.


• Now, execute the following command: flask run and it will point to the 
localhost server with the port 5000.


• Enter the IP Address: http://localhost:5000 on a web browser and use 
the web application.


DEPENDENCIES:


Following are the dependencies of my project:


• scikit-learn


• Flask


• pandas


• numpy


• scikit-learn


• gunicorn


CONCEPTS AND ALGORITHMS USED:


• Sorting: Used specifically for sorting the restaurants based on their 
location, ratings and cuisines.


• Cosine Similarity: Used specifically to arrange similar restaurants based 
on the highlight section under each restaurant.
