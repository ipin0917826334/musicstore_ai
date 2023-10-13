from flask import Flask, request, jsonify, send_from_directory
# from flask_mysqldb import MySQL
from flask_pymongo import PyMongo
import requests
from io import BytesIO
import os
import tensorflow as tf
from pymongo import MongoClient

# client = MongoClient("mongodb+srv://pea458:Asd04140@schoolservice.le9s1ov.mongodb.net/?retryWrites=true&w=majority")
# db = client.test  # replace 'test' with your database name
# print(db.command("ping"))
# Load the trained model
loaded_model = tf.keras.models.load_model("bank_slip_classifier.h5")

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://pea458:Asd04140@schoolservice.le9s1ov.mongodb.net/musicstore?retryWrites=true&w=majority/"  # MongoDB connection string
mongo = PyMongo(app)

# Database configuration
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''  # replace with your MySQL password
# app.config['MYSQL_DB'] = 'musicstore'

# mysql = MySQL(app)


def predict_bank_slip(img_stream, model):
    from tensorflow.keras.preprocessing.image import load_img, img_to_array
    import numpy as np

    img = load_img(img_stream, target_size=(128, 128))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255.
    result = model.predict(x)
    if result[0][0] > 0.5:
        return "ตรวจสอบสลิปสําเร็จ."
    else:
        return "ตรวจสอบไม่สําเร็จ."

@app.route('/')
def hello():
    return "Hello Flask-Heroku"
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    image_url = data.get('imageurl', None)
    print(image_url)
    if not image_url:
        return jsonify(error="No imageURL provided"), 400

    try:
        response = requests.get(image_url)
        image_stream = BytesIO(response.content)
        result = predict_bank_slip(image_stream, loaded_model)
        print(result)
        flextemplate = {
      "type": "bubble",
      "size": "giga",
      "hero": {
        "type": "image",
        "url": "https://us.123rf.com/450wm/johan2011/johan20111205/johan2011120500048/13710726-marca-de-verificaci%C3%B3n-verde-en-el-fondo-blancoo.jpg?ver=6",  # provide a default image url if 'image' key is not found
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "1:1",
        # "action": {
        #   "type": "message",
        #   "label": "action",
        #   "text": result.get('name', 'No name')
        # }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": result,
            "weight": "bold",
            "size": "lg",
            "wrap": True,
            "margin": "none",
            "contents": []
          },
        ],
        "spacing": "none",
        "paddingAll": "sm"
      }
    }
        return jsonify(flextemplate)
        # return jsonify({"predict":[result]})
    except Exception as e:
        return jsonify(error=f"An error occurred: {str(e)}"), 500
    
# @app.route('/instruments', methods=['POST'])
# def add_instrument():
#     data = request.json
#     cursor = mysql.connection.cursor()
#     cursor.execute("INSERT INTO instruments (name, band, type, price, usefor, image) VALUES (%s, %s, %s, %s, %s, %s)",
#                    (data['name'], data['band'], data['type'], data['price'], data['usefor'], data['image']))
#     mysql.connection.commit()
#     return jsonify(id=cursor.lastrowid, **data)


# @app.route('/search/type', methods=['POST'])
# def search_by_type():
#     data = request.json
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM instruments WHERE type = %s", [data['type']])
#     results = cursor.fetchall()
#     return jsonify(results)


# @app.route('/search/band', methods=['POST'])
# def search_by_band():
#     data = request.json
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM instruments WHERE band = %s", [data['band']])
#     results = cursor.fetchall()
#     return jsonify(results)


# @app.route('/instruments', methods=['GET'])
# def fetch_all_instruments():
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM instruments")
#     results = cursor.fetchall()
#     return jsonify(results)


# @app.route('/instruments/<usefor>', methods=['GET'])
# def fetch_instruments_by_use(usefor):
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM instruments WHERE usefor = %s", [usefor])
#     results = cursor.fetchall()
#     return jsonify(results)
   
# @app.route('/instruments', methods=['POST'])
# def add_instrument():
#     data = request.json
#     result = mongo.db.instruments.insert_one(data)
#     return jsonify(id=str(result.inserted_id), **data)

@app.route('/search/type', methods=['POST'])
def search_by_type():
    data_type = request.json.get('type')
    results = list(mongo.db.instruments.find({"type": data_type}))
    return jsonify(results)

@app.route('/search/band', methods=['POST'])
def search_by_band():
    band = request.json.get('band')
    results = list(mongo.db.instruments.find({"band": band}))
    return jsonify(results)

@app.route('/instruments', methods=['GET'])
def fetch_all_instruments():
    result = mongo.db.instruments.find_one()


    flextemplate = {
      "type": "bubble",
      "size": "nano",
      "hero": {
        "type": "image",
        "url": result.get('image', 'default_image_url'),  # provide a default image url if 'image' key is not found
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213",
        "action": {
          "type": "message",
          "label": "action",
          "text": result.get('name', 'No name')
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": result.get('name', 'No name'),
            "weight": "regular",
            "size": "xxs",
            "wrap": True,
            "margin": "none",
            "contents": []
          },
          {
            "type": "text",
            "text": f"{result.get('price', '0')} บาท",
            "size": "xxs"
          }
        ],
        "spacing": "none",
        "paddingAll": "sm"
      }
    }
    return jsonify({"res":flextemplate})
    

@app.route('/instruments/<usefor>', methods=['GET'])
def fetch_instruments_by_use(usefor):
    results = list(mongo.db.instruments.find({"usefor": usefor}))
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=False)
