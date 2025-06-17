from app import app
import json
import os
import pandas as pd
from flask import render_template, redirect, url_for, request, send_file, abort, send_from_directory
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
            print("www")
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
                product_id = filename[:-5]  
                product = Product(product_id)
                product.import_info()
                products.append(product)
    return render_template("products.html",products=products)

@app.route("/product/<product_id>")
def product(product_id):
    product = Product(product_id)
    product.import_opinions()
    return render_template("product.html", product_id=product_id, opinions = product.opinions)

@app.route("/product/<product_id>/charts")
def charts(product_id):
    try:
        product = Product(product_id)
        product.import_opinions()
        product.generate_charts()
        if not product.opinions:
            return "No opinions found for this product", 404
        product.generate_charts()
        return render_template("charts.html", product_id=product_id)
    except Exception as e:
        return f"Error generating charts: {e}", 500

@app.route("/about")  
def about():
    return render_template("about.html")

@app.route('/download/<product_id>')
def download_product(product_id):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'data', 'opinions', f'{product_id}.json')
    if not os.path.exists(json_path):
        abort(404, description="File not found.")
    file_format = request.args.get('format', 'json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    if file_format == 'json':
        return send_file(json_path, as_attachment=True, download_name=f'{product_id}.json')
    elif file_format == 'csv':
        csv_path = os.path.join(base_dir, 'data', 'opinions', f'{product_id}.csv')
        df.to_csv(csv_path, index=False, encoding='utf-8')
        return send_file(csv_path, as_attachment=True, download_name=f'{product_id}.csv')
    elif file_format == 'xls':
        excel_path = os.path.join(base_dir, 'data', 'opinions', f'{product_id}.xlsx')
        df.to_excel(excel_path, index=False)
        return send_file(excel_path, as_attachment=True, download_name=f'{product_id}.xlsx')
    else:
        abort(400, description="Invalid format specified")

    
#flask run --debug   - reload of the page
