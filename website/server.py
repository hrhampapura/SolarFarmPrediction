from flask import Flask, request, jsonify
import util

app = Flask(__name__)


@app.route('/classify_solar_site',methods=['POST'])
def classify_solar_site():
	lat = float(request.form['lat'])
	lon = float(request.form['lon'])
	model = request.form['model']

	response = jsonify({
		'solar_site_classification': util.classify_solar_site(lat,lon,model)
		})

	response.headers.add('Access-Control-Allow-Origin', '*')

	return response


if __name__ == "__main__":
	util.load_saved_artifacts()
	app.run()