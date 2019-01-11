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

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Aric's Catalog App"

# Connect to Database and create database session
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


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['email']
    login_session['picture'] = data['picture']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/')
def catalogHome():
    session = DBSession()
    category = session.query(Categories).all()
    item = session.query(Items).all()
    newitem = list(reversed(item))
    del newitem[9:]
    if 'username' not in login_session:
        loggedIn = False
        return render_template('home.html', category=category, item=newitem, loggedIn=loggedIn)
    else:
        loggedIn = True
        userUsername = login_session['username']
        return render_template('home.html', category=category, item=newitem, loggedIn=loggedIn, userUsername=userUsername)


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['picture']
        flash('You were successfully logged out')
        return redirect(url_for('catalogHome'))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/catalog/<category_name>/items')
def catalogDisplay(category_name):
    session = DBSession()
    categoryDisplay = session.query(
        Categories).filter_by(name=category_name).one()
    category = session.query(Categories).all()
    item = session.query(Items).all()
    if 'username' in login_session:
        userUsername = login_session['username']
        return render_template('category.html', loggedIn=True, category=category, item=item, categoryDisplay=categoryDisplay, userUsername=userUsername)
    else:
        return render_template('category.html', category=category, item=item, categoryDisplay=categoryDisplay)


@app.route('/catalog/<category_name>/<item_name>')
def descriptionDisplay(category_name, item_name):
    session = DBSession()
    categoryDisplay = session.query(
        Categories).filter_by(name=category_name).one()
    item = session.query(Items).filter_by(title=item_name).one()
    if 'username' in login_session:
        userUsername = login_session['username']
        return render_template('description.html', loggedIn=True, categoryDisplay=categoryDisplay, item=item, userUsername=userUsername)
    else:
        return render_template('description.html', categoryDisplay=categoryDisplay, item=item)


@app.route('/add', methods=['GET', 'POST'])
def addItem():
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    else:
        if request.method == 'POST':
            newItem = Items(
                title=request.form['title'], description=request.form['description'], cat_id=request.form['catId'])
            session.add(newItem)
            session.commit()
            flash('New item created!')
            return redirect('/')
        else:
            userUsername = login_session['username']
            return render_template('add.html', userUsername=userUsername, loggedIn=True)


@app.route('/catalog/<item_title>/edit/', methods=['GET', 'POST'])
def editItem(item_title):
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    else:
        if request.method == 'POST':
            editedItem = session.query(Items).filter_by(title=item_title).one()
            editedItem.title = request.form['title']
            editedItem.description = request.form['description']
            editedItem.cat_id = request.form['catId']
            session.add(editedItem)
            session.commit()
            flash('Item edited successfully!')
            return redirect(url_for('catalogHome'))
        else:
            item = session.query(Items).filter_by(title=item_title).one()
            userUsername = login_session['username']
            return render_template('edit.html', userUsername=userUsername, loggedIn=True, item=item)


@app.route('/catalog/<item_title>/delete/', methods=['GET', 'POST'])
def deleteItem(item_title):
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    else:
        deleteItem = session.query(Items).filter_by(title=item_title).one()
        if request.method == 'POST':
            session.delete(deleteItem)
            session.commit()
            flash('Item deleted successfully!')
            return redirect(url_for('catalogHome'))
        else:
            item = session.query(Items).filter_by(title=item_title).one()
            userUsername = login_session['username']
            return render_template('delete.html', userUsername=userUsername, loggedIn=True, item=item)


@app.route('/catalog.json', methods=['GET'])
def catalogJSON():
    session = DBSession()
    category = session.query(Categories).all()
    items = session.query(Items).all()
    return jsonify(Category=[i.serialize for i in category], Items=[i.serialize for i in items])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
