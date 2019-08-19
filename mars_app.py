from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

@app.route("/")
def index():
    mars = db.mars_data.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
  
    mars_data_new = scrape_mars.scrape()
    db.mars_data.update({}, mars_data_new, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
    
    
 