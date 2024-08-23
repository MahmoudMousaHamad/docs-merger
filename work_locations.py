import csv
from geopy.geocoders import Nominatim
import time

# Initialize geolocator
geolocator = Nominatim(user_agent="oklahoma_town_locator")

# Define the towns array
towns = [
    "Oklahoma City", "Edmond", "Norman", "Spencer", "Midwest Cty", "Del City", "Tinker Air Force Base", "Yukon", 
    "Bethan", "Moore", "Newcastle", "Tulsa", "Jenks", "Broken Arrow", "Sand Springs", "Sapulpa", "Catoosa", "Owasso", 
    "Ada", "Addington", "Atoka", "Anadarko", "Apache", "Ardmore", "Bokchito", "Boswell", "Broken Bow", "Butler", 
    "Caddo", "Calumet", "Calvin", "Chickasha", "Choctaw", "Clinton", "Coalgate", "Cordell", "Dover", "Duncan", 
    "Durant", "Hastings", "Hartshorne", "Idabel", "Lawton", "Elk City", "El Reno", "Ft Cobb", "Ft Sill", "Hinton", 
    "Madill", "Muscogee Creek Nation", "Randlett", "Ringling", "Ryan", "Savanna", "Talihina", "Temple", "Thomas", 
    "Watonga", "Waureka", "Weatherford", "Woodward", "Vici"
]

# Remove duplicates
towns = list(dict.fromkeys(towns))

# Output file path
output_file = "oklahoma_towns_filled.csv"

# Function to get location details
def get_location_details(town_name):
    try:
        location = geolocator.geocode(f"{town_name}, Oklahoma")
        print(location)
        if location:
            return {
                'address': location.address,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'zip_code': location.raw['display_name'].split(",")[-2].strip()  # Extract ZIP code if available
            }
    except Exception as e:
        print(f"Error fetching data for {town_name}: {e}")
    return None

# Write to the CSV file
with open(output_file, mode='w', newline='') as outfile:
    writer = csv.writer(outfile)
    # Write the headers
    writer.writerow(['name', 'city center address', 'zip code', 'city center latitude', 'city center long'])

    for town_name in towns:
        location_details = get_location_details(town_name)
        if location_details:
            writer.writerow([
                town_name, 
                location_details['address'], 
                location_details['zip_code'], 
                location_details['latitude'], 
                location_details['longitude']
            ])
        else:
            # Write the town name with empty details if no location found
            writer.writerow([town_name, '', '', '', ''])
        
        time.sleep(1)  # To avoid hitting the API request limit

print("Data fetching complete. Output saved to", output_file)
