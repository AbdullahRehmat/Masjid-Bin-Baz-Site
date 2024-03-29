import os
import re
import json
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from flask_flatpages import FlatPages
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    send_from_directory,
    request,
)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from pdf2image import convert_from_path


# FLATPAGES Config
FLATPAGES_EXTENSION = ".md"
FLATPAGES_ROOT = "static"
ARTICLE_DIR = "articles"

# FLASK App Config
app = Flask(__name__)
flatpages = FlatPages(app)
app.config.from_object(__name__)
load_dotenv()

# Flask Server Configuration
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["AUDIO_FOLDER"] = os.environ.get("AUDIO_FOLDER")
app.config["JSON_PLAYLISTS"] = None
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TIMETABLE_FOLDER"] = os.environ.get("TIMETABLE_FOLDER")
app.config["ARTICLE_FOLDER"] = os.environ.get("ARTICLE_FOLDER")
app.config["BOTS_FOLDER"] = os.environ.get("BOTS_FOLDER")

# Playlist Name + URL Loader
def load_playlists():
    with open(app.config["AUDIO_FOLDER"]) as f:
        app.config["JSON_PLAYLISTS"] = json.load(f)

    return None


# Load All Markdown Articles
def load_articles():
    FlatPages.reload()


# Article HTML Tag Stripper
def tag_stripper(text):
    safe_text = re.sub(re.compile("<.*?>"), "", text)

    return safe_text


# Database Config
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


class TimetableConfig(db.Model):
    __tablename__ = "persistentConfig"
    id = db.Column(db.Integer, primary_key=True)
    pdf = db.Column(db.String(256), unique=True)
    jpeg = db.Column(db.String(256), unique=True)
    webp = db.Column(db.String(256), unique=True)


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired()], render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"placeholder": "Password"}
    )


class RegisterForm(FlaskForm):
    username = StringField(
        "username",
        validators=[DataRequired(), Length(min=4, max=15)],
        render_kw={"placeholder": "Username"},
    )
    email = StringField(
        "email",
        validators=[DataRequired(), Email(message="Invalid email"), Length(max=50)],
        render_kw={"placeholder": "E-Mail Address"},
    )
    password = StringField(
        "password",
        validators=[DataRequired(), Length(min=8, max=80)],
        render_kw={"placeholder": "Password"},
    )


class UploadTimetable(FlaskForm):
    file = FileField(
        "Timetable File", validators=[FileRequired(), FileAllowed(["pdf"])]
    )


class UploadArticle(FlaskForm):
    file = FileField("Article File", validators=[FileRequired(), FileAllowed(["md"])])


# PUBLIC PAGES
@app.route("/")
@app.route("/index")
def index():
    articles = [a for a in flatpages if a.path.startswith(ARTICLE_DIR)]
    articles.sort(key=lambda item: item["date"], reverse=True)

    # tag_stripper() -> Passes Tag Stripping Function To Jinja2 Script

    return render_template(
        "public/index.html", articles=articles, tag_stripper=tag_stripper
    )


@app.route("/timetable")
def timetable():
    t = TimetableConfig.query.filter_by(id=1).first()
    if t:
        timetable_pdf = t.pdf
        timetable_jpeg = t.jpeg
        timetable_webp = "uploads/" + t.webp

    return render_template(
        "public/timetable.html",
        timetablePDF=timetable_pdf,
        timetableJPEG=timetable_jpeg,
        timetableWebP=timetable_webp,
    )


@app.route("/articles/")
def articles():
    articles = [a for a in flatpages if a.path.startswith(ARTICLE_DIR)]
    articles.sort(key=lambda item: item["date"], reverse=True)

    # tag_stripper -> Passes Tag Stripping Function To Jinja2 Script

    return render_template(
        "public/articles.html", articles=articles, tag_stripper=tag_stripper
    )


@app.route("/article/<name>/")
def article(name):
    path = "{}/{}".format(ARTICLE_DIR, name)
    article = flatpages.get_or_404(path)
    return render_template("public/article.html", article=article)


