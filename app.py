from email.policy import default
from urllib import request
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    priceHistory = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    # if(request.method == 'POST' or request.method == 'GET'):
    f = open("output.txt", "r")
    lines = f.readlines()
    for line in lines:
        name = line
        # name = f.readline()
        new_task = Product(name=name, url="", priceHistory="")
        try:
            db.session.add(new_task)
            db.session.commit()
            print("\nCommitted\n")
            tasks = Product.query.order_by(Product.date_created).all()
            return render_template('index.html', tasks = tasks)
            # return redirect('index.html', tasks=tasks)
        except Exception as e:
            return str(e)
        # return 'There was an issue adding the thing to the other thing'
    # else:
        # print("\nNOT POST!!!!!\n")
        # tasks = Product.query.order_by(Product.date_created).all()
        # return render_template('index.html', tasks = tasks)

if __name__ == "__main__":
    app.run(debug=True)