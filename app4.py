from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

# Define the path to the CSV file
CSV_FILE = 'data.csv'

@app.route('/')
def index():
    return render_template('add_index.html')

@app.route('/add_house', methods=['POST'])
def add_house():
    try:
        price = int(request.form['price'])
        area = int(request.form['area'])
        room = int(request.form['rooms'])
        bath = int(request.form['baths'])
        floor = int(request.form['floor'])
        if 'city' not in request.form:
            return render_template('add_index.html',message = "City field was missing in the form data.")
        else:
            city = request.form['city']

        district = request.form['district']

        if 'kind' not in request.form:
            return render_template('add_index.html',message = "Kind field was missing in the form data.")
        else:
            kind = request.form['kind']

        if 'type' not in request.form:
            return render_template('add_index.html',message = "Type field was missing in the form data.")
        else:
            finish_type = request.form['type']
        

        balcony = 1 if request.form.get('balcony') == '1' else 0
        elevator = 1 if request.form.get('elevator') == '1' else 0  
        natural_gas = 1 if request.form.get('natural_gas') == '1' else 0
        security = 1 if request.form.get('security') == '1' else 0
        water_meter = 1 if request.form.get('water_meter') == '1' else 0

        
        # Write the new house data to the CSV file
        with open(CSV_FILE, 'a', newline='') as csvfile:
            fieldnames = ['room','bath','price','area','balcony','elevator','natural_gas','security','water_meter','finish_type','district','kind','floor','city']

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Check if the file is empty and write headers if needed
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow({'room':room,'bath':bath,'price':price,'area':area,'balcony':balcony,'elevator':elevator,'natural_gas':natural_gas,'security':security,'water_meter':water_meter,'finish_type':finish_type,'district':district,'kind':kind,'floor':floor,'city':city})
            house ={'Price':price, 'Area':area,'Rooms':room,'Baths':bath,'floor':floor,
                    'city':city, 'district':district,'finish_type':finish_type,'kind':kind,
                    'balcony':balcony,'elevator':elevator,'natural_gas':natural_gas,'security':security,'water_meter':water_meter}

        message = f'House whose value is {house} is added successfully!'
        return render_template('add_index.html', message=message)

    except:
        message = 'Please Choose a City/Kind/Type'
        return render_template('add_index.html', message=message)
    
if __name__ == '__main__':
    app.run(port=5004, debug=True)
