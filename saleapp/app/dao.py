from app.models import Category, Product, User, Receipt, ReceiptDetails
from app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func


def load_categories():
    return Category.query.order_by('id').all()


def load_products(kw=None, category_id=None, page=1):
    products = Product.query

    if kw:
        products = products.filter(Product.name.contains(kw))

    if category_id:
        products = products.filter(Product.category_id == category_id)

    page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    products = products.slice(start, start + page_size)

    return products.all()


def count_products():
    return Product.query.count()


def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User.query.filter(User.username.__eq__(username.strip()),
                          User.password.__eq__(password))
    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(name=name, username=username, password=password,
             avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg')

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get('secure_url')

    db.session.add(u)
    db.session.commit()


def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], unit_price=c['price'],
                               product_id=c['id'], receipt=r)
            db.session.add(d)

        db.session.commit()


def get_user_by_id(id):
    return User.query.get(id)


def revenue_stats(kw=None):
    query = db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price)) \
        .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id)).group_by(Product.id)

    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.all()


if __name__ == '__main__':
    with app.app_context():
        print(revenue_stats())
