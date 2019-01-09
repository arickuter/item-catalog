from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Categories, Items, Base
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from apiclient import discovery
import httplib2
from oauth2client import client

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db', pool_pre_ping=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def catalogHome():
    session = DBSession()
    category = session.query(Categories).all()
    item = session.query(Items).all()
    return render_template('home.html', category=category, item=item)


@app.route('/catalog/<category_name>/items')
def catalogDisplay(category_name):
    session = DBSession()
    categoryDisplay = session.query(
        Categories).filter_by(name=category_name).one()
    category = session.query(Categories).all()
    item = session.query(Items).all()
    return render_template('category.html', category=category, item=item, categoryDisplay=categoryDisplay)


@app.route('/catalog/<category_name>/<item_name>')
def descriptionDisplay(category_name, item_name):
    session = DBSession()
    categoryDisplay = session.query(
        Categories).filter_by(name=category_name).one()
    item = session.query(Items).filter_by(title=item_name).one()
    return render_template('description.html', categoryDisplay=categoryDisplay, item=item)

# (Receive auth_code by HTTPS POST)


@app.route('/login', methods=['POST'])
def login():
    # If this request does not have `X-Requested-With` header, this could be a CSRF
    if not request.headers.get('X-Requested-With'):
        abort(403)

    # Set path to the Web application client_secret_*.json file you downloaded from the
    # Google API Console: https://console.developers.google.com/apis/credentials
    CLIENT_SECRET_FILE = 'client_secret.json'

    auth_code = request.data

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
        auth_code)

    # Get profile info from ID token
    userid = credentials.id_token['sub']
    email = credentials.id_token['email']
    return catalogHome()


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
