from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    expenses = db.relationship("Expense", backref="category", lazy=True, cascade="all, delete")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Expense(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    amount = db.Column(db.Float)
    expense_date = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id, ondelete="CASCADE"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "amount": self.amount,
            "expense_date": self.expense_date,
            "category_id": self.category_id
        }