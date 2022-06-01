#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, send_file, render_template
from MyQR import myqr
import tempfile

# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, template_folder='views', static_folder='/tmp/')

# Set the app secret key from the secret environment variables.
app.secret = os.environ.get('SECRET')


@app.route('/qr/<id>/<amount>')
def serve_qr(id, amount):
    return send_file(create_qr(id, amount), mimetype='image/png')


@app.route('/css')
def serve_css():  # Workaround as static file is routed to tmp folder
    return send_file('static/css/style.css', mimetype='text/css')


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
    return save_dir + "/" + id+"_qr.png"


@app.route('/<id>')
def payment(id):
    if '@' in id:
        """Displays the QR and Payment Info."""
        return render_template('home.html', id=id, amount=None)
    else:
        return render_template("create.html", id=id, amount=None)


@app.route('/')
def homepage():
    return render_template('create.html')


@app.route('/<id>/<amount>')
def amount_payment(id, amount):
    if '@' in id:
        """Displays the QR and Payment Info."""
        try:
            amount = round(float(amount), 2)
        except Exception:
            amount = None
        return render_template('home.html', id=id, amount=amount)
    else:
        return render_template("create.html", id=id, amount=amount)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=True)
