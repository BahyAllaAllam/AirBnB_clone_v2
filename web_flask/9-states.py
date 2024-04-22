#!/usr/bin/python3
"""
Flask web application  listening on 0.0.0.0, port 5000
"""


from flask import Flask
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def list_states_with_or_without_id(id=None):
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda s: s.name)
    if id != None:
        for state in sorted_states:
            if state.id == id:
                sorted_cities = sorted(state.cities, key=lambda c: c.name)
                return render_template(
                        "9-states.html",
                        results=sorted_cities,
                        state=state,
                        id=id
                        )
    return render_template("9-states.html", results=sorted_states, id=id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
