from flask import Flask, render_template, redirect, request, session
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
import os

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/gokart"
app.config['UPLOAD_FOLDER'] = "D:\\Gokart\\static\\img"
app.secret_key="super-secret-key"
db = SQLAlchemy(app)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    message = db.Column(db.String(50), nullable=False)

class Items(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(50), default="https://www.amazon.in/")
    img_file = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date= db.Column(db.String(12), nullable=False)

class Mobile(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    img_file = db.Column(db.String(25), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(50), nullable=False)

class Laptop(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    img_file = db.Column(db.String(25), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(50), nullable=False)

class Gadgets(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    img_file = db.Column(db.String(25), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(50), nullable=False)

class Camera(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    img_file = db.Column(db.String(25), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    items=Items.query.filter_by().all()
    return render_template('Gokart.html', items=items)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name=request.form.get('name')
        email=request.form.get('email')
        message=request.form.get('message')

        entry = Contact(name=name, email=email, message=message)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')

@app.route('/mobile')
def mobile():
    mobile=Mobile.query.filter_by().all()
    return render_template('Mobile.html', mobile=mobile)
@app.route('/laptop')
def laptop():
    laptop=Laptop.query.filter_by().all()
    return render_template('Laptop.html', laptop=laptop)
@app.route('/gadget')
def gadget():
    gadgets=Gadgets.query.filter_by().all()
    return render_template('gadget.html', gadgets=gadgets)
@app.route('/camera')
def camera():
    camera=Camera.query.filter_by().all()
    return render_template('camera.html', camera=camera)

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    items=Items.query.filter_by().all()
    if 'user' in session and session['user'] == 'admin':
        return render_template('dashboard.html', item=items)
    if request.method == 'POST':
        user=request.form.get('username')
        password=request.form.get('password')
        if(user == 'admin' and password == 'admin'):
            session['user'] = user
            return render_template('dashboard.html', items=items)
        else:
            return render_template('admin.html')
    else:
        return render_template('admin.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/admin')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload():
    if 'user' in session and session['user'] == 'admin':
        if request.method == 'POST':
            f=request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "uploaded successfully"
    else:
        return redirect('/admin')

app.run(debug=True)