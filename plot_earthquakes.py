from datetime import date
import json
import requests
import matplotlib.pyplot as plt

def get_data():
    """Retrieve the data we will be working with."""
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )
    text = response.text
    data = json.loads(text)
    return data

#%%
def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year
#%%

def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]

# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve magnitudes of all earthquakes per year."""
    magnitudes_per_year = {}
    for earthquake in earthquakes:
        year = get_year(earthquake)
        magnitude = get_magnitude(earthquake)
        if magnitude is None:
            continue  # skip missing magnitudes
        if year not in magnitudes_per_year:
            magnitudes_per_year[year] = []
        magnitudes_per_year[year].append(magnitude)
    return magnitudes_per_year    

def plot_average_magnitude_per_year(earthquakes):
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)

    years = sorted(magnitudes_per_year.keys())
    avg_magnitudes = [sum(magnitudes_per_year[y]) / len(magnitudes_per_year[y]) for y in years]

    plt.figure(figsize=(8, 5))
    plt.plot(years, avg_magnitudes, color='orange', marker='o')
    plt.title("Average Magnitude of Earthquakes per Year")
    plt.xlabel("Year")
    plt.ylabel("Average Magnitude")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()


def plot_number_per_year(earthquakes):
    ...
    
if __name__ == "__main__":
    data = get_data()
    earthquakes = data["features"]

    plot_average_magnitude_per_year(earthquakes)
    #plot_number_per_year(quakes)
    plt.clf()
