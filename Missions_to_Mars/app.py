from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Set route
@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    
    return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scraper():
    mars_info_collection = mongo.db.mars_info

    results_dict = scrape_mars.scrape()

    mars_info_collection.update({}, results_dict, upsert=True)
    
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
