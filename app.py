from datetime import datetime
from flask import Flask, render_template,url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app, session_options={"expire_on_commit": False})


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='pic.jpg')
    email = db.Column(db.String(100), nullable=False, unique=True)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"


posts = [
    {
        'author': 'Lynne Chebet',
        'title': 'Mental Health',
        'content': 'Mental health is very important in our generation',
        'date_posted': 'January 18, 2023'
    },
{
        'author': 'John Ekhardt',
        'title': 'Salvation',
        'content': 'Jesus saves us',
        'date_posted': 'January 20, 2023'
    },
{
        'author': 'Smith Wigglesworth',
        'title': 'The power of prayer',
        'content': 'Prayer is very important in our generation',
        'date_posted': 'February 14, 2023'
    },
{
        'author': 'Peter Tan',
        'title': 'Anointing that breaks chains',
        'content': 'Everyone has a special anointing',
        'date_posted': 'July 24, 2023'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created! Username: {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Log in successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


with app.app_context():
    db.create_all()
    db.drop_all()
    db.create_all()


user1 = User(username='Benny', email='benny@gmail.com', password='benny')
user2 = User(username='Joy', email='joy@gmail.com', password='joy')
user3 = User(username='Angel', email='angel@gmail.com', password='angel')


with app.app_context():
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()


post1 = Post(title='The Holy Spirit', content='The Holy Spirit is the third person of the trinity, but the most misunderstood. Read my book, Good Morning Holy Spirit to find out more about the Holy Spirit', user_id=user2.id)
post2 = Post(title='The Anointing', content='The anointing of God, The anointing of God breaks chains. It causes walls to fall. It gives you power', user_id=user1.id)
post3 = Post(title='Supernatural Power of a believer', content='You do not know how much power you have in you. Understand the different types of power God has given you as a believer. The kratos, ischus, dunamis, exousia and the epikaizo ', user_id=user3.id)


with app.app_context():
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
