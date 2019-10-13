import polyline

def decode_polyline(encoded_polyline):
	points = polyline.decode(encoded_polyline)
	
	# this returns a list of tuples
	# conver that into a list of lists instead
	points = list(map(list, points))

	return points

COLORS = {
	'purple': '#6C3483',
	'grey': '#A6ACAF',
	'orange': '#FF5733',
	'green': '#DAF7A6',
	'blue': '#2980B9',
	'pink': '#ff69b4'
}