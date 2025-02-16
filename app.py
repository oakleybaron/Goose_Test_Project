from flask import Flask, render_template
import requests
import folium
from datetime import datetime
import os

app = Flask(__name__)

SPACEX_API_URL = "https://api.spacexdata.com/v4/launches/upcoming"

@app.route('/')
def index():
    # Fetch upcoming launches
    response = requests.get(SPACEX_API_URL)
    launches = response.json()
    
    # Create a map centered on Kennedy Space Center
    m = folium.Map(location=[28.5728, -80.6490], zoom_start=4)
    
    # Add markers for each launch
    for launch in launches:
        if launch.get('launchpad'):
            # Fetch launchpad details
            launchpad_url = f"https://api.spacexdata.com/v4/launchpads/{launch['launchpad']}"
            launchpad = requests.get(launchpad_url).json()
            
            # Create popup content
            launch_date = datetime.fromtimestamp(launch['date_unix']).strftime('%Y-%m-%d %H:%M:%S')
            popup_content = f"""
                <b>{launch['name']}</b><br>
                Date: {launch_date}<br>
                Launchpad: {launchpad['name']}<br>
            """
            
            # Add marker to map
            folium.Marker(
                location=[launchpad['latitude'], launchpad['longitude']],
                popup=popup_content,
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
    
    # Save map to static folder
    if not os.path.exists('static'):
        os.makedirs('static')
    m.save('static/map.html')
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)