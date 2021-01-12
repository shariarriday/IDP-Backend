# flask_ngrok_example.py
import os
import shutil
import urllib.request
from flask import Flask, request, redirect, jsonify, send_from_directory
from flask_ngrok import run_with_ngrok
import time
import base64
from PIL import Image

UPLOAD_FOLDER = 'images'
DOWNLOAD_FOLDER = 'static'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024

run_with_ngrok(app)  # Start ngrok when app is run


@app.route("/" , methods=['GET' , 'POST'])
def hello():
    # delete folders
    if request.method != 'POST':
        os.system('start convert.bat')
        time.sleep(5)
        return send_from_directory(DOWNLOAD_FOLDER, 'result.mp3', as_attachment=True)
    
    try:
        shutil.rmtree(UPLOAD_FOLDER)
    except Exception as e:
        do = "nothing"
    try:
        shutil.rmtree(DOWNLOAD_FOLDER)
    except Exception as e:
        do = "nothing"

    # create empty output folders
    uncreated = 1
    while (uncreated):
        try:
            os.mkdir(UPLOAD_FOLDER)
            uncreated = 0
        except Exception as e:
            do = "nothing"
    uncreated = 1
    while (uncreated):
        try:
            os.mkdir(DOWNLOAD_FOLDER)
            uncreated = 0
        except Exception as e:
            do = "nothing"
            
    if request.method == 'POST':
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     resp = jsonify({'message' : 'No file part in the request'})
        #     resp.status_code = 400
        #     return resp
        file = request.form['basestring']
        
        if file == '':
            resp = jsonify({'message' : 'Empty Image'})
            resp.status_code = 400
            return resp
        else:
            imgdata = base64.b64decode(file)
            filename = UPLOAD_FOLDER+'/uploaded.jpg'  # I assume you have a way of picking unique filenames
            with open(filename, 'wb') as f:
                f.write(imgdata)         

            #read the image
            im = Image.open(UPLOAD_FOLDER+'/uploaded.jpg')
            #rotate image
            angle = 270
            out = im.rotate(angle , expand = True)
            out.save(UPLOAD_FOLDER+'/uploaded.jpg')

            resp = jsonify({'message' : 'File successfully uploaded'})
            resp.status_code = 201
            os.system('execution.bat')
            return "File Successfully Uploaded"
            #return send_from_directory(DOWNLOAD_FOLDER, 'result.wav', as_attachment=True)

if __name__ == '__main__':
    app.run()
