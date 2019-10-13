from flask import Flask, render_template, jsonify, request, abort
import json
import urllib
from utils import decode_polyline, COLORS

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

	# convert lat-lng values to floats
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
		The encoded polylines are sourced from Google Maps.
		It is returned as a response to the Google Maps Directions API.
		Yet to understand how exactly.
		Structure of this array: 
		[
			[], [], [] 
		]
	'''
	encoded_polyline_set = [
		r'g`_mDox~tM`E~GdHuHrF_FtRgQ^_@Nq@lE~D|AnAh@j@~B`CxThWdFdGhGjHlAqCh@u@xAiAbDgClCmBdByAh@i@NQ@IvAmBl@cAjAiBPSl@q@HE^g@fAkBz@gBXu@zAoDTg@b@}@V_@`AiAz@{@Xc@L]Jc@LuAt@yMN{B@aACQjBs@fFeBbBm@nAe@v@WHg@|AoExAe@XMEORIrQoGw@uCqBqHO_@eAm@eFuCyG{DyCsBKGTUdBoBVe@Xo@r@yBlAwDVg@Va@Xw@\{A\iBXkBdAmFNsABcAL}AJq@tA{Fz@qDRcAb@eCP}AJoAL_G?_CcB_OWiCU_BU_AgD{Jm@kBW_AeAiHcBqNm@_FOsBD_BHmALmA@GCCEGIS?]HYRQTEN@FBP?XCpAG`ASf@Oh@_@nByA`BmAbCoBhCkB|LuJdDeC|@u@~@}@^a@V[h@]p@q@nFeDz@_@z@W`Ce@fEWh@@j@LNHXD\CPENEDOLOVOP?VTn@r@TFPPbBhAfFtCvAdAh@`@lBhBjDvCtCvCrLzKrBzBh@c@@}@oAoAAOEKIMCMG{C?{C?zCFzCBLNX@NnAnAA|@Dr@A^h@^nA@vB@f@u@jH{Kr@oAv@aBbAqE\uAX{@z@sArC}DlEeHjGiJvOgUFs@@c@Ce@Go@a@]qK_KOMPY`CiDrEuGzBeDP_@\aAn@gCj@gC\gAqEoEuCiCcIwHc@UoDfCoAr@YH{BB}MPuDD{@hAO^GTFRJb@Ld@',
		r'g`_mDox~tM`E~GdHuHrF_FtRgQ^_@Nq@lE~D|AnAh@j@~B`CxThWdFdGhGjHlAqCh@u@xAiAbDgClCmBdByAh@i@NQ@IvAmBl@cAjAiBPSl@q@HE^g@fAkBz@gBXu@zAoDTg@b@}@V_@`AiAz@{@Xc@L]Jc@LuAt@yMN{B@aACQjBs@fFeBbBm@nAe@xIwClP}FbJkDzF{BrDqAf@]@C?GDIFEN@JN@@`@KlIwCtFqB~HqCxDoAzCiAhA]vE_BbC_A|B{@~@c@lE_Cv@i@nB}AtCoCxG_H|CwCfDaC`BgA`@_@rB{A|BwA`Cy@hE_BdDmA~DyAfHmCl@WtEeBtHkChH}Bf@UbBaAp@i@x@k@f@S`@C|CBdBAnMq@v@KbCMnLu@nBOtDc@rCa@dCc@n@O|EiA|@UdAOfCYrDY`CS`AQpAS|@SrFoAtCm@b@GrB[nIaBtI}AxKyBpGwAjGkAtKsBxBe@`@MnDq@`McCjGkAlDq@vEcAvH{AfLwBn@GrFeAdJcBfHiA|GiA~@QxBc@dDe@zDs@jFy@l@IbF{@`Fy@bBe@`@MvAu@zG{EpDoClAw@tByAjFyClMaHzEkCjCgAxAc@xD{@fMqClN_DtYuGGeB?gC@uEDuBDuCAuCGS[e@]c@s@m@iAi@W[IYCu@@gBEeH?yKC{K@aTE}DiG?uGAtG@hG?D|DA`TBzK?xKDdHAfBBt@HXVZhAh@r@l@\b@Zd@FR@tCEtCEtBAtE?z@?jAFdBBP{A^iDv@kQbE_]rHmEdAyAd@_Bp@}DrBuDtB}LvG]RoC`BkOtKiAt@iB~@aAZsCp@wDl@eHbAaNxBgIvA{GnAiGjAeFx@iF~@kGhAuGtAeDl@yI`B_OxCmPbDMDE_@O{@yAqFkCiK}AwGgAsEw@iEqAaIy@sEyAaGSk@Sa@eAeAeFwFkAmAyAiA_EsCuD}C_EaEwIyIyAaBkB_BiFkFyHeH}HyH_KoJ_ImHiAiAuBcBo@c@}@u@sQeQ}BwBiIeIkGcGeDcD}@y@S]I_@Dg@FkACw@I]o@}A{CqGM]Y@qA@eBzAqEtC_BhAyIzF{ClB}BtAoDfCoAr@YH[@_B@}MPuDDc@h@W^O^GTFRJb@Ld@',
		r'g`_mDox~tM`E~GdHuHrF_FtRgQ^_@Nq@lE~D|AnAh@j@~B`CxThWdFdGhGjHlAqCh@u@xAiAbDgClCmBdByAh@i@NQ@IvAmBl@cAjAiBPSl@q@HE^g@fAkBz@gBXu@zAoDTg@b@}@V_@`AiAz@{@Xc@L]Jc@LuAt@yMN{B@aACQjBs@fFeBbBm@nAe@v@WHg@|AoExAe@XMEORIrQoGw@uCqBqHO_@eAm@eFuCyG{DyCsBKGTUdBoBVe@Xo@r@yBlAwDVg@Va@Xw@\{A\iBXkBdAmFNsABcAL}AJq@tA{Fz@qDRcAb@eCP}AJoAL_G?_CcB_OWiCU_BU_AgD{Jm@kBW_AeAiHcBqNm@_FOsBD_BHmALmA@GCCEGIS?]HYRQTEN@FBP?XCpAG`ASf@Oh@_@nByA`BmAbCoBhCkB|LuJdDeC|@u@~@}@^a@V[h@]p@q@nCeBXEp@QtAc@fA[pBa@x@Iz@CfAKvAUb@M\Qv@k@lAkA\w@b@_Af@oAv@_Bj@y@fA}ArGoJr@gADO@SFIX]?KFSXg@BO@QwA_C_BiCrEoGhFuHfFgHqAkBcCmD{BuCs@_AO[GYQqDOuDfBMjPsAbFOjB?@MBEVQr@e@\c@Rm@G_@QcAUyAcAsHgCcR}BwOmAeJyAeK}@\uB`Ay@l@MPy@~Be@bA}AtDOOd@qArAaD~@{BPFw@|Be@bA}AtDw@xAc@l@_@^a@Vo@j@cA^i@Tu@Ps@HiBDkF@o@E?rGAtP?fQFzJ?TRVVXPR|AMtE]tE_@xD[jPsAbFOxFGtD?jJS?b@qGLwB@WZW\S^Od@`@|A'
	]
	
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
		polyline_points = decode_polyline(encoded_polyline_set[i])
		color = list(COLORS.values())[i % len(COLORS)]

		# # add start and end point to polyline_points
		polyline_points.insert(0, start)
		polyline_points.append(end)

		
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
		
		# construct route dict
		route = {
			"url": url,
			"waypoints": waypoints,
			"polyline_points": polyline_points,
			"color": color
		}

		routes.append(route)

	return json.dumps(routes)
# /====


if __name__ == '__main__':
	app.run(debug=True, port=8080, host='0.0.0.0')
