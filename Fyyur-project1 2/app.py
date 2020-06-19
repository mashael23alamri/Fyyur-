#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging

from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from forms import *

import sys
from datetime import datetime
from sqlalchemy import MetaData
from forms import VenueForm, ArtistForm, ShowForm


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
# connect to a local postgresql database in config.py...

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# TODO: implement any missing fields, as a database migration using Flask-Migrate
# Add restrictions to name,city,state,address,phone...
# Add fields genres,website,seeking_talent,seeking_description...

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), unique=True)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description =  db.Column(db.String(120))
    # Add relationship...
    shows = db.relationship('Show', backref='venue', lazy=True)

    # Add def __repr__(self)...
    # Use the function repr to display objects...
    def __repr__(self):
        return f'<Venue {self.id}, {self.name}, {self.city},\
                        {self.state}, {self.address}, {self.phone},\
                        {self.image_link}, {self.facebook_link}, {self.genres},\
                        {self.website}, {self.seeking_talent}, {self.seeking_description}>'


# Add restrictions to name,city,state,phone,genres...
# Add fields,website,seeking_venue,seeking_description ...
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), unique=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description =  db.Column(db.String(120))
    # Add relationship...
    shows = db.relationship('Show', backref='artist', lazy=True)

    # Add def __repr__(self)...
    # Use the function repr to display objects...

    def __repr__(self):
      return f'<Artist {self.id}, {self.name}, {self.city}, {self.state},\
                       {self.phone}, {self.genres}, {self.image_link},\
                       {self.facebook_link}, {self.genres}, {self.website}\
                       {self.seeking_venue}, { self.seeking_description}>'


# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# Create a class Show...
class Show(db.Model):
    __tablename__ = 'Show'

    # Create a record for each of  id, artist_id, venue_id,start_time...
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    # Create foreign keys to link relationships between a table Artist and a table Venue with a table Show...
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False )
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

    # Add def __repr__(self)...
    # Use the function repr to display objects...

    def __repr__(self):
        return f'<Show artist_id : {self.venue_id} venue_id: {self.artist_id},\
                 start_time: {self.start_time} venue: {self.venue.name}>'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  # Show venues as a list...

     # Query using the order of Venue city and Venue state...
     venues_list = Venue.query.order_by(Venue.city, Venue.state).all()
     # A list...
     data = []
     #Create a set of all the cities/states combinations uniquely...
     citystate = ''
     # for loop...
     for venue in venues_list:
         # To find out about upcoming shows, query using join Venue and show...
         num_upcoming_shows = db.session.query(Venue).join(Show).\
           filter (Venue.id == venue.id, Show.start_time > datetime.now()).count()
         if citystate == venue.city + venue.state:
            # Add the item venues to the end of the list...
            # References:https://docs.python.org/3.3/tutorial/datastructures.html...
             data[len(data) - 1]['venues'].append({
                    'id': venue.id,
                    'name': venue.name,
                    'num_upcoming_shows': num_upcoming_shows
             })
         else:
             data.append({
                 'city': venue.city,
                 'state': venue.state,
                 'venues':[{'id': venue.id ,'name': venue.name, 'num_upcoming_shows': num_upcoming_shows }]
             })
             citystate = venue.city + venue.state
     return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
   response = {}
   try:
       # Use query.with_entities because get tuples with values of chosen columns...
       # Use filter not filter_by when doing like search i=insensitive to case...
       venues_list = Venue.query.with_entities(Venue.id, Venue.name).\
            filter(Venue.name.ilike('%' + request.form.get('search_term', '') + '%')).all()

       response['data'] = venues_list
       response['count'] = len(venues_list)

   except Exception as e:
       print(e)
       flash('An error occurred in the search term' + request.form.get('search_term', ''))

   finally:
       return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.get(venue_id)
  # The function creates a value for the venue property and giving it a name and values...
  # References:https://wiki.hsoub.com/Python/setattr...
  setattr(venue, 'past_shows', [])
  setattr(venue, 'upcoming_shows', [])
  current_time = datetime.now()
  past_shows_count = 0
  upcoming_shows_count = 0
  # Query from Artist and start_time in show and join Show with filter Show.venue_id == venue_id...
  shows = db.session.query(Artist, Show.start_time).join(Show).filter(Show.venue_id == venue_id)
  # For loop in show ...
  for artist, start_time in shows:
      # if start time less than from current_time this mean shows in past...
      if start_time  <  current_time:
          # append...
          venue.past_shows.append({
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': str(start_time)
          })
          past_shows_count += 1
      # if not start time less than from current_time this mean shows in upcoming...
      else:
          venue.upcoming_shows.append({
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': str(start_time)
          })
          upcoming_shows_count += 1
      # References:https://wiki.hsoub.com/Python/setattr...
      setattr(venue, 'past_shows_count', past_shows_count)
      setattr(venue, 'upcoming_shows_count', upcoming_shows_count)
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()

  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    # To access the array we use getlist...
    # References:http://http://www.seanbehan.com/reshape-an-array-of-form-inputs-for-flask-with-getlist/...
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website']
    seeking_talent = True if 'seeking_talent' in request.form else False
    seeking_description = request.form['seeking_description']

    venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue ' + request.form['name']+ ' could not be listed.')
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')


#  DELETE Venue...
#  ----------------------------------------------------------------
@app.route('/venues/<venue_id>' , methods=['DELETE'])
def delete_venues(venue_id):
  try:
    venue = db.session.query(Venue).filter(Venue.id==venue_id).all()
    for v in venue:
      db.session.delete(v)
      db.session.commit()
  except:
    flash('cannot be deleted')
  finally:
    db.session.close()
    #return venues...
    return redirect(url_for("venues"))


#  DELETE Artist...
#  ----------------------------------------------------------------
@app.route('/artists/<artist_id>' , methods=['DELETE'])
def delete_artist(artist_id):
      try:
        artist = db.session.query(Artist).filter(Artist.id==artist_id).all()
        for a in artist:
          db.session.delete(a)
          db.session.commit()
      except:
        flash('cannot be deleted')
      finally:
        db.session.close()
        #return venues...
        return redirect(url_for("artists"))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.with_entities(Artist.id, Artist.name).all()
  return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response = {}
  try:
      # Use query.with_entities because get tuples with values of chosen columns...
      # Use filter not filter_by when doing like search i=insensitive to case...
      artist_list = Artist.query.with_entities(Artist.id, Artist.name).\
          filter(Artist.name.ilike('%' + request.form.get('search_term', '') + '%')).all()

      response['data'] = artist_list
      response['count'] = len(artist_list)

  except Exception as e:
      print(e)
      flask('An error occurred for the search term' + request.form.get('search_term', ''))

  finally:
      return render_template ('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
    current_time = datetime.now()
    artist = Artist.query.get(artist_id)
    setattr(artist, 'past_shows', [])
    setattr(artist, 'upcoming_shows', [])
    past_shows_count = 0
    upcoming_shows_count = 0
    # Query from Artist and start_time in show and join Show with filter Show.venue_id == venue_id...
    shows = db.session.query(Venue, Show.start_time).join(Show).filter(Show.artist_id == artist_id)
    # for loop in show...
    for venue, start_time in shows:
        # if start time less than from current_time this mean shows in past...
        if start_time < current_time:
            # append...
            artist.past_shows.append({
               'venue_id': venue.id,
               'venue_name': venue.name,
               'venue_image_link': venue.image_link,
               'start_time' : str(start_time)
            })
            past_shows_count += 1
        # if not start time less than from current_time this mean shows in upcoming...
        else:
            artist.upcoming_shows.append({
               'venue_id': venue.id,
               'venue_name': venue.name,
               'venue_image_link': venue.image_link,
               'start_time' : str(start_time)
            })
            upcoming_shows_count += 1
    # References:https://wiki.hsoub.com/Python/setattr...
    setattr(artist, 'past_shows_count', past_shows_count)
    setattr(artist, 'upcoming_shows_count', upcoming_shows_count)

    return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  if artist:
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    form.website.data = artist.website
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description

   # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  artist = Artist.query.get(artist_id)

  try:
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    # To access the array we use getlist...
    # References:http://http://www.seanbehan.com/reshape-an-array-of-form-inputs-for-flask-with-getlist/...
    artist.genres = request.form.getlist('genres')
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    artist.website = request.form['website']
    artist.seeking_venue = True if 'seeking_venue' in request.form else False
    artist.seeking_description = request.form['seeking_description']

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist could not be changed.')
  if not error:
    flash('Artist was successfully updated!')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  if venue:
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.address.data = venue.address
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.website.data = venue.website
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
   # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  venue = Venue.query.get(venue_id)

  try:
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    # To access the array we use getlist...
    # References:http://http://www.seanbehan.com/reshape-an-array-of-form-inputs-for-flask-with-getlist/...
    venue.genres = request.form.getlist('genres')
    venue.image_link = request.form['image_link']
    venue.facebook_link = request.form['facebook_link']
    venue.website = request.form['website']
    venue.seeking_talent = True if 'seeking_talent' in request.form else False
    venue.seeking_description = request.form['seeking_description']

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash(f'An error occurred. Venue could not be changed.')
  if not error:
    flash(f'Venue was successfully updated!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  error = False
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    # To access the array we use getlist...
    # References:http://http://www.seanbehan.com/reshape-an-array-of-form-inputs-for-flask-with-getlist/...
    genres = request.form.getlist('genres'),
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website = request.form['website']
    seeking_venue = True if 'seeking_venue' in request.form else False
    seeking_description = request.form['seeking_description']

    artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist ' + request.form['name']+ ' could not be listed.')
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')




#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
   data = []
   shows = db.session.query(Show, Venue.name, Artist).join(Venue, Artist)
   for show, venue_name, artist in shows:
       data.append({
          'start_time': str(show.start_time),
           'venue_id': show.venue_id,
           'venue_name': venue_name,
           'artist_id': show.artist_id,
           'artist_name': artist.name,
           'artist_image_link': artist.image_link
       })
       print('data: ', data[0]['start_time'])
   return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
   # renders form. do not touch.
   form = ShowForm()
   return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
    form = ShowForm()
    error = False
    try:
        if form.validate_on_submit():
            show = Show(
                start_time=form.start_time.data,
                venue_id=form.venue_id.data,
                artist_id=form.artist_id.data
            )
            db.session.add(show)
            db.session.commit()
    except Exception as e:
         print('create_show_submission: ', e)
         db.session.rollback()
         print(sys.exc_info())
         error = True
    finally:
         # on successful db insert, flash success
         db.session.close()
    if error:
       # TODO: on unsuccessful db insert, flash an error instead.
       # e.g., flash('An error occurred. Show could not be listed.')
       # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
       flash('An error occurred. Show could not be listed.')
       return render_template('forms/new_show.html', form=form)
    else:
        flash('Show was successfully listed!')
        return render_template('pages/home.html')

#----------------------------------------------------------------------------#

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
