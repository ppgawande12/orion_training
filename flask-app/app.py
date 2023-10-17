from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = 'Pass@123' 
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydb' 

mongo = PyMongo(app)

users_collection = mongo.db.users



@app.route('/')
def home():
    return render_template('base.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if users_collection.find_one({'email': email}):
            return 'email already exists. Choose another one.'

        password = password
        users_collection.insert_one({'email': email, 'password': password})
        session['email'] = email
        return redirect(url_for('profile'))

    return render_template('signup.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_collection.find_one({'email': email})
        if user and password(user['password'], password):
            session['email'] = email
            return redirect(url_for('profile'))

        return 'Invalid email or password. Please try again.'

    return render_template('login.html')



@app.route('/profile')
def profile():
    if 'email' in session:
        email = session['email']
        return f'Welcome, {email}!'
    return 'You need to log in first.'



@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
