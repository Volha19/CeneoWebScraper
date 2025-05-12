from flask import render_template
from app import app

@app.route("/")  
@app.route("/<name>")  
def greeting(name = "World"):
    return render_template("index.html")

@app.route("/extract")  
def extract(name = "World"):
    return render_template("extract.html")

@app.route("/extract")  
def products(name = "World"):
    return render_template("products.html")

@app.route("/product/<product_id>")  
def product(name = "World"):
    return render_template("product.html")

@app.route("/about")  
def about(name = "World"):
    return render_template("about.html")



    
#flask run --debug   - reload of the page
