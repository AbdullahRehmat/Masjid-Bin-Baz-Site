from flask import Flask, render_template

app = Flask(__name__)


# PUBLIC ACCESsABLE PAGES
@app.route("/")
@app.route("/index")
def index():
    return render_template("public/index.html")


@app.route("/timetable")
def timtable():
    return render_template("public/timetable.html")


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
    return render_template("public/contact.html")

# ADMIN PAGES


@app.route("/admin/login")
def admin_login():
    return render_template("admin/admin-login.html", name="Login")


@app.route("/admin/portal")
def admin_portal():
    return render_template("admin/admin-portal.html", name="Portal")


@app.route("/admin/articles")
def admin_articles():
    return render_template("admin/admin-articles.html", name="Article Editor")

# ERROR HANDLER


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
