# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 19:23:34 2020
Project-Image Authentication Using Water Marking Technique
Section-Main
@author: RAVI
"""

from flask import Flask,render_template,request,url_for,redirect,flash
from flask_uploads import UploadSet,IMAGES
import os
import img_io as img
import key_io

app = Flask(__name__)

"""app configuration"""
app.config["UPLOADED_PHOTOS_DEST"]=r"C:\Users\RAVI\Desktop\I.A.W.T\image\upload"
app.config["WATERMARK_UPLOAD"]=r"C:\Users\RAVI\Desktop\I.A.W.T\image\watermark"
app.config["WATERMARKED_UPLOAD"]=r"C:\Users\RAVI\Desktop\I.A.W.T\image\watermarked"
app.config["ALLOWED_IMAGE_EXTENSIONS"]=["PNG","JPG","JPEG","GIF"]
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
ret_wm=r"C:\Users\RAVI\Desktop\I.A.W.T\image\watermark"

images=UploadSet("images",IMAGES)



@app.route("/", methods=["GET", "POST"])
def home():
   if request.method == "POST":
      if request.files:
         image = request.files["image_file"]
         watermark=None
         watermark=request.files["watermark_file"]
         image.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image.filename))
         watermark.save(os.path.join(app.config["WATERMARK_UPLOAD"], watermark.filename))
         key=request.form.get("key")
         if 'encrypt' in request.form:
             img.insert_lsb(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image.filename),os.path.join(app.config["WATERMARK_UPLOAD"], watermark.filename),os.path.join(app.config["WATERMARKED_UPLOAD"], image.filename),key)
             return render_template("index.html")
         if 'decrypt' in request.form:
             img.extract_lsb(os.path.join(app.config["WATERMARKED_UPLOAD"], image.filename),ret_wm,key)
             return render_template("index.html")
         



   return render_template("index.html")

@app.route("/encryptor", methods=["GET", "POST"])
def encryptor():
    if request.method == "POST":
      if request.files:
         image = request.files["image_file"]
         watermark=None
         watermark=request.files["watermark_file"]
         image.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image.filename))
         watermark.save(os.path.join(app.config["WATERMARK_UPLOAD"], watermark.filename))
         key=request.form.get("key")
         if 'encrypt' in request.form:
             img.insert_lsb(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image.filename),os.path.join(app.config["WATERMARK_UPLOAD"], watermark.filename),os.path.join(app.config["WATERMARKED_UPLOAD"], image.filename),key)
             return render_template("encryption.html")
         
    return render_template("encryption.html")


@app.route("/decryptor", methods=["GET", "POST"])
def decryptor():
    if request.method == "POST":
      if request.files:
         image = request.files["image_file"]
         image.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], image.filename))
         key=request.form.get("key")
         if 'decrypt' in request.form:
             img.extract_lsb(os.path.join(app.config["WATERMARKED_UPLOAD"], image.filename),ret_wm,key)
             return render_template("decryption.html")
    return render_template("decryption.html")

@app.route("/encryption_output", methods=["GET", "POST"])
def encryption_output():
    pass

@app.route("/decryption_output", methods=["GET", "POST"])
def decryption_output():
    pass



if __name__=="__main__":
    _host='127.0.0.1'
    _port=5000
    app.run(host=_host,port=_port,debug=True)
