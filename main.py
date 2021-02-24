import os
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from dotenv import load_dotenv


app = Flask(__name__)

# Environment Variables
MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")

# DataBase Config
app.config['SQLALCHEMY_DATABASE_URI']=f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



class Authors (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    specialisation = db.Column(db.String(50))
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, specialisation):
        self.name = name
        self.specialisation = specialisation
    
    def __repr__(self):
        return f'<author_id: {self.id}>'


db.create_all()

class AuthorsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Authors
        sqla_session = db.session
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    specialisation = fields.String(required=True)


@app.route('/')
def hello_world():
    return 'Hello, From Flask!'


@app.route('/authors', methods = ['GET'])
def get_authors():
    get_authors = Authors.query.all()
    author_schema = AuthorsSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors": authors}))


@app.route('/authors', methods = ['POST'])
def create_author():
    data = request.get_json()
    author_schema = AuthorsSchema()
    # Deserialize a data structure to an object 
    # defined by this Schema’s fields.
    author = author_schema.load(data)
    created_author = author_schema.dump(author.create())
    # author.create() creates the author on db using the schema
    # author_schema.dump turns object into python type 
    return make_response(jsonify({"author": created_author}),201)






if __name__ == '__main__':
    app.run()
