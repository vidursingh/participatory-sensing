from flask import Flask, render_template, jsonify, request, abort
import json
import urllib

app = Flask(__name__)
app.config["SECRET_KEY"] = "somesecretthatonlyiknowandyouwillneverevedfhjklkjhgfdreverget"

# .====

@app.route('/suggest_route')
def suggest_route():
	'''
		This function returns a JSON object containing 3 (or more)
		routes. We send the Cross-platform URL for each route.
		Documentation for Cross-platform URLS: https://developers.google.com/maps/documentation/urls/guide

		This URI is called as follows:
			/suggest_route?start_lat=lat&start_lng=lng&end_lat=lat&end_lng=lng
	'''
	
	start = [request.args.get('start_lat'), request.args.get('start_lng')]
	end = [request.args.get('end_lat'), request.args.get('end_lng')]

	# convert values to floats
	start = list(map(float, start))
	end = list(map(float, end))

	# defines number of routes we want to send to the app
	number_of_routes = 3

	'''
		The waypoints are sourced from Google Maps.
		Yet to understand how exactly.
		Structure of this array: 
		[
			[], [], [] 
		]
	'''
	waypoint_set = [
		[[28.935536,77.099374], [28.906680,77.109102], [28.882645,77.118494]],
		[[28.935536,77.099374], [28.906680,77.109102], [28.882645,77.118494]],
		[[28.935536,77.099374], [28.906680,77.109102], [28.882645,77.118494]]
	]

	assert len(waypoint_set) == number_of_routes

	
	'''
	This is the final object that will be sent. Structure is as follows:
		[
			{
				"url": f"",
				"waypoints": []
			}
		]
	URL structure:
		https://www.google.com/maps/dir/?api=1&origin=28.943842,77.103218&destination=28.631682,77.219708&travelmode=driving&waypoints=28.935536,77.099374|28.906680,77.109102|28.882645,77.118494
	'''
	routes = []
	for i in range(number_of_routes):
		waypoints = waypoint_set[i]
		
		# construct url
		baseurl = f'https://www.google.com/maps/dir/'
		url_params = {
			'api': '1',
			'origin': f'{start[0]},{start[1]}',
			'destination': f'{end[0]},{end[1]}',
			'travelmode': 'driving',
			'waypoints': "|".join([f"{waypoint[0]},{waypoint[1]}" for waypoint in waypoints])
		}
		# urlencode the params to construct final url
		url = baseurl + '?' + urllib.parse.urlencode(url_params)
		
		route = {
			"url": url,
			"waypoints": waypoints
		}

		routes.append(route)

	return json.dumps(routes)
# /====


if __name__ == '__main__':
	app.run(debug=True, port=8080, host='52.127.0.178')
