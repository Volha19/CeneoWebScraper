from app import app
import json
import os
from flask import render_template, redirect, url_for, request
from app.forms import ExtractionForm
from app.models import Product

@app.route("/")  
def index():
    return render_template("index.html")


@app.route("/extract")
def render_form():
    form = ExtractionForm()
    return render_template("extract.html", form=form)

@app.route("/extract", methods=['POST'])
def extract():
    form = ExtractionForm(request.form)
    if form.validate():
        product_id = form.product_id.data
        product = Product(product_id)
        if product.extract_name():
            product.extract_opinions()
            product.analyze()
            product.export_info()
            product.export_opinions()
            return redirect(url_for('product', product_id=product_id))
        form.product_id.errors.append('There is no product for provided id or product has no opinions')
        return render_template('extract.html', form=form)
    return render_template('extract.html', form=form)

@app.route("/products")
def products():
    product_dir = "./app/data/products"
    products = []

    if os.path.exists(product_dir):
        for filename in os.listdir(product_dir):
            if filename.endswith(".json"):
                product = Product(filename[:-5])
                product.import_info()
                products.append(product)
    return render_template("products.html",products=products)

@app.route("/product/<product_id>")
def product(product_id):
    return render_template("product.html", product_id=product_id)

@app.route("/about")  
def about():
    return render_template("about.html")



    
#flask run --debug   - reload of the page
