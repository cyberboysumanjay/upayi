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
        """Displays the QR and Payment Info."""
        qr = create_qr(id)
        if qr:
            return render_template('home.html',id=id,qr=create_qr(id))
        else:
            return "Something went wrong!"
    else:
        return render_template("create.html")
    

@app.route('/')
def homepage():
    return render_template('create.html')

@app.route('/<id>/<amount>')
def amount_payment(id,amount):
    if '@' in id:
        """Displays the QR and Payment Info."""
        qr = create_qr(id)
        try:
            amount = round(float(amount),2)
        except Exception:
            amount = None
        if qr:
            return render_template('home.html',id=id,qr=create_qr(id),amount=amount)
        else:
            return "Something went wrong!"
    else:
        return render_template("create.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,use_reloader=True)