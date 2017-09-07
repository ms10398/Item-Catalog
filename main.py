#!/usr/bin/python
# -*- coding: utf-8 -*-
# Importing dependencies for the project

from flask import Flask, render_template, request, redirect, url_for, \
    session, make_response, jsonify

import random
import string
from oauth2client.client import flow_from_clientsecrets, \
    FlowExchangeError, AccessTokenCredentials
import httplib2
import json
import requests

# Import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import DB Modules

from database_setup import Base, User, Genre, Movies

app = Flask(__name__)

# create engine connection with sql library

engine = create_engine('sqlite:///MovieDatabase.db')

# bind the engine with base class

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
sess = DBSession()

# Google Client ID.

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web'
                                                               ]['client_id']
APPLICATION_NAME = 'ItemCatalog'


# Helper Functions

def create_state():
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.digits) for x in xrange(32))
    session['state'] = state
    return state


def check_user():
    email = session['email']
    return sess.query(User).filter_by(email=email).one_or_none()


def add_user():
    user = User()
    user.name = session['name']
    user.email = session['email']
    user.url = session['img']
    user.provider = session['provider']
    sess.add(user)
    sess.commit()


# Routes for the application

@app.route('/')
def genreListView():

    # Get Handler for the Main Page

    genreList = sess.query(Genre).all()
    state = create_state()
    return render_template('genreList.html', genres=genreList,
                           state=state, error='')


@app.route('/new/', methods=['get', 'post'])
def newMovie():
    if request.method == 'POST':

        # Check if the request is post request or get.

        if 'provider' in session and session['provider'] != 'null':

            # Validates if user is logged or not.

            name = request.form['name']
            desc = request.form['desc']
            g_id = request.form['genre']

            # get the all variables from the post request.

            u_id = check_user().id
            if name and g_id:

                # Null/None Validation for name url and g_id.

                movie = Movies()
                movie.name = name
                movie.g_id = g_id
                movie.u_id = u_id
                if desc:

                    # Check if description is also posted.

                    movie.description = desc
                sess.add(movie)
                sess.commit()
                return redirect(url_for('genreView', gid=g_id))
            else:
                genreList = sess.query(Genre).all()
                state = create_state()
                return render_template('genreList.html',
                                       genres=genreList, state=state,
                                       error='Incomplete Fields')
        else:
            genreList = sess.query(Genre).all()
            state = create_state()
            return render_template('genreList.html', genres=genreList,
                                   state=state,
                                   error='User not Logged in.')

    if 'provider' in session and session['provider'] != 'null':

        # Validates if user is logged or not.

        genreList = sess.query(Genre).all()
        state = create_state()
        return render_template('newMovie.html', genres=genreList,
                               state=state)
    else:
        genreList = sess.query(Genre).all()
        state = create_state()
        return render_template('genreList.html', genres=genreList,
                               state=state, error='User not Logged in.')


@app.route('/genre/<int:gid>/')
def genreView(gid):

    # Get Handler for the Category Page.

    genre = sess.query(Genre).filter_by(id=gid).one()
    movieList = sess.query(Movies).filter_by(g_id=gid)
    state = create_state()
    return render_template('genre.html', movies=movieList, genre=genre,
                           state=state)


@app.route('/view/<int:g_id>/<int:m_id>')
def viewMovie(g_id, m_id):
    movie = sess.query(Movies).filter_by(id=m_id,
                                         g_id=g_id).one_or_none()
    if movie:

        # Check if movie exsists.

        state = create_state()
        return render_template('viewMovie.html', movie=movie,
                               state=state)
    else:
        genreList = sess.query(Genre).all()
        state = create_state()
        return render_template('genreList.html', genres=genreList,
                               state=state, error='Movie does not exist')


@app.route('/edit/<int:g_id>/<int:m_id>', methods=['get', 'post'])
def editMovie(g_id, m_id):
    if request.method == 'POST':

        # Check if the request is post request or get.

        if 'provider' in session and session['provider'] != 'null':

            # Validates if user is logged or not.

            name = request.form['name']
            desc = request.form['desc']
            gid = request.form['genre']
            u_id = check_user().id
            if name and gid:

                # Null/None Validation for name url and g_id.

                movie = sess.query(Movies).filter_by(id=m_id,
                                                     g_id=g_id).one_or_none()
                if movie:

                    # Check if movie exsists.

                    if movie.u_id == u_id:

                        # Validates movie ownership.

                        movie.name = name
                        movie.g_id = gid
                        if desc:

                            # Check if description is also posted.

                            movie.description = desc
                        sess.add(movie)
                        sess.commit()
                        return redirect(url_for('genreView', gid=gid))
                    else:
                        genreList = sess.query(Genre).all()
                        state = create_state()
                        return render_template('genreList.html',
                                               genres=genreList, state=state,
                                               error='You dont have ownership')
                else:
                    genreList = sess.query(Genre).all()
                    state = create_state()
                    return render_template('genreList.html',
                                           genres=genreList, state=state,
                                           error='Data not found')
            else:
                genreList = sess.query(Genre).all()
                state = create_state()
                return render_template('genreList.html',
                                       genres=genreList, state=state,
                                       error='You didnt fill all the fields')
        else:
            genreList = sess.query(Genre).all()
            state = create_state()
            return render_template('genreList.html', genres=genreList,
                                   state=state,
                                   error='You are not logged in')
    else:

        # get Handler post.

        if 'provider' in session and session['provider'] != 'null':

            # Validates if user is logged or not.

            state = create_state()
            u_id = check_user().id
            genreList = sess.query(Genre).all()
            movie = sess.query(Movies).filter_by(id=m_id,
                                                 g_id=g_id).one_or_none()
            if movie.u_id == u_id:

                # Validates movie ownership.

                return render_template('editMovie.html',
                                       genres=genreList, movie=movie,
                                       state=state)
            else:
                genreList = sess.query(Genre).all()
                state = create_state()
                return render_template('genreList.html',
                                       genres=genreList, state=state,
                                       error='Wrong Owner')
        else:
            genreList = sess.query(Genre).all()
            state = create_state()
            return render_template('genreList.html', genres=genreList,
                                   state=state,
                                   error='You are not logged in.')


@app.route('/delete/<int:g_id>/<int:m_id>')
def deleteMovie(g_id, m_id):
    if 'provider' in session and session['provider'] != 'null':

        # Validates if user is logged or not.

        u_id = check_user().id
        movie = sess.query(Movies).filter_by(id=m_id,
                                             g_id=g_id).one_or_none()
        if movie:

            # Check if movie exsists.

            if movie.u_id == u_id:

                # Validates movie ownership.

                sess.delete(movie)
                sess.commit()
                return redirect(url_for('genreView', gid=g_id))
            else:
                genreList = sess.query(Genre).all()
                state = create_state()
                return render_template('genreList.html',
                                       genres=genreList, state=state,
                                       error='You are not the owner')
        else:
            genreList = sess.query(Genre).all()
            state = create_state()
            return render_template('genreList.html', genres=genreList,
                                   state=state, error='Movie not found.'
                                   )
    else:
        genreList = sess.query(Genre).all()
        state = create_state()
        return render_template('genreList.html', genres=genreList,
                               state=state,
                               error='You are not logged in.')


@app.route('/gconnect', methods=['post'])
def gConnect():
    if request.args.get('state') != session['state']:
        response.make_response(json.dumps('Invalid State paramenter'),
                               401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code

    code = request.data
    try:

        # Upgrade the authorization code into a credentials object

        oauth_flow = flow_from_clientsecrets('client_secret.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = \
            make_response(json.dumps('Failed to upgrade the authorisation code'
                                     ), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    header = httplib2.Http()
    result = json.loads(header.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']

    # Verify that the access token is used for the intended user.

    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID  "
                                 + """does not
match given user ID."""
                                            ), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID"
                                 + """does not
                                      match app's."""
                                            ), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected.'
                                     ), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    session['credentials'] = access_token
    session['id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # ADD PROVIDER TO LOGIN SESSION

    session['name'] = data['name']
    session['img'] = data['picture']
    session['email'] = data['email']
    session['provider'] = 'google'
    if not check_user():
        add_user()
    return jsonify(name=session['name'], email=session['email'],
                   img=session['img'])


@app.route('/logout', methods=['post'])
def logout():

    # Disconnect based on provider

    if session.get('provider') == 'google':
        return gdisconnect()
    else:
        response = make_response(json.dumps({'state': 'notConnected'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/gdisconnect')
def gdisconnect():
    access_token = session['credentials']

    # Only disconnect a connected user.

    if access_token is None:
        response = make_response(json.dumps({'state': 'notConnected'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % access_token
    header = httplib2.Http()
    result = header.request(url, 'GET')[0]

    if result['status'] == '200':

        # Reset the user's session.

        del session['credentials']
        del session['id']
        del session['name']
        del session['email']
        del session['img']
        session['provider'] = 'null'
        response = make_response(json.dumps({'state': 'loggedOut'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        # if given token is invalid, unable to revoke token

        response = make_response(json.dumps({'state': 'errorRevoke'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/genre.json')
def genresJSON():
    genreList = sess.query(Genre).all()
    return jsonify(genres=[genre.serialize for genre in genreList])


@app.route('/genre/<int:gid>.json')
def movieListJSON(gid):
    movieList = sess.query(Movies).filter_by(g_id=gid)
    return jsonify(movies=[movie.serialize for movie in movieList])


@app.route('/genre/<int:g_id>/movie/<int:m_id>.json')
def movieJSON(g_id, m_id):
    movie = sess.query(Movies).filter_by(id=m_id,
                                         g_id=g_id).one_or_none()
    return jsonify(movie=movie.serialize)

if __name__ == '__main__':
    app.secret_key = 'quittersneverwin'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
