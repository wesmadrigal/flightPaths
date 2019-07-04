from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



from build_graphs import get_airport_data, optimize_paths_distance_hops, find_airports, get_airport_data

@app.route('/build_flight_paths', methods=["POST"])
def build_flight_paths():
    import json
    if request.method == 'GET':
        return
    elif request.method == 'POST':
        print request.data
        data = json.loads(request.data)
        start = data['start_city'].encode('utf-8')
        print start
        end = data['end_city'].encode('utf-8')
        print end
        airportdata = get_airport_data()
        start_airport = list(reversed(find_airports(start, airportdata=airportdata)))[0]
        end_airport = list(reversed(find_airports(end, airportdata=airportdata)))[0]


        start_id = start_airport['airport_id']
        end_id = end_airport['airport_id']
        #print "Start airport id: {0}".format(start_id)
        #print "End airport id: {0}".format(end_id)
        #path = optimize_paths_distance_hops(str(start_id), str(end_id))
        path = optimize_paths_distance_hops(start_id, end_id)
        distance = path['distance']
        best_path = path['path']
        route = ' --> '.join([airportdata[i]['name'] for i in best_path]) + ' | Travel Distance : {0} KM'.format(str(round(distance)))
        path['route'] = route
        return json.dumps(path)

if __name__ == '__main__':
    app.run()
