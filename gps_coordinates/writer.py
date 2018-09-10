import json


"""This modules writes the coordinates to the external JSON file so that
    they can be displayed by google maps
"""
FILENAME = "../static/markers.json"
class Writer:
    def as_geojson(self, coordinates):
        data = {
            "type": "FeatureCollection",
            "features": []
        }

        for coor in coordinates:
            data['features'].append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates":[
                       coor['longitude'],
                       coor['latitude']
                    ]
                },
                "properties": {
                    "name": "Dinagat Islands"
                }
            })
        obj = open('./static/data.json', 'w')
        obj.write(json.dumps(data))
        obj.close()
