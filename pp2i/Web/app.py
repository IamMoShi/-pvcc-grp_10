from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/status')
def index():
    return 'Up and Running'

@app.route('/navbar')
def navbar():
    return render_template("navBar.html")

@app.route('/signin')
def signin():
    return render_template("login/signin.html")
  
@app.route('/signup')
def signup():
    return render_template("login/signup.html")   

@app.route('/login')
def login():
    return render_template("login/login.html")

if __name__ == '__main__':
    app.run(debug=True)
