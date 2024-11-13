from sqlalchemy import Integer, Column, String, Float, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from app import db, app
import hashlib
from enum import Enum as RoleEnum


class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100), nullable=True)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship("Product", backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(100), nullable=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        u = User(name="admin", username="admin", password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
                 avatar="https://res.cloudinary.com/dehkjrhjw/image/upload/v1730272749/cld-sample-4.jpg",
                 user_role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()
        # c1 = Category(name="Smartphone")
        # c2 = Category(name="Tablet")
        # c3 = Category(name="Desktop")
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        #
        # products = [{
        #     "id": 1,
        #     "name": "iPhone 7 Plus",
        #     "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #     "price": 17000000,
        #     "image": "https://res.cloudinary.com/dehkjrhjw/image/upload/v1730273590/iphone-7-plus-rose-gold_x1rryi.jpg",
        #     "category_id": 1
        # }, {
        #     "id": 2,
        #     "name": "iPad Pro 2020",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dehkjrhjw/image/upload/v1730278180/ipad_pro_11_2020_u8mr7f.webp",
        #     "category_id": 2
        # }, {
        #     "id": 3,
        #     "name": "Galaxy Note 10 Plus",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image": "https://res.cloudinary.com/dehkjrhjw/image/upload/v1730278216/note_10_plus_5g_tmlque.webp",
        #     "category_id": 1
        # }, {
        #     "id": 4,
        #     "name": "Galaxy Note 11 Plus",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image": "https://res.cloudinary.com/dehkjrhjw/image/upload/v1730278216/note_10_plus_5g_tmlque.webp",
        #     "category_id": 1
        # }, {
        #     "id": 5,
        #     "name": "Galaxy Note 20 Plus",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image": "https://res.cloudinary.com/dehkjrhjw/image/upload/v1730278216/note_10_plus_5g_tmlque.webp",
        #     "category_id": 1
        # }, {
        #     "id": 6,
        #     "name": "Galaxy Note 9 Plus",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image": "https://res.cloudinary.com/dehkjrhjw/image/upload/v1730278216/note_10_plus_5g_tmlque.webp",
        #     "category_id": 1
        # }, {
        #     "id": 7,
        #     "name": "Galaxy Note 9 Plus",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image": "https://res.cloudinary.com/dehkjrhjw/image/upload/v1730278216/note_10_plus_5g_tmlque.webp",
        #     "category_id": 1
        # }]
        #
        # for p in products:
        #     p = Product(**p)
        #     db.session.add(p)
        #
        # db.session.commit()
