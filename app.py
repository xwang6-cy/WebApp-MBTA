# from flask import Flask





# app = Flask(__name__)


# @app.route('/')
# def hello():
#     return 'Hello World!'

from flask import Flask, render_template, request
from mbta_helper import find_stop_near

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        place_name = request.form['place_name']
        station_name, is_accessible = find_stop_near(place_name)
        if station_name:
            return render_template('mbta_station.html',
                                   place_name=place_name,
                                   station_name=station_name,
                                   is_accessible=is_accessible)
        else:
            return render_template('error.html')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
