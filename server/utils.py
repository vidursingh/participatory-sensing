import polyline

def decode_polyline(encoded_polyline):
	points = polyline.decode(encoded_polyline)
	
	# this returns a list of tuples
	# conver that into a list of lists instead
	points = list(map(list, points))

	return points