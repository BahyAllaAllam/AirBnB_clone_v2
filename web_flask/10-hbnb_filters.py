#!/usr/bin/python3
"""
Flask web application  listening on 0.0.0.0, port 5000
"""


from flask import Flask
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """
    Displays an HTML page with filters
    """
    states = storage.all("State").values()
    amenities = storage.all("Amenity").values()
    return render_template("10-hbnb_filters.html", states=states,
                           amenities=amenities)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
