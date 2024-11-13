from app.models import Category, Product, User
from app import app, db
import hashlib

def load_categories():
    return Category.query.order_by('id').all()


def load_products(kw=None, cate_id=None, page=1):
    query = Product.query

    if kw:
        query = query.filter(Product.name.contains(kw))

    if cate_id:
        query = query.filter(Product.category_id == cate_id)

    page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    query = query.slice(start, start + page_size)

    return query.all()

def count_products():
    return Product.query.count()


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = User(name=name,username=username, password=password,
             avatar="https://res.cloudinary.com/dehkjrhjw/image/upload/v1730272749/cld-sample-4.jpg")
    db.session.add(u)
    db.session.commit()
