import polyline

def decode_polyline(encoded_polyline):
	points = polyline.decode(encoded_polyline)
	
	# this returns a list of tuples
	# conver that into a list of lists instead
	points = list(map(list, points))

	return points

COLORS = {
	'green': '#DAF7A6',
	'yellow': '#FFC300',
	'orange': '#FF5733',
	'blue': '#2980B9',
	'grey': '#A6ACAF',
	'purple': '#6C3483'
}