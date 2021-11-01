import os
import smtplib
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, Response, request, render_template, url_for, redirect, flash, send_from_directory
from wtforms import StringField, TextAreaField, PasswordField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Email, Length
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from email.mime.text import MIMEText
from pdf2image import convert_from_path

app = Flask(__name__)
load_dotenv()

# Flask Server Config
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER")

# Database Config
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Email Config
admin_email = os.environ.get("ADMIN_EMAIL")
password = os.environ.get("ADMIN_EMAIL_PASSWORD")
receiver = os.environ.get("EMAIL_RECEIVER")


def sendMail(clientAddress, clientSubject, clientMessage):

    clientMessage = str("From: " + clientAddress +
                        "<br />" + "<br />"
                        " Message:" +
                        "<br/>" + clientMessage)

    msg = MIMEText(clientMessage, "html")
    msg["From"] = admin_email
    msg["To"] = receiver
    msg["Subject"] = clientSubject

    s = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
    s.login(user=admin_email, password=password)
    s.sendmail(admin_email, receiver, msg.as_string())
    s.quit()


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class ContactForm(FlaskForm):
    clientAddress = StringField('eMail Address', validators=[
                                DataRequired()], render_kw={"placeholder": "Email"})
    clientSubject = StringField('Subject', validators=[DataRequired()], render_kw={
                                "placeholder": "Subject"})
    clientMessage = TextAreaField(
        'Message', validators=[DataRequired()], render_kw={"placeholder": "Message"})


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={
                           "placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={
                             "placeholder": "Password"})


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "Username"})
    email = StringField('email', validators=[DataRequired(), Email(
        message='Invalid email'), Length(max=50)], render_kw={"placeholder": "E-Mail Address"})
    password = StringField('password', validators=[DataRequired(), Length(
        min=8, max=80)], render_kw={"placeholder": "Password"})


class UploadFile(FlaskForm):
    file = FileField('Files', validators=[FileRequired(
    ), FileAllowed(['pdf'])])


app.config['TIMETABLE_PDF'] = ""
app.config['TIMETABLE_JPEG'] = ""
app.config['TIMETABLE_WEBP'] = ""


# PUBLIC ACCESsABLE PAGES
@app.route("/")
@app.route("/index")
def index():
    return render_template("public/index.html")


@app.route("/timetable")
def timtable():
    d = TimetableConfig.query.filter_by(id=1).first()
    if d:
        timetablePDF = d.pdf
        timetableJPEG = d.jpeg
        timetableWebP = "uploads/" + d.webp

    return render_template("public/timetable.html", timetablePDF=timetablePDF,
                           timetableJPEG=timetableJPEG, timetableWebP=timetableWebP)


@app.route("/articles")
def articles():
    return render_template("public/articles.html")


@app.route("/audio")
def audio():
    return render_template("public/audio.html")


@app.route("/about")
def about():
    return render_template("public/about.html")


@app.route("/contact")
def contact():
    form = ContactForm()

    if form.validate_on_submit():

        clientAddress = form.clientAddress.data
        clientSubject = clientAddress + " : " + form.clientSubject.data
        clientMessage = form.clientMessage.data
        sendMail(clientAddress, clientSubject, clientMessage)

        return redirect('/')

    return render_template("public/contact.html", form=form)


@app.route("/admin/login", methods=('GET', 'POST'))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=False)
                return redirect(url_for('admin_portal'))

        return redirect(url_for('admin_portal'))

    return render_template("admin/admin-login.html", name="Login", form=form)


@app.route('/admin/register', methods=['GET', 'POST'])
@login_required
def admin_register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')

        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("admin_portal"))

    return render_template('admin/admin-register.html', form=form)


@app.route("/admin/portal")
@login_required
def admin_portal():
    form = UploadFile()

    return render_template("admin/admin-portal.html", name="Portal", form=form)


@app.route("/admin/articles")
@login_required
def admin_articles():
    return render_template("admin/admin-articles.html", name="Article Editor")


@app.route('/admin/uploads', methods=['GET', 'POST'])
@login_required
def admin_upload_file():

    form = UploadFile()

    if form.validate_on_submit():
        f = form.file.data
        uploadDir = app.config['UPLOAD_FOLDER']

        # Add uploaded File to Uploads Folder
        timetablePDF = secure_filename(f.filename)
        f.save(os.path.join(uploadDir, timetablePDF))

        # Save first PDF Page in JPEG & WebP formats
        timetableWebP = os.path.splitext(timetablePDF)[0] + ".webp"
        timetableJPG = os.path.splitext(timetablePDF)[0] + ".jpg"
        pdfLocation = uploadDir + timetablePDF

        images = convert_from_path(pdfLocation, 500)
        images[0].save(os.path.join(uploadDir, timetableWebP))
        images[0].save(os.path.join(uploadDir, timetableJPG))

        # Save File Names to Database
        fileData = TimetableConfig(
            id=1,
            pdf=timetablePDF,
            jpeg=timetableJPG,
            webp=timetableWebP
        )

        db.session.query(TimetableConfig).delete()
        db.session.commit()

        db.session.add(fileData)
        db.session.commit()

    return redirect(url_for('admin_portal'))


@app.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# ERROR HANDLER
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
