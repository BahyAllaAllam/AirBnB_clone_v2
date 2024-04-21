#!/usr/bin/python3
"""
Flask web application  listening on 0.0.0.0, port 5000
"""


from flask import Flask
from models import storage
import models


app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    return render_template("7-states_list.html", states=storage.all(models.State))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
