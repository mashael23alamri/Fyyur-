# Fyyur-project1-FSND
Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues.
This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.
-------------------------------------------------------------------------

### Tech Stack

Our tech stack will include:

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependences
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```
  
  -------------------------------------------------------------------------
  
  ### Development Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) if you haven't already.

  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)

 
-------------------------------------------------------------------------
 ### DELETE Venue & Artist
 #### app.py
 
  ```python
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
```

 #### show_venue.html
 ```html
 <button id ="delete_venues" onclick="deleteVenue(event)" class="btn btn-default btn-sm" data-id="{{ venue.id }}" style="width: 100px;" >Delete Venue</button>
 ```
 
 #### show_artist.html
 ```html
 <button id ="delete_artist" onclick="deleteartist(event)" class="btn btn-default btn-sm" data-id="{{ artsit.id }}" style="width: 100px;" >Delete Venue</button>
 ``` 
 
 #### show_venue.html
 ```javascript
 	// A function to handle the deletion event....
	function deleteVenue(venue_id){
      fetch('/venues/'+venue_id , {
            method: 'DELETE',
            headers: {'content-type': 'application/json',
                      redirect: true},
            body: JSON.stringify({id: venue_id})
            })
                  .then(res => console.log(res))
                  .then(setTimeout(function(){
             window.location.href = '/venues'
					 }, 200))
             }
     
 ```
 #### show_artist.html
  ```javascript
 	// A function to handle the deletion event....
	function deleteArtist(artist_id){
      fetch('/artists/'+artist_id , {
            method: 'DELETE',
            headers: {'content-type': 'application/json',
                      redirect: true},
            body: JSON.stringify({id: artist_id})
            })
                  .then(res => console.log(res))
                  .then(setTimeout(function(){
             window.location.href = '/artists'
					 }, 200))
             }
 ```
 
 ## References:
 1-[flask-wtf](https://flask-wtf.readthedocs.io/en/stable/)
 
 2-[flask-migrate](https://www.patricksoftwareblog.com/tag/flask-migrate/)
 
 3-[w3schools](https://www.w3schools.com/)
 
 4-[flask-with-getlist](http://http://www.seanbehan.com/reshape-an-array-of-form-inputs-for-flask-with-getlist/)
 
 5-[setattr](https://wiki.hsoub.com/Python/setattr...)
 
