from multiprocessing.sharedctypes import Value
from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
from flask_paginate import Pagination, get_page_parameter

import pandas as pd
import mysql.connector

app = Flask(__name__,template_folder='templates')

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


# Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="review_product"
)

mycursor = mydb.cursor()

# Root URL
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datatraining')
def data():
  return render_template('data.html')


# Get the uploaded files
@app.route("/datatraining", methods=['POST'])
def uploadFiles():
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
           uploaded_file.save(file_path)
           parseCSV(file_path)
      return redirect(url_for('data'))

def parseCSV(filePath):
      col_names = ['category','review_title','review_content', 'rating']
      csvData = pd.read_csv(filePath,names=col_names, header=None)
      for i,row in csvData.iterrows():
             sql = "INSERT INTO review_ebay (category, review_title, review_content, rating) VALUES (%s, %s, %s, %s)"
             value = (row['category'],row['review_title'],row['review_content'],row['rating'])
             mycursor.execute(sql, value)
             mydb.commit()
             print(i,row['category'],row['review_title'],row['review_content'],row['rating'])

@app.route("/listreview/<int:page>")
def readData(page = 1):
    perpage = 20
    startat = page * perpage
    page = request.args.get(get_page_parameter(), type=int, default=1)
    mycursor = mydb.cursor()
    mycursor.execute("select * from review_ebay")
    data = mycursor.fetchall()
    pagination = Pagination(
        page=page, 
        total=len(data)
    )
    return render_template(
        'list.html', 
        value=data,
        pagination=pagination)


if (__name__ == "__main__"):
     app.run(debug=True)
