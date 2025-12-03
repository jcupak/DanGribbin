from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import csv


app = Flask(__name__)
ckeditor = CKEditor(app)
Bootstrap(app)


# WTForms
class CreateContactForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    email = StringField("Return Email Address", validators=[DataRequired()])
    message = CKEditorField("Message", validators=[DataRequired()])
    # security_image = <img src="/include/captchas/captcha_image.php", alt="security image", border="0">
    security_code = StringField("Enter Security Code", validators=[DataRequired()])
    submit = SubmitField("Submit Message")


# MARK: home
@app.route("/", endpoint='index')
def home():
    """
    Display home page
    :return: nothing
    """
    return render_template("index.html")

# MARK: songs
@app.route('/songs', endpoint='songs')
def songs():
    """
    Displays alphabetical list of songs written by Dan Gribbin
    :return: link to songs.html with list_of_songs
    """
    with open("songs_sorted.csv", newline='') as songs_file:
        songs_data = csv.reader(songs_file, delimiter=',')
        list_of_songs = []
        for song in songs_data:
            list_of_songs.append(song)
        return render_template('songs.html', songs=list_of_songs)

# MARK: song
@app.route('/song/<id>')
def song(id):
    """
    Displays specific song information
    :param id: The song number, 0-47
    :return: Nothing
    
    Song lyrics from file song_lyrics_##.tx
    """
    song_data = []

    with open(f"song_info.csv", mode="r") as songs_file:
        songs_data = csv.reader(songs_file, delimiter="|")
        for song in songs_data:
            song_data.append(song)
    # end song_info file

    # Read song lyrics file
    if len(id) == 1:
        song_lyrics_filename = f"song_lyrics_0{id}.txt"
    else:
        song_lyrics_filename = f"song_lyrics_{id}.txt"
    # endif
    song_lyrics = ""
    with open(song_lyrics_filename, mode="r") as song_lyrics_file:
        song_lyrics_raw = song_lyrics_file.readlines()
        for line in song_lyrics_raw:
            stripped_line = line.strip()
            # print(f"{len(line)} {stripped_line}")
            song_lyrics += stripped_line + '\n'


    # Pass specific song data to web page
    song_number = int(id)
    return render_template('song.html', song=song_data[song_number], lyrics=song_lyrics)

# MARK: albums
@app.route("/albums", endpoint='albums')
def albums():
    """Displays song albums created by Dan Gribbin
    :return: link to albums.html with list_of_albums
    """
    with open("albums.csv", newline='') as albums_file:
        albums_data = csv.reader(albums_file, delimiter=",")
        list_of_albums = []
        for album in albums_data:
            list_of_albums.append(album)
        return render_template('albums.html', albums=list_of_albums)

# MARK: album
@app.route("/album/<id>/", endpoint='album')
def album(id):
    """ Displays album information and tracks
    :return: nothing
    """

    # Create album information from first 3 lines of file
    with open(f"album_{id}_info.txt", "r") as info_file:
        album_image = info_file.readline()
        album_title = info_file.readline()
        album_info  = info_file.readline()
    # end album_info file

    # Create album track information
    with open(f"album_{id}_tracks.csv", newline='') as tracks_file:
        tracks_data = csv.reader(tracks_file, delimiter='|')  # Use '|' because description has commas
        album_tracks = []
        for track in tracks_data:
            album_tracks.append(track)
    # end album_tracks file

    return render_template('album.html',
                           image=album_image,
                           title=album_title,
                           description=album_info,
                           tracks=album_tracks)

# MARK: gallery
@app.route("/gallery", endpoint='gallery')
def gallery():
    """
    Displays carousel of Dan Gribbin's photos

    :return: nothing
    """
    with open("photos.csv") as photos_file:                            # Open CSV file of photo information
        photos_data = csv.reader(photos_file, delimiter="|")           # Uses "|" because descriptions contain comma
        list_of_photos = []                                            # Create empty list
        for photo_info in photos_data:                                 # For each line of dlimited data in file
            list_of_photos.append(photo_info)                          # Append to list
        return render_template("gallery.html", photos=list_of_photos)  # Pass list to web page

# MARK: events
@app.route("/events", endpoint='events')
def events():
    """Displays list of recent and past events"""
    with open("events.csv") as events_file:
        events_data = csv.reader(events_file, delimiter="|")
        events_list = [ ]
        for event_info in events_data:
            events_list.append(event_info)
        return render_template("events.html", events=events_list)

# MARK: event
@app.route("/event/<id>/", endpoint='event')
def event(id):
    """Displays information for event matching id."""
    the_event = []
    with open("event_info.csv") as events_file:
        events_data = csv.reader(events_file, delimiter="|")
        for event_info in events_data:
            if event_info[0] == id:
                # print(f"{id} matches event {event_info [ 0 ]}")
                the_event = event_info
                break
            # endif matching event id
        # end for event_info

    # Read event footer file
    event_footer_filename = f"event_footer_{id}.txt"
    with open(event_footer_filename, mode="r") as event_footer_file:
        event_footer = event_footer_file.readlines()

    # Pass event info and event footer info to event.html for display
    return render_template("event.html", event=the_event, footer=event_footer)

# MARK: news
@app.route("/news", endpoint='news')
def news():
    """Displays list of recent and past news"""
    with open("news.txt") as news_file:
        news_data = news_file.readlines()  #read entire file into list
        return render_template("news.html", news=news_data)

# MARK: about
@app.route("/about", endpoint='about')
def about():
    """Displays about biographty of Dan Gribbin"""
    return render_template("about.html")

# MARK: links
@app.route("/links", endpoint='links')
def links():
    """Displays links and information"""
    with open("album_info_links.csv") as links_file:
        links_data = csv.reader(links_file, delimiter="|")
        links_list = []
        for link_info in links_data:
            links_list.append(link_info)
        return render_template("links.html", links=links_list)

# MARK: contact
@app.route("/contact", endpoint='contact')
def contact():
    """Display contact form, send all information"""
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
