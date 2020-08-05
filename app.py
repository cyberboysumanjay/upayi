#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, render_template, jsonify
from MyQR import myqr
import requests
import tempfile


# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, template_folder='views')

# Set the app secret key from the secret environment variables.
app.secret = os.environ.get('SECRET')


def telegraph(filename):
    try:
        with open(filename, 'rb') as f:
            path=(
              requests.post(
                  'https://telegra.ph/upload',
                  files={'file': ('file', f, 'image/jpeg')}  # image/gif, image/jpeg, image/jpg, image/png, video/mp4
              )
            ).json()[0]['src']
        return('https://telegra.ph{}'.format(path))
    except Exception:
        return None
    finally:
        try:
            os.remove(filename)
        except:
            pass

def create_qr(id):
    upi_id = id
    save_dir = tempfile.gettempdir()
    url=f"upi://pay?pn=UPAYI&pa={upi_id}&cu=INR"
    version, level, qr_name = myqr.run(
        url,
        version=1,
        level='H',
        picture="logo.jpg",
        colorized=False,
        contrast=1.0,
        brightness=1.0,
        save_name=id+"_qr.png",
        save_dir=save_dir
    )
    link = telegraph(save_dir+"/"+id+"_qr.png")
    return link

@app.route('/<id>')
def payment(id):
    if '@' in id:
        base_url = "https://upayi.me/"
        """Displays the QR and Payment Info."""
        return render_template('index.html',id=id,qr=create_qr(id),base_url=base_url)
    else:
        return "Invalid UPI ID"
    
@app.route('/')
def homepage():
    """Displays the homepage."""
    id='sumanjay@pnb'
    return render_template('index.html',id=id,qr=create_qr(id),base_url="https://upayi.me/")
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,use_reloader=True)