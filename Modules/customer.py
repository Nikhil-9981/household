from flask import Flask, redirect, render_template, request, jsonify
from flask import session
from flask import url_for
from functools import wraps
from model import *
import os

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('islogin',False) and session.get('type','')=='C':
            return f(*args, **kwargs)
        return redirect('/')
    return decorated_function


def index(app):
    @app.route('/customer')
    @login_required
    def sdash():
        return render_template('customer.html')
    
    @app.route('/customer/getdetails',methods=['GET'])
    def customgetdet():
        username = session['username']
        user = Users.query.filter_by(username=username).first()
        cuser = Customers.query.filter_by(UserID=user.ID).first()
        d = {column.name: getattr(user, column.name) for column in user.__table__.columns if column.name!="password"}
        d |= {column.name: getattr(cuser, column.name) for column in cuser.__table__.columns}
        directory = "static/images/Profile"
        files = [f for f in os.listdir(directory) if f.startswith(username+".")]
        if files:
            d["profilepic"] = directory+'/'+files[0]
        else:
            d["profilepic"] = directory+'/default.png'
        return jsonify(d)
