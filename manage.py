from flask import Flask,Response,send_file, render_template, url_for, send_from_directory,request,flash,redirect,make_response
from werkzeug.utils import secure_filename
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from style_transfer import *
from PIL import Image
import numpy as np
import uuid
import base64
import random
import os
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = '9881522bx4b16xr086p2dgde210wa328'

app.config['UPLOAD_FOLDER'] = "UPLOAD_FOLDER"

@app.route('/')
def home():
    return render_template('index.html')

def serve_pil_image(pil_img):
    img_io = io.BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'bmp','jpg', 'jpeg','png'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/generate', methods=['GET','POST'])
def generate():
    return render_template('picture.html')

@app.route('/gallery', methods=['GET','POST'])
def gallery():
    imgs =os.listdir("static/generated")
    print(imgs)    
    return render_template('gallery.html',imgs=imgs)

@app.route('/styles')
def styles():

    return render_template('styles.html')


@app.route('/upload_cam', methods=['GET','POST'])
def upload_cam(stylized=None):
    if request.method == 'POST':      
        imagefile = request.form['file']
        b = str.encode(imagefile)
        z = b[b.find(b'/9'):]
        im = Image.open(io.BytesIO(base64.b64decode(z)))#.save('UPLOAD_FOLDER/captured.jpg')
        img = np.array(im) 
        # Convert RGB to BGR 
        img = img[:, :, ::-1].copy() 
        sytles_fldr = os.path.join(os.getcwd(),'static','sytles')
        styles_imgs = os.listdir(sytles_fldr)
        styles = [load_img(os.path.join(os.getcwd(),'static','sytles',x)) for x in styles_imgs]

        style = random.choice(styles)
        stylized = generate_stylezed(img,style)
        uuidOne = uuid.uuid1()
        stylized.save("static/generated/{}.png".format(uuidOne))
        #return redirect("generated/static/{}.png")
        return redirect(url_for('gallery'))
    else:
        return redirect(url_for('gallery'))
@app.route('/download')
def download():
    uuid= (request.args['uuid'])
    im = Image.open("static/{}.png".format(uuid))
    return "hola"#serve_pil_image(stylized)

if __name__ == '__main__':
    app.run()