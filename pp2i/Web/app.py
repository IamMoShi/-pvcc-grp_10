from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/status')
def index():
    return 'Up and Running'

@app.route('/navbar')
def navbar():
    return render_template("navBar.html")


if __name__ == '__main__':
    app.run(debug=True)