@app.route("/audio")
def audio():
    return render_template("public/audio.html", data=app.config["JSON_PLAYLISTS"])


@app.route("/donate")
def donate():
    return render_template("public/donate.html")


@app.route("/about")
def about():
    return render_template("public/about.html")


@app.route("/private-policy")
def private_policy():
    return render_template("public/private-policy.html")


@app.route("/downloads/<path:filename>")
def download_file(filename):
    return send_from_directory(
        app.config["TIMETABLE_FOLDER"], filename, as_attachment=True
    )


# PRIVATE PAGES
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/portal/login", methods=("GET", "POST"))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=False)
                return redirect(url_for("portal_index"))

        return redirect(url_for("portal_index"))

    return render_template("portal/portal-login.html", name="Login", form=form)


@app.route("/portal/register", methods=["GET", "POST"])
@login_required
def portal_register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")

        new_user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("portal_index"))

    return render_template("portal/portal-register.html", form=form)


@app.route("/portal")
@login_required
def portal_index():
    form_timetable = UploadTimetable()
    form_article = UploadArticle()

    return render_template(
        "portal/portal-index.html",
        name="Dashboard",
        form_timetable=form_timetable,
        form_article=form_article,
    )


@app.route("/portal/articles")
@login_required
def portal_articles():
    return render_template("portal/portal-articles.html", name="Article Editor")


@app.route("/portal/upload/<category>", methods=["GET", "POST"])
@login_required
def portal_upload_file(category):

    if category == "timetable":
        form = UploadTimetable()

        if form.validate_on_submit():
            f = form.file.data
            upload_dir = app.config["TIMETABLE_FOLDER"]

            # Add uploaded File to Timetable Folder
            timetable_pdf = secure_filename(f.filename)
            f.save(os.path.join(upload_dir, timetable_pdf))

            # Save first PDF Page in JPEG & WebP formats
            timetable_webp = os.path.splitext(timetable_pdf)[0] + ".webp"
            timetable_jpeg = os.path.splitext(timetable_pdf)[0] + ".jpg"
            pdf_location = upload_dir + timetable_pdf

            images = convert_from_path(pdf_location, 500)
            images[0].save(os.path.join(upload_dir, timetable_webp))
            images[0].save(os.path.join(upload_dir, timetable_jpeg))

            # Save File Names to Database
            file_data = TimetableConfig(
                id=1, pdf=timetable_pdf, jpeg=timetable_jpeg, webp=timetable_webp
            )

            db.session.query(TimetableConfig).delete()
            db.session.commit()

            db.session.add(file_data)
            db.session.commit()

            return redirect(url_for("portal_index"))

        else:
            return redirect(url_for("page_not_found"))

    elif category == "article":
        form = UploadArticle()

        if form.validate_on_submit():
            f = form.file.data
            upload_dir = app.config["ARTICLE_FOLDER"]

            # Add uploaded File to Article Folder
            article_md = secure_filename(f.filename)
            f.save(os.path.join(upload_dir, article_md))

            return redirect(url_for("portal_index"))

        else:
            return redirect(url_for("page_not_found"))

    else:
        return redirect(url_for("page_not_found"))


@app.route("/portal/reload/<path>")
@login_required
def reload_content(path):
    if path == "audio":
        # Reload SoundCloud Playlist URLs
        load_playlists()
        return redirect(url_for("portal_index"))

    elif path == "articles":
        # Reload Markdown Articles
        # load_articles()
        # FlatPages.reload()
        return redirect(url_for("portal_index"))

    else:
        return redirect(url_for("page_not_found"))


@app.route("/portal/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


# PAGES FOR BOTS
@app.route("/robots.txt")
@app.route("/sitemap.xml")
def static_from_root():
    return send_from_directory(app.config["BOTS_FOLDER"], request.path[1:])


# ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404


if __name__ == "__main__":

    # Load SoundCloud Playlist URLs
    load_playlists()

    # Run Application
    app.run(debug=True, host="0.0.0.0", port=5000)
