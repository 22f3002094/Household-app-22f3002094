from  flask import render_template , redirect ,request
from flask import current_app as app


@app.route("/" , methods = ["GET" , "POST"])
def home():
    return render_template("home.html" )