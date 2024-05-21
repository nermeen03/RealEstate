from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__, static_url_path='/static')

class House:
    def __init__(self, location, property_details, amenities, price, additional_features):
        self.location = location
        self.property_details = property_details
        self.amenities = amenities
        self.price = price
        self.additional_features = additional_features

def process_query(houses, query):
    matching_houses = []
    for house in houses:
        if all(house_matches_criteria(house, criteria) for criteria in query):
            matching_houses.append(house)
    return matching_houses

# Extract min and max areas from criteria if provided
def house_matches_criteria(house, criteria):
    min_price = None
    max_price = None
    min_area = None
    max_area = None
    min_rooms = None
    max_rooms = None
    min_bathrooms = None
    max_bathrooms = None
    min_floor = None
    max_floor = None
    
    # Extract criteria from the dictionary
    for key, value in criteria.items():
        if key == "Price_min":
            min_price = value
        elif key == "Price_max":
            max_price = value
        elif key == "Area_min":
            min_area = value
        elif key == "Area_max":
            max_area = value
        elif key == "Room_min":
            min_rooms = value
        elif key == "Room_max":
            max_rooms = value
        elif key == "Bath_min":
            min_bathrooms = value
        elif key == "Bath_max":
            max_bathrooms = value
        elif key == "Floor_min":
            min_floor = value
        elif key == "Floor_max":
            max_floor = value
    
    
    # Check if the house matches the criteria
    if (min_price is not None and max_price is not None and
            not min_price <= house.price['Price'] <= max_price):
        return False
    if (min_area is not None and max_area is not None and
            not min_area <= house.property_details['Area'] <= max_area):
        return False
    if (min_rooms is not None and max_rooms is not None and
            not min_rooms <= house.property_details['Room'] <= max_rooms):
        return False
    if (min_bathrooms is not None and max_bathrooms is not None and
            not min_bathrooms <= house.property_details['Bath'] <= max_bathrooms):
        return False
    if (min_floor is not None and max_floor is not None and
            not min_floor <= house.property_details['Floor'] <= max_floor):
        return False

    # Otherwise, check other criteria
    for key, value in criteria.items():
        if key in house.location:
            if house.location[key] != value:
                return False
        elif key in house.amenities:
            if house.amenities[key] != value:
                return False
        elif key in house.additional_features:
            if house.additional_features[key] != value:
                return False
    
    return True

def load_houses_from_csv(file_path):
    df = pd.read_csv(file_path)
    houses = []
    for _, row in df.iterrows():
        location = {"City": row['city'], "District": row['district']}
        property_details = {
            "Room": row['room'],
            "Bath": row['bath'],
            "Area": row['area'],
            "Floor": row['floor']
        }
        amenities = {"Balcony": row['balcony'],
            "Elevator": row['elevator'],
            "Natural Gas": row['natural_gas'],
            "Security": row['security'],
            "Water Meter": row['water_meter']}
        price = {"Price": row['price']}
        additional_features = {"Finish Type": row['finish_type'], "Kind": row['kind']}
        house = House(location, property_details, amenities, price, additional_features)
        houses.append(house)
    return houses

@app.route('/')
def index():
    return render_template('expert_index.html')


@app.route('/search',methods=['POST','GET'])

def search():
    if request.method == 'POST':
        try:
            # Load houses from CSV
            houses = load_houses_from_csv('data.csv')

            price = int(request.form['price'])
            area = int(request.form['area'])
            rooms = int(request.form['rooms'])
            bathrooms = int(request.form['baths'])
            floor = int(request.form['floor'])

            if 'city' not in request.form:
                return render_template('expert_index.html',message = "City field was missing in the form data.")
            else:
                city = request.form['city']

            district = request.form['district']
            if 'kind' not in request.form:
                return render_template('expert_index.html',message = "Kind field was missing in the form data.")
            else:
                kind = request.form['kind']
            if 'type' not in request.form:
                return render_template('expert_index.html',message = "Type field was missing in the form data.")
            else:
                type_ = request.form['type']

            min_price = 400000
            max_price = price + 20000
            min_area = area - 20
            max_area = area + 50
            min_rooms = rooms 
            max_rooms = rooms + 2
            min_bathrooms = bathrooms 
            max_bathrooms = bathrooms + 2
            min_floor = floor - 2
            max_floor = floor + 2

            balcony = 1 if request.form.get('balcony') == "1" else 0
            elevator = 1 if request.form.get('elevator') == "1" else 0  
            natural_gas = 1 if request.form.get('natural_gas') == "1" else 0
            security = 1 if request.form.get('security') == "1" else 0
            water_meter = 1 if request.form.get('water_meter') == "1" else 0


            query = [
            {"City": city, "District": district},
            {"Price_min": min_price, "Price_max": max_price},  
            {"Room_min": min_rooms, "Room_max": max_rooms,
            "Bath_min": min_bathrooms, "Bath_max": max_bathrooms, 
            "Area_min": min_area, "Area_max": max_area,
            "Floor_min": min_floor, "Floor_max": max_floor},
            {"Finish Type": type_, "Kind": kind},
            {"Balcony": balcony, "Elevator": elevator,
            "Natural Gas": natural_gas, "Security": security,
            "Water Meter": water_meter}
            ]

            # Process form data and perform query
            matching_houses = process_query(houses, query)


            # Construct results
            results = []
            if len(matching_houses) >0:
                for house in matching_houses:
                    result = {
                        'Location': house.location['District'] + ', ' + house.location['City'],
                        'Price': house.price['Price'],
                        'Area': house.property_details['Area'],
                        'Rooms': house.property_details['Room'],
                        'Bathrooms': house.property_details['Bath'],
                        'Floor': house.property_details['Floor'],
                        'Kind': house.additional_features['Kind'],
                        'Finish Type': house.additional_features['Finish Type'],
                        'Balcony': house.amenities['Balcony'],
                        'Elevator': house.amenities['Elevator'],
                        'Natural Gas': house.amenities['Natural Gas'],
                        'Security': house.amenities['Security'],
                        'Water Meter': house.amenities['Water Meter']
                    }
                    results.append(result)


                # Return results as HTML table with bold text, centered, and increased font size
                table = '<div style="margin-bottom: 20px;">' \
                        '<button style="padding: 10px 20px; font-size: 18px; background-color: #009472; border: none; cursor: pointer;" onclick="window.location.href=\'/\'">Main Page</button>' \
                        '</div>' \
                        '<table border="1" style="width: 100%; height: 500px; font-size: 24px; text-align: center; border-collapse: collapse; border: 2px solid red;">' \
                        '<tr><th style="color: blue;"><b>Location</b></th><th style="color: blue;"><b>Price</b></th><th style="color: blue;"><b>Area</b></th>' \
                        '<th style="color: blue;"><b>Rooms</b></th><th style="color: blue;"><b>Bathrooms</b></th><th style="color: blue;"><b>Floor</b></th>' \
                        '<th style="color: blue;"><b>Kind</b></th><th style="color: blue;"><b>Finish Type</b></th><th style="color: blue;"><b>Balcony</b></th>' \
                        '<th style="color: blue;"><b>Elevator</b></th><th style="color: blue;"><b>Natural Gas</b></th><th style="color: blue;"><b>Security</b></th>' \
                        '<th style="color: blue;"><b>Water Meter</b></th></tr>'
                for result in results:
                    table += '<tr>'
                    table += '<td style="font-weight: bold;">' + result['Location'] + '</td>'
                    table += '<td style="font-weight: bold;">' + str(result['Price']) + '</td>'
                    table += '<td style="font-weight: bold;">' + str(result['Area']) + '</td>'
                    table += '<td style="font-weight: bold;">' + str(result['Rooms']) + '</td>'
                    table += '<td style="font-weight: bold;">' + str(result['Bathrooms']) + '</td>'
                    table += '<td style="font-weight: bold;">' + str(result['Floor']) + '</td>'
                    table += '<td style="font-weight: bold;">' + str(result['Kind']) + '</td>'
                    table += '<td style="font-weight: bold;">' + str(result['Finish Type']) + '</td>'
                    table += '<td style="font-weight: bold;">' + str(result['Balcony']) + '</td>'
                    table += '<td style="font-weight: bold;">' + str(result['Elevator']) + '</td>'
                    table += '<td style="font-weight: bold;">' + str(result['Natural Gas']) + '</td>'
                    table += '<td style="font-weight: bold;">' + str(result['Security']) + '</td>'
                    table += '<td style="font-weight: bold;">' + str(result['Water Meter']) + '</td>'
                    table += '</tr>'
                table += '</table>'

                # Return results as HTML response
                return table


            else:
                # Return error message as JSON response
                return render_template('expert_index.html',message = 'No matching houses found!!')
            
        except ValueError:
            # Return error message as JSON response
            return render_template('expert_index.html',message = 'Please enter valid values.')
            


if __name__ == '__main__':
    app.run(port=5001, debug=True)
