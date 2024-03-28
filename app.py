# imports
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# make request to api and retrieve json with data
def fetch_air_quality_report(start_time, end_time, grid_id):
    # API endpoint
    api_url = "https://platform.airqo.net/api/v2/analytics/grid/report?token=NVSHTBYFX1QD11ZY"

    # Request parameters
    params = {
        "grid_id": grid_id,
        "start_time": start_time,
        "end_time": end_time
    }

    print("Fetching data from API...")
    # Fetching data from the API
    response = requests.post(api_url, json=params)
    
    print("API response status code:", response.status_code)

    if response.status_code == 200:
        # Extracting relevant PM2.5 data
        pm25_data = response.json()["airquality"]["datetime_mean_pm"]
        pm25_values = [data_point["pm2_5_raw_value"] for data_point in pm25_data]
        print("PM2.5 values within date range:", pm25_values)
        
        return {"pm25_values": pm25_values}  # Return PM2.5 values directly
    else:
        print("Failed to fetch air quality data")
        return "Failed to fetch air quality data"


@app.route('/generate_report', methods=['POST'])
def generate_air_quality_report():
    if request.is_json:
        data = request.json
    else:
        data = request.form

    start_time = data.get('start_time')
    end_time = data.get('end_time')
    grid_id = data.get('grid_id')

    print("Received POST request")
    print("Start time:", start_time)
    print("End time:", end_time)
    print("Grid ID:", grid_id)

    if not start_time or not end_time or not grid_id:
        print("Missing parameters")
        return jsonify({'error': 'Missing parameters'}), 400

    # Generate air quality report
    response_data = fetch_air_quality_report(start_time, end_time, grid_id)

    return jsonify(response_data)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
