#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, render_template, jsonify
from MyQR import myqr
import tempfile
import shutil


# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, template_folder='views')

# Set the app secret key from the secret environment variables.
app.secret = os.environ.get('SECRET')


def create_qr(id, amount=None):
    upi_id = id
    save_dir = tempfile.gettempdir()
    if amount:
        try:
            amount = round(float(amount), 2)
            url = f"upi://pay?pn=UPAYI&pa={upi_id}&cu=INR&am={amount}"
        except Exception:
            amount = None
            url = f"upi://pay?pn=UPAYI&pa={upi_id}&cu=INR"
    else:
        url = f"upi://pay?pn=UPAYI&pa={upi_id}&cu=INR"

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
    link = "/static/"+id+"_qr.png"
    destination = os.getcwd()+link
    shutil.copyfile(save_dir+"/"+id+"_qr.png", destination)
    return link


@app.route('/<id>')
def payment(id):
    if '@' in id:
        """Displays the QR and Payment Info."""
        qr = create_qr(id)
        if qr:
            return render_template('home.html', id=id, qr=create_qr(id))
        else:
            return "Something went wrong!"
    else:
        return render_template("create.html")


@app.route('/')
def homepage():
    return render_template('create.html')


@app.route('/<id>/<amount>')
def amount_payment(id, amount):
    if '@' in id:
        """Displays the QR and Payment Info."""
        qr = create_qr(id, amount)
        try:
            amount = round(float(amount), 2)
        except Exception:
            amount = None
        if qr:
            return render_template('home.html', id=id, qr=create_qr(id, amount), amount=amount)
        else:
            return "Something went wrong!"
    else:
        return render_template("create.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=True)
