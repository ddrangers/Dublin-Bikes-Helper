from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    # get db connection
    return "render_template('index.html')"


@app.route('/contact')
def contact():
    # get db connection
    return "app.send_static_file(‘contact.html')"


@app.route('/stations')
def stations():
    # get db connection
    return "list of stations"


@app.route('/stations/<int:station_id>')
def station(station_id):
    # show the station with the given id, the id is an integer
    return 'Retrieving info for Station: {}'.format(station_id)
