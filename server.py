# Sqlite3 has Connection class
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from linkedlist import LinkedList
from hashtable import HashTable
from binarysearchtree import BinarySearchTree
import random

# configure sqlite3 to enforce foreign key constraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

app.app_context().push()
db = SQLAlchemy()
db.init_app(app)

now = datetime.now()

# Models

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    posts = db.relationship("BlogPost", cascade='all, delete')

class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(500git))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name = data['name'],
        email = data['email'],
        address = data['address'],
        phone = data['phone']
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': "Sucesss"}), 200

@app.route("/user/asc", methods=["GET"])
def get_user_in_asc():
    users  = User.query.all()
    ll = LinkedList()
    for user in users:
        ll.insert_at_end({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'address': user.address
        })
    return jsonify(ll.to_list()), 200

@app.route("/user/desc", methods=["GET"])
def get_user_in_desc():
    users = User.query.all()
    ll = LinkedList()
    for user in users:
        ll.insert_at_beg({
            'id': user.id,
            'name':user.name,
            'email': user.email,
            'address': user.address
        })
        
    return jsonify(ll.to_list()), 200

@app.route("/user/<int:user_id>", methods=["GET"])
def get_one_user(user_id):
    users = User.query.all()
    ll = LinkedList()
    for user in users:
        ll.insert_at_beg({
            'id': user.id,
            'name':user.name,
            'email': user.email,
            'address': user.address
        })
    
    get_user = ll.get_user_by_id(user_id)
    return jsonify(get_user), 200

@app.route("/user/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({}), 200

@app.route("/blogs/create/<user_id>", methods=["POST"])
def create_blog(user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "user doesn't exist"}), 400
    ht = HashTable(10)
    ht.add_key_value("id", data['id'])
    ht.add_key_value("title", data['title'])
    ht.add_key_value("body", data['body'])
    ht.add_key_value('date', now)
    ht.add_key_value('user_id', user_id)

    new_blog_post = BlogPost(
        title = ht.get_value('title'),
        body = ht.get_value('body'),
        date = ht.get_value('date'),
        user_id = ht.get_value('user_id')
    )    
    db.session.add(new_blog_post)
    db.session.commit()
    # ht.print_table()
    return jsonify({"message": "sucessfully created"}), 200
        
@app.route("/blogs/search/<blog_post_id>", methods=['GET'])
def get_blog_post(blog_post_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)
    bst = BinarySearchTree()
    
    for post in blog_posts:
        bst.insert({
                'id': post.id,
                'title': post.title,
                'body': post.body,
                'user_id': post.user_id,
            })
    
    post = bst.search(blog_post_id)

    if not post:
        return jsonify({"message":"Post Not Found"}), 400
    
    return jsonify(post), 200

if __name__ == "__main__":
    app.run(debug=True, port=3000)