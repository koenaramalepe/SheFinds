from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import logging
app = Flask(__name__, static_folder='.')
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

BASE_URL = "https://api-ubt.mukuru.com/taurus/v1/resources/pay-out-partners"

COUNTRY_URLS = {
    "ZW": "https://api-ubt.mukuru.com/taurus/v1/resources/pay-out-partners/{payOutPartnerGuid}/locations",
    "MW": "https://api-ubt.mukuru.com/taurus/v1/resources/pay-out-partners/{payOutPartnerGuid}/locations",
    "ZM": "https://api-ubt.mukuru.com/taurus/v1/resources/pay-out-partners/{payOutPartnerGuid}/locations"
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# @app.route('/api/payout-partners')
# def get_payout_partners():
#     country = request.args.get('country')
#     url = f"{BASE_URL}"
#     params = {"Country": country, "page_size": 100, "page": 1}
    
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         partners = response.json()
#         return jsonify([{"name": partner['name'], "guid": partner['guid']} for partner in partners['items']])
#     else:
#         return jsonify({"error": "Unable to fetch payout partners"}), 400

@app.route('/api/payout-partners')
def get_payout_partners():
    headers = {"Authorization": "{BASE_URL}"}
    country = request.args.get('country')
    url = f"{BASE_URL}"
    params = {"Country": country, "page_size": 100, "page": 1}

    api_response = requests.get(url, params=params)
    # Print the entire response text (as a string)
    print(f"Response Text: {api_response.json}")
     
    # response = null
    
    # If the response is JSON and you want to print it in a structured way:
    try:
        response_json = api_response.json()  # Converts the response to a dictionary
        print("Response JSON:", response_json)
    except ValueError:
        print("Response is not in JSON format")

    if api_response.status_code == 200:
        partners = api_response.json()
        # Log the response to inspect it
        logging.debug(f"Partners data: {partners}")
        response = jsonify([{"name": partner['name'], "guid": partner['guid']} for partner in partners['items']])
    else:
        logging.error("Unable to fetch payout partners")
        response =  jsonify({"error": "Unable to fetch payout partners"}), 400

    response.headers.add('Access-Contro9l-Allow-Origin', '*')
    return response




@app.route('/api/payout-locations')
def get_payout_locations():
    country = request.args.get('country')
    partner_guid = request.args.get('partner_guid')
    city = request.args.get('city')

    if country not in COUNTRY_URLS:
        return jsonify({"error": "Unsupported country code"}), 400
    
    url = COUNTRY_URLS[country].format(payOutPartnerGuid=partner_guid)
    params = {"page_size": 100, "page": 1}
    
    api_response = requests.get(url, params=params)
    if api_response.status_code == 200:
        locations = api_response.json()
        if city:
            response = jsonify(get_locations_by_city(locations, city))
        else:
            response = jsonify(get_cities(locations))
    else:
        response = jsonify({"error": "Unable to fetch payout locations"}), 400
    
    response.headers.add('Access-Contro9l-Allow-Origin', '*')
    return response


def get_cities(locations):
    cities = set()
    if locations and 'items' in locations:
        for location in locations['items']:
            if 'address' in location and 'city' in location['address']:
                cities.add(location['address']['city'])
    return sorted(list(cities))

def get_locations_by_city(locations, city):
    city_locations = []
    for location in locations['items']:
        if location['address']['city'] == city:
            city_locations.append({
                "name": location['name'],
                "address": f"{location['address']['streetAddress']}, {location['address']['city']}",
                "coordinates": f"{location['coordinates']['latitude']}, {location['coordinates']['longitude']}" if 'coordinates' in location else "Not available",
                "currencies": ", ".join(location['currencies'])
            })
    return city_locations



if __name__ == '__main__':
    app.run(debug=True)