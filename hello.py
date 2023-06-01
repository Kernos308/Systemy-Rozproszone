from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/photos'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}
db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Definiowanie modelu danych
class FormEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    photo = db.Column(db.String(100))


# Tworzenie tabeli w bazie danych
with app.app_context():
    db.create_all()

# Strona główna
@app.route('/')
def home():
    buttons = [
        {'text': 'Photos', 'url': '/photos'},
        {'text': 'Videos', 'url': '/videos'},
        {'text': 'Form', 'url': '/form'}
    ]
    return render_template('index.html', buttons=buttons)


# Formularz
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('Brak zdjecia w formularzu')
            return redirect(request.url)
        name = request.form['name']
        email = request.form['email']
        photo = request.files['photo']

        if photo.filename == '':
            flash('Brak wybranego zdjecia')
            return redirect(request.url)

        if 'photo' in request.files and allowed_file(photo.filename):
            photo = request.files['photo']
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Przesłano zdjęcie')
            return redirect(url_for('form'))
        else:
            flash('Nie przesłano zdjęcie. Błędne rozszerzenie')
            filename = None
            return redirect(request.url)

        # Zapisywanie danych do bazy danych
        entry = FormEntry(name=name, email=email, photo=filename)
        db.session.add(entry)
        db.session.commit()

    return render_template('form.html')


# Podstrona z osadzonym elementem multimedialnym
@app.route('/photos')
def photos():
    entries = FormEntry.query.all()  # Pobierz wszystkie wpisy z bazy danych

    return render_template('photos.html', entries=entries)

@app.route('/videos')
def videos():
    video_path = "/static/videos/my_video.mp4"
    return render_template('videos.html', video_path=video_path)



if __name__ == '__main__':
    app.run()