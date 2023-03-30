from flask import Flask, jsonify, json, render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
import sqlite3




app = Flask(__name__)


app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Vendor(db.Model):
    Vendor_Id = db.Column(db.Integer, primary_key=True)
    Vendor_Name = db.Column(db.String(20),nullable=False,unique=True)
    Description = db.Column(db.String(100))
    items = db.relationship('Items',backref='user')

class Items(db.Model):
    Item_Id = db.Column(db.Integer, primary_key=True)
    Vendor_Id = db.Column(db.Integer, db.ForeignKey('vendor.Vendor_Id'))
    Item_Name = db.Column(db.String(50))
    Description = db.Column(db.String(100))
    Quantity = db.Column(db.Integer)




def add_vendor(id, name, description):
    new_vendor = Vendor(Vendor_Id=id, Vendor_Name=name, Description=description)
    db.session.add(new_vendor)
    db.session.commit()


def add_items(vendor_id, name, description, qty):
    new_item = Items(Vendor_Id=vendor_id, Item_Name=name, Description=description, Quantity=qty)
    db.session.add(new_item)
    db.session.commit()



# @app.route('/')
# def home():
#     vendor_id = 4
#     name = 'Sport Shoes'
#     description = 'For Football Boots, Running Shoes, Canva Shoes'
#     qty = 300
#     add_items(vendor_id, name,description, qty)

#     return 'Added Sucessfully'


@app.route('/vendor')
def vendor():
    con = sqlite3.connect('instance/database.db')
    cursor = con.cursor()
    cursor.execute('select Vendor_Id, Vendor_Name from Vendor')
    data = cursor.fetchall()
    Vendor_data=[]
    for i in data:
        dict_data ={}
        dict_data['id'] = i[0]
        dict_data['name'] = i[1]
        Vendor_data.append(dict_data)

    return Vendor_data



@app.route('/items', methods=['POST'])
def items():
    vendor_id = request.get_json(force=True)
    vendor_id = str(vendor_id)
    con = sqlite3.connect('instance/database.db')
    cursor = con.cursor()
    cursor.execute('select Item_Id, Item_Name from Items where Vendor_Id='+vendor_id)
    data = cursor.fetchall()
    Item_data=[]
    for i in data:
        dict_data ={}
        dict_data['id'] = i[0]
        dict_data['name'] = i[1]
        Item_data.append(dict_data)

    return Item_data


@app.route('/stock', methods=['POST'])
def stock():
    item_list = request.get_json()
    con = sqlite3.connect('instance/database.db')
    cursor = con.cursor()
    unavilable_items = []
    for item in item_list:
        id = str(item['id'])
        qty = str(item['qty'])
        cursor.execute('select Item_Name, Quantity from Items where Item_Id='+ id +' and Quantity<'+qty)
        data = cursor.fetchall()
        for i in data:
            dict_data = {}
            dict_data['name'] = i[0]
            dict_data['qty'] = i[1]
            unavilable_items.append(dict_data)
    print(unavilable_items)
    return jsonify(unavilable_items)


if __name__ == "__main__":
    # app.run(debug = True)
    app.run(host='192.168.143.85', debug = True)

