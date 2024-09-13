import datetime

from app import app, request, db
from flask import jsonify
from models import User, Category, Expense
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from decimal import Decimal
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


@app.route('/register', methods=["POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        if db.session.execute(db.select(User).where(User.username == data["username"])).scalar():
            return {
                "msg": "User already exists"
            }, 400
        user = User()
        user.username = data["username"]
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 200


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        user = db.session.execute(db.select(User).where(User.username == data["username"])).scalar()
        if not user:
            return {
                "msg": "User not found"
            }, 400
        if not user.check_password(data["password"]):
            return {
                "msg": "Wrong password"
            }, 400
        access_token = create_access_token(identity=user.username)
        return jsonify({"access_token": access_token})


@app.route("/categories", methods=["POST", "GET"])
@jwt_required()
def category_api():
    username = get_jwt_identity()
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()

    if not user:
        return jsonify({
            "error": "User doesn't exist"
        }), 400
    if request.method == "POST":
        data = request.get_json()
        category = Category()
        category.name = data["name"]
        db.session.add(category)
        db.session.commit()
        return jsonify(category.serialize()), 200
    if request.method == "GET":
        categories_query = Category.query
        if "name" in request.args:
            categories_query = categories_query.filter_by(name=request.args["name"])
        page = request.args.get('page', 1, type=int)
        categories = categories_query.order_by(Category.name.asc()).paginate(page=page, per_page=100)
        return jsonify([category.serialize() for category in categories]), 200


@app.route("/expenses", methods=["POST", "GET"])
@jwt_required()
def expenses_api():
    username = get_jwt_identity()
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if not user:
        return jsonify({
            "error": "User doesn't exist"
        }), 400
    if request.method == "POST":
        data = request.get_json()
        expense = Expense()
        expense.description = data["description"]
        expense.amount = Decimal(data["amount"])
        expense.expense_date = parse(data["expense_date"])
        expense.category_id = data["category_id"]
        db.session.add(expense)
        db.session.commit()
        return jsonify(expense.serialize()), 200
    if request.method == "GET":
        expenses_query = Expense.query
        if "type" in request.args:
            if request.args["type"] == "past_week":
                end_date = datetime.datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.datetime.now() - relativedelta(weeks=1)).strftime("%Y-%m-%d")
                expenses_query = expenses_query.filter(Expense.expense_date.between(start_date, end_date))
            if request.args["type"] == "past_month":
                end_date = datetime.datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.datetime.now() - relativedelta(months=1)).strftime("%Y-%m-%d")
                expenses_query = expenses_query.filter(Expense.expense_date.between(start_date, end_date))
            if request.args["type"] == "last_3_months":
                end_date = datetime.datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.datetime.now() - relativedelta(months=3)).strftime("%Y-%m-%d")
                expenses_query = expenses_query.filter(Expense.expense_date.between(start_date, end_date))
        if "start_date" in request.args:
            expenses_query = expenses_query.filter(Expense.expense_date >= request.args["start_date"])
        if "end_date" in request.args:
            expenses_query = expenses_query.filter(Expense.expense_date <= request.args["end_date"])
        if "category_id" in request.args:
            expenses_query = expenses_query.filter(Expense.category_id == request.args["category_id"])
        page = request.args.get('page', 1, type=int)
        expenses = expenses_query.order_by(Expense.expense_date.desc()).paginate(page=page, per_page=100)
        return jsonify([expense.serialize() for expense in expenses]), 200


@app.route("/expenses/<id>", methods=["DELETE", "PUT", "PATCH", "GET"])
@jwt_required()
def expense_api(id):
    if request.method == "DELETE":
        expense = Expense.query.filter(Expense.id == id).one_or_none()
        db.session.delete(expense)
        db.session.commit()
        return jsonify({}),204
    if request.method == "PUT":

        data = request.get_json()
        expense = Expense.query.filter(Expense.id == id).one_or_none()
        if not expense:
            return jsonify({"msg": "Expense not found"}), 404

        description = data.get("description")
        if not description:
            return jsonify({"msg": "Missing description"}), 400
        if not data.get("amount"):
            return jsonify({"msg": "Missing amount"}), 400
        amount = Decimal(data.get("amount"))
        if not data.get("expense_date"):
            return jsonify({"msg": "Missing expense_date"}), 400
        expense_date = parse(data.get("expense_date"))
        category_id = data.get("category_id")
        if not data.get("category_id"):
            return jsonify({"msg": "Missing category_id"}), 400
        Expense.query.filter(Expense.id == id).update({
            "amount": amount,
            "description": description,
            "expense_date": expense_date,
            "category_id": category_id
        })
        db.session.commit()

        return jsonify(data), 200
    if request.method == "PATCH":
        data = request.get_json()
        expense = Expense.query.filter(Expense.id == id).one_or_none()
        if not expense:
            return jsonify({"error": "Expense doesn't exists"}), 404

        if data.get("amount"):
            data["amount"] = Decimal(data.get("amount"))
        if data.get("expense_date"):
            data["expense_date"] = parse(data.get("expense_date"))

        Expense.query.filter(Expense.id == id).update(data)
        db.session.commit()
        return jsonify(data), 200
    if request.method == "GET":
        expense = Expense.query.filter(Expense.id == id).one_or_none()
        if not expense:
            return jsonify({"msg": "Expense not found"}), 404
        return jsonify(expense.serialize()), 200