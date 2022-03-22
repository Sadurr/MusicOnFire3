from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy import or_


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:zyZiek1999XD!@localhost/postgres'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)

class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    band = db.Column(db.String(80), nullable=False)
    album = db.Column(db.String(120), nullable=False)
    genre =  db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def __init__(self, band, album, genre, description):
        self.band = band
        self.album = album
        self.genre = genre
        self.description = description

@app.route('/')
def home():
    return render_template("index.html")


@app.route("/addmusic")
def addmusic():
    return render_template("index.html")


@app.route("/musicadd", methods=['POST'])
def musicadd():
    band = request.form["modalBandText"]
    album = request.form["modalAlbumText"]
    genre = request.form["modalGenreText"]
    description = request.form["modalDescriptionText"]

    entry = Music(band, album, genre, description)
    db.session.add(entry)
    db.session.commit()

    return render_template("index.html")

@app.route("/musicsearch",  methods=['POST', 'GET'])
def musicsearch():
    inputForQuery = request.form["inputText"]
    inputType = request.form["inputType"]

    # bands = db.session.query(Music.band).all() #all bands from db
    # albums = db.session.query(Music.album).all()
    # genres = db.session.query(Music.genre).all()
    # descriptions = db.session.query(Music.description).all()


    if inputType == "band":
        band = db.session.query(Music.band).filter_by(band=inputForQuery).all() #list 
        album = db.session.query(Music.album).filter_by(band=inputForQuery).all()
        genre = db.session.query(Music.genre).filter_by(band=inputForQuery).all()
        description =  db.session.query(Music.description).filter_by(band=inputForQuery).all()
    elif inputType == 'genre':
        band = db.session.query(Music.band).filter_by(genre=inputForQuery).all()
        album = db.session.query(Music.album).filter_by(genre=inputForQuery).all()
        genre = db.session.query(Music.genre).filter_by(genre=inputForQuery).all()
        description =  db.session.query(Music.description).filter_by(genre=inputForQuery).all()       
    elif inputType == 'description':
        band = db.session.query(Music.band).filter_by(description=inputForQuery).all()
        album = db.session.query(Music.album).filter_by(description=inputForQuery).all()
        genre = db.session.query(Music.genre).filter_by(description=inputForQuery).all()
        description =  db.session.query(Music.description).filter_by(description=inputForQuery).all()
        if inputForQuery == 'calm': #or...
            recommended_band =  db.session.query(Music.band).filter_by(description='happy').all()
            recommended_album = db.session.query(Music.album).filter_by(description='happy').all()
            recommended_genre =  db.session.query(Music.genre).filter_by(description='happy').all()
            recommended_description =  db.session.query(Music.description).filter_by(description='happy').all()
        elif inputForQuery == 'energetic':
            recommended_band = db.session.query(Music.band).filter(or_(Music.description == 'noisy' or Music.description == 'aggressive')).all()
            recommended_album = db.session.query(Music.album).filter(or_(Music.description == 'noisy' or Music.description == 'aggressive')).all()
            recommended_genre = db.session.query(Music.genre).filter(or_(Music.description == 'noisy' or Music.description == 'aggressive')).all()
            recommended_description = db.session.query(Music.description).filter(or_(Music.description == 'noisy' or Music.description == 'aggressive')).all()

    return render_template("result.html", band=band, album=album, genre=genre, description=description, 
    recommended_band=recommended_band, recommended_album=recommended_album, recommended_genre=recommended_genre, recommended_description=recommended_description)

if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.run()