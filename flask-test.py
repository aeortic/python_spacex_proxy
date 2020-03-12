from flask import Flask, escape, request
import requests as req
import json

app = Flask(__name__)

# dictionary with rocket_id as key
trimmed_rockets = dict()
           
# list with pruned launch data
trimmed_launches = list()

# currated list combining launches with rocket info
combined_launches = list()

def web_format(json_object):
    formatted = json.dumps(json_object, indent = 4)
    formatted = formatted.replace("\n", "<br/>")
    formatted = formatted.replace("\t", "&tab")
    formatted = "<pre>" + formatted + "</pre>"
    return formatted

def get_rockets():
    if len(trimmed_rockets) > 0:
        return trimmed_rockets

    r = req.get("https://api.spacexdata.com/v3/rockets")
    rockets = json.loads(r.text)

    for rocket in rockets:
        trimmed_rocket = {
                "rocket_id": rocket.get('rocket_id'),
                "rocket_name": rocket.get('rocket_name'),
                "description": rocket.get('description'),
                "country": rocket.get('country'),
                "company": rocket.get('company'),
                "cost_per_launch": rocket.get('cost_per_launch'),
                "images": rocket.get('flickr_images')
        }

        trimmed_rockets[rocket['rocket_id']] = trimmed_rocket

    return trimmed_rockets

def get_launches():
    if len(trimmed_launches) > 0:
        return trimmed_launches
    
    l = req.get("https://api.spacexdata.com/v3/launches")
    launches = json.loads(l.text)


    for launch in launches:
        trimmed_payloads = list()

        for payload in launch['rocket']['second_stage']['payloads']:
            trimmed_payload = {
                    "payload_id": payload.get('payload_id'),
                    "reused": payload.get('reused'),
                    "nationality": payload.get('nationality'),
                    "manufacturer": payload.get('manufacturer'),
                    "type": payload.get('payload_type'),
                    "customers": payload.get('customers')
            }

            trimmed_payloads.append(trimmed_payload)

        trimmed_launch = {
                "flight_number": launch.get('flight_number'),
                "mission_name": launch.get('mission_name'),
                "description": launch.get('details'),
                "launch_date_unix": launch.get('launch_date_unix'),
                "rocket": {"rocket_id": launch['rocket']['rocket_id']},
                "payloads": trimmed_payloads
        }
        
        trimmed_launches.append(trimmed_launch)
    
    return trimmed_launches

@app.route('/')
def index():
    if len(combined_launches) > 0:
        return web_format(combined_launches)
    
    rockets = get_rockets()
    launches = get_launches()

    for i in range(len(launches)):
        launch = launches[i].copy()
        rocket_id = launch['rocket']['rocket_id']
        rocket = rockets[rocket_id]
        launch['rocket'] = rocket
        combined_launches.append(launch)
        
    return web_format(combined_launches)

@app.route('/launches')
def launches_route():
    return web_format(get_launches())

@app.route('/rockets')
def rockets_route():
    return web_format(get_rockets())
