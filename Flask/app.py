from flask import Flask, render_template, request, jsonify, send_file,url_for,redirect
import base64
from io import BytesIO
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import tensorflow as tp
import keras
import pickle
import cv2
import pymysql
import warnings
warnings.filterwarnings("ignore")
import io
from x import pred
func = pred()
app = Flask(__name__)

map = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
       'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
       'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
        'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'd', 'e', 
        'f', 'g', 'h', 'n', 'q', 'r', 't']

UPLOAD_TO = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_TO
model=keras.models.load_model("model.h5")


def predict(path):
    img_array = cv2.imread(path)
    #os.remove(path)
    new_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    new_array = cv2.resize(new_array, (28,28))
    new_array=new_array.reshape(1,28,28,1)
    pred = model.predict(new_array)
    number_code = np.argmax(pred[0])
    prediction = map[number_code]
    return prediction

def verify(username,password):
            conn = pymysql.connect(host='localhost',port=3306, user='root' , password='root',db='app')
            cur = conn.cursor()
            cur.execute(f'Select password from data where username = "{username}";')
            data=cur.fetchall()
            if(len(data)==1 and data[0][0]==password):
                  return True
            else:
                  return False

def create(username,email,password):
            conn = pymysql.connect(host='localhost',port=3306, user='root' , password='root',db='app')
            cur = conn.cursor()
            cur.execute(f'Select password from data where username = "{username}";')
            data=cur.fetchall()
            if(len(data)==0):
                cur.execute(f'INSERT into data values("{username}","{email}","{password}");')
                conn.commit()
                return True
            else:
                return False


@app.route('/',methods=['POST','GET'])
def index():
    return render_template('login.html')

@app.route('/doodle',methods=['POST','GET'])
def doodle():
      return render_template('welcome.html')

@app.route('/anime',methods=['POST','GET'])
def anime():
      return render_template('anime.html')
global a
a=""
@app.route('/data',methods=['POST','GET'])
def data():
        global a
        if(request.method=='GET'):
              return render_template("anime.html",anime=a)
        else:
            xa = request.form["name"]
            print(xa)
            a = func.recommend(str(xa))
            
        return render_template("anime.html",anime=a)

      

@app.route('/signin',methods=["POST","GET"])
def signin():
      name=request.form["username"]
      password=request.form["password"]
      if(verify(name,password)):
            return render_template('domain.html')  
      else:
            return render_template("login.html",message="Invalid login")
      
@app.route('/signup',methods=['POST'])
def signup():
       name=request.form["username"]
       password=request.form["password"]
       email=request.form["email"]
       if(create(name,email,password)):
             return render_template('login.html',message="created successfully")
       else:
             return render_template('login.html',message="Account already exists")
global p
p=""
@app.route('/canvas', methods=['POST','GET'])
def canvas():
    global p
    if(request.method=='GET'):
          if(p==str('j') or p==""):
                return render_template('canvas.html',pred=("Please Draw & Upload"))
          m=p
          p=""
          return render_template('canvas.html',pred=("you drew a "+m))
    
    else:
            data_url = request.form['imageBase64']
            img_bytes = base64.b64decode(data_url.split(',')[1])
            filename = secure_filename('image.png')
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            with open(path, 'wb') as f:
                f.write(img_bytes)
            
            prediction = predict(path)
            p = prediction
            print(p)        
            
    return render_template('canvas.html',pred=p)
        
        