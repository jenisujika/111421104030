from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuring the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Product model


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    productName = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Product {self.productName}>'


# Create the database and tables
with app.app_context():
    db.create_all()

# Insert sample data
with app.app_context():
    if Product.query.count() == 0:
        sample_products = [
            Product(company="AMZ", category="Laptop", productName="Laptop 1",
                    price=2236, rating=4.7, discount=63, availability="yes"),
            Product(company="AMZ", category="Laptop", productName="Laptop 2",
                    price=1244, rating=4.5, discount=45, availability="out-of-stock"),
            Product(company="AMZ", category="Laptop", productName="Laptop 3",
                    price=1059, rating=2.77, discount=21, availability="yes"),
            Product(company="FLP", category="Phone", productName="Phone 1",
                    price=2059, rating=7.77, discount=29, availability="yes"),
            Product(company="FLP", category="Phone", productName="Phone 2",
                    price=3059, rating=8.77, discount=30, availability="yes")

        ]
        db.session.bulk_save_objects(sample_products)
        db.session.commit()


@app.route('/categories/<categoryname>/products', methods=['GET'])
def get_top_products(categoryname):
    company = request.args.get('company')
    n = int(request.args.get('n', 10))
    page = int(request.args.get('page', 1))
    sort_by = request.args.get('sort_by', 'price')
    order = request.args.get('order', 'asc')

    print(f"company: {company}, categoryname: {categoryname}")

    sort_order = getattr(Product, sort_by).asc(
    ) if order == 'asc' else getattr(Product, sort_by).desc()

    query = Product.query.filter_by(
        company=company, category=categoryname).order_by(sort_order)
    total_products = query.count()

    print(f"Total products found: {total_products}")

    if total_products == 0:
        return jsonify([])

    # Pagination
    paginated_products = query.paginate(page=page, per_page=n).items

    return jsonify([{
        "id": product.id,
        "company": product.company,
        "category": product.category,
        "productName": product.productName,
        "price": product.price,
        "rating": product.rating,
        "discount": product.discount,
        "availability": product.availability
    } for product in paginated_products])


@app.route('/categories/<categoryname>/products/<int:productid>', methods=['GET'])
def get_product_details(categoryname, productid):
    company = request.args.get('company')

    product = Product.query.filter_by(
        id=productid, company=company, category=categoryname).first()

    if product:
        return jsonify({
            "id": product.id,
            "company": product.company,
            "category": product.category,
            "productName": product.productName,
            "price": product.price,
            "rating": product.rating,
            "discount": product.discount,
            "availability": product.availability
        })
    else:
        return jsonify({"error": "Product not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
