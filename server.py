from flask import Flask, render_template
import socketio
import eventlet
import os
import time

from flask import Flask, render_template


import requests
import json 

image_file = "/Users/timotius02/Downloads/photo.png"



#print(res)
    
sio = socketio.Server()
app = Flask(__name__, static_folder='web', template_folder='web')


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/start', methods=['GET'])
def start():
    print("Starting")
    sio.emit("take_picture")
    return "ok"
@app.route('/score', methods=['GET'])
def score():
    print("Post Starting")
    data = open(image_file, 'rb').read()
    payload = {'api_key':'wnKWg4_2ySRuh2i1mBJMMNj6vqMo78__', 'api_secret':'P5Y_Lgf2HIXpOhEtDAKBdIGLcY5FvFrb', 'return_attributes':'beauty'}
    r = requests.post("https://api-us.faceplusplus.com/facepp/v3/detect", params=payload, files=dict(image_file=data))
    print("Post post")
    j = json.loads(r.text)
    if (r.status_code == 200):
        if len(j['faces']) > 0:
            score = round(max(j['faces'][0]['attributes']['beauty']['female_score'], j['faces'][0]['attributes']['beauty']['male_score']))
            res = '{"score": ' + str(score) + '}'
        else:
            res = '{"error": "Oh look it\'s John Cena!"}'
    else:
        error = '{"error": "' + j['error_message'] + '"}'
        res  = error
    os.remove("/Users/timotius02/Downloads/photo.png")
    print(res)
    return res


@sio.on('connect', namespace='/server')
def connect(sid, environ):
    print("connect ", sid)



@sio.on('disconnect', namespace='/server')
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
