import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key="hello"
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:uranium238@localhost/finance"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    cost = db.Column(db.Numeric(15,2))

    def __init__(self,name,cost):
        self.name = name
        self.cost = cost

class Person(db.Model):
    user_id = db.Column(db.Numeric(),primary_key=True)
    email = db.Column(db.String)
    password=db.Column(db.String)

    def __init__(self,email,password):
        self.email=email
        self.password=password

with app.app_context():
    db.create_all()
    print()
    db.session.commit()

@app.route('/login',methods=['GET'])
def create_user():
    mail=request.args['email']
    password=request.args['password']

    k=Person.query.filter_by(email=mail).all()
    print(k)
    
    if len(k)==0:
        user=Person(mail,password)
        db.session.add(user)
        db.session.commit()
        return "200 OK"
    else:
        return "404"

    


@app.route('/api',methods=['GET'])
def add():
    d={}
    cost = float(request.args["cost"])
    name= request.args["name"]
    d["cost"]=cost
    d['name']=name
    item=Item(name,cost)
    db.session.add(item)
    db.session.commit()
    print("Item stored:")
    print(cost,name)
    return jsonify(d)


@app.route('/api/drop',methods=['GET'])
def drop():
    name= request.args["name"]


    return name,cost#jsonify(d)

if __name__ == '__main__':
    app.run()
