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

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

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


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
