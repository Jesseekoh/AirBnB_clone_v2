#!/usr/bin/python3
"""2-2-c_route module
starts a web app and handles routes
"""

from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():

    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():

    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    text = text.replace("_", " ")
    return "C {}".format(text)


if __name__ == "__main__":

    app.run(host="0.0.0.0")
