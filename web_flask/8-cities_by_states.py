#!/usr/bin/python3
"""
Flask web application  listening on 0.0.0.0, port 5000
"""


from flask import Flask
import models


app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    states = models.storage.all(State).values()
    sorted_states = sorted(states, key=lambda s: s.name)
    return render_template("8-cities_by_states.html", states=sorted_states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
