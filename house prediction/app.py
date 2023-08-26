from flask import flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

app = flask(__name__)
app.secret_key = 'secret_key'  # Set your secret key for session management

 
users = {
    'john': generate_password_hash('password1'),
    'jane': generate_password_hash('password2')
 }

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return render_template('house_prediction.html')
            return redirect('/profile')

        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return render_template('signup.html', error='Username already taken')

        users[username] = generate_password_hash(password)
        session['username'] = username
        return redirect('/profile')

    return render_template('signup.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        return render_template('profile.html', username=username)

    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'username' in session:
        if request.method == 'POST':
            # Get the input data from the form
            area = request.form['area']
            bedrooms = request.form['bedrooms']
            bathrooms = request.form['bathrooms']

            # Perform house prediction logic here
            # You can use a machine learning model or any other method to predict the house price based on the input data

            # For demonstration purposes, let's assume the prediction result is a random value between 100,000 and 1,000,000
            import random
            prediction_result = random.randint(100000, 1000000)

            return render_template('prediction_result.html', area=area, bedrooms=bedrooms, bathrooms=bathrooms, prediction_result=prediction_result)

        return render_template('house_prediction.html')
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
