from flask import Flask, request, jsonify
import util
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/get_general_condition', methods=['GET'])
def get_general_condition():
    response = jsonify({
        'general_condition': util.get_general_condition()
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/get_heating', methods=['GET'])
def get_heating():
    response = jsonify({
        'heating': util.get_heating()
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/predict_price', methods=['GET', 'POST'])
def predict_price():
    area_m2 = float(request.form['area_m2'])
    rooms = float(request.form['rooms'])
    general_condition = request.form['general_condition']
    heating = request.form['heating']
    neighborhood = request.form['neighborhood']

    response = jsonify({
        'estimated_price': util.get_estimated_price(area_m2, rooms, general_condition, heating, neighborhood)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == '__main__':
    util.load_saved_artifacts()
    print("Starting Flask Server For Belgrade RPP...")
    app.run()