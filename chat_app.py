from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'}
db = SQLAlchemy(app)


class User(db.Model):
    user = db.Column(db.String(100), nullable=False, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, user, email, password):
        self.user = user
        self.email = email
        self.password = password


class Chat(db.Model): 
    __bind_key__ = 'chat'

    message = db.Column(db.String(100), nullable=False, primary_key=True)
    author = db.Column(db.String(120), nullable=False)

    def __init__(self, message, author):
        self.message = message
        self.author = author


@app.route('/')
def default():
    db.create_all()
    return render_template("login_page.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        db_user = User.query.filter_by(user=request.form['username'], password=request.form["password"]).first()
        user_input = request.form["username"]

        if db_user is None:     # if user is not in db go to register page
            return redirect(url_for("register"))

        return redirect(url_for("profile", username=user_input))    # log in user

    return render_template("login_page.html")


@app.route("/register/", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        retype_password = request.form['retype']

        requested_user = User.query.filter_by(user=username, email=email, password=password).first()

        if username is None:    # if anything is blank return to register page
            return redirect(url_for("register"))
        elif email is None:
            return redirect(url_for("register"))
        elif password is None:
            return redirect(url_for("register"))
        elif requested_user is None:    # registering new user
            if password != retype_password:  # if passwords don't match return to register page
                return redirect(url_for("register"))
            else:   # add information to the database
                register_user = User(user=username, email=email, password=password)
                db.session.add(register_user)
                db.session.commit()
                return redirect(url_for("login"))   # go to login page
        elif username == requested_user.user and email == requested_user.email and password == requested_user.password:
            return "This user is already registered"    # if already registered throw error page

    return render_template("register.html")


@app.route('/logout/')
def logout():
    return render_template('logout_page.html')


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    requested_user = User.query.filter_by(user=username).first()
    return render_template("chat_page.html", user=requested_user)


@app.route("/new_message/", methods=["POST"]) 
def new_message():  # commits new message to chats db
    message = request.form['message']
    author = request.form['author']
    new_chat = Chat(message=message, author=author)

    db.session.add(new_chat)
    db.session.commit()

    return "messages added"


@app.route("/messages/") 
def messages():     # properly format messages into dicts
    chats_arr = Chat.query.all()
    chats_dict = []
    for chat in chats_arr:
        chats_dict.append({'message': chat.message, 'author': "User: "+chat.author})

    return json.dumps(chats_dict)


if __name__ == "__main__":
    app.run(debug=True)
