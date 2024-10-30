from sqlalchemy import Integer, Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app import db, app


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship("Product", backref='category', lazy=True)


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(100), nullable=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # c1 = Category(name="Smartphone")
        # c2 = Category(name="Tablet")
        # c3 = Category(name="Desktop")
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()

        data = [{
            "id": 1,
            "name": "iPhone 7 Plus",
            "description": "Apple, 32GB, RAM: 3GB, iOS13",
            "price": 17000000,
            "image": "https://res.cloudinary.com/dehkjrhjw/image/upload/v1730273590/iphone-7-plus-rose-gold_x1rryi.jpg",
            "category_id": 1
        }, {
            "id": 2,
            "name": "iPad Pro 2020",
            "description": "Apple, 128GB, RAM: 6GB",
            "price": 37000000,
            "image": "https://res.cloudinary.com/dehkjrhjw/image/upload/v1730278180/ipad_pro_11_2020_u8mr7f.webp",
            "category_id": 2
        }, {
            "id": 3,
            "name": "Galaxy Note 10 Plus",
            "description": "Samsung, 64GB, RAML: 6GB",
            "price": 24000000,
            "image": "https://res.cloudinary.com/dehkjrhjw/image/upload/v1730278216/note_10_plus_5g_tmlque.webp",
            "category_id": 1
        }]

        # for p in data:
        #     prod = Product(name=p['name'], description=p['description'], price=p['price'],
        #                image=p['image'], category_id=p['category_id'])
        #     db.session.add(prod)
        #
        # db.session.commit()

        ipad_products = Product.query.filter(Product.name.startswith("iPhone")).all()
        print([p.name for p in ipad_products])
        price_filtered_products = Product.query.filter(
            Product.price.__gt__(15),
            Product.price.__lt__(37000000)
        ).order_by(Product.id).all()
        print([p.name for p in price_filtered_products])


