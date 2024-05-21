from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd 
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OrdinalEncoder

app = Flask(__name__, static_url_path='/static')

# Load datasets
df = pd.read_csv('data2.csv')

od = OrdinalEncoder()
cat=df.select_dtypes(include=[object])
df[od.get_feature_names_out()]=od.fit_transform(cat).astype(int)
encoded_categories = od.categories_
dict ={}
for i, col in enumerate(cat.columns):
    for j, category in enumerate(encoded_categories[i]):
        dict[category] = j

# Split features and target variable
y = df['price']
X = df.drop(columns='price')

def generate_model():
    # Initialize and train the RandomForestRegressor model
    model = RandomForestRegressor(criterion='poisson', random_state=42,
        n_estimators=100,
        max_depth=30,
        min_samples_split=3,
        min_samples_leaf=1,
        max_features='log2')
    model.fit(X, y)
    return model

def tonumeric(x):
    return dict.get(x)


@app.route('/')
def index():
    return render_template("model_index.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
        
        if 'city' not in request.form:
            return render_template('model_index.html',message = "City field was missing in the form data.")
        else:
            city = tonumeric(request.form['city'])

        if 'kind' not in request.form:
            return render_template('model_index.html',message = "Kind field was missing in the form data.")
        else:
            kind = tonumeric(request.form['kind'])
            
        if 'type' not in request.form:
            return render_template('model_index.html',message = "Type field was missing in the form data.")
        else:
            type_ = tonumeric(request.form['type'])

        # Extract features from the form
        features = [
            request.form['room'], request.form['bath'], request.form['area'],
            1 if request.form.get('balcony') == '1' else 0,
            1 if request.form.get('elevator') == '1' else 0,
            1 if request.form.get('natural_gas') == '1' else 0,
            1 if request.form.get('security') == '1' else 0,
            1 if request.form.get('water_gas') == '1' else 0,
            type_,request.form['district'],kind,
            request.form['floor'], city
        ]

        # Convert categorical features to numeric
        for i, value in enumerate(features):
            try:
                features[i] = int(value)
            except ValueError:
                features[i] = tonumeric(value)

        # Prepare data for prediction
        final_features = [np.array(features)]
        # Make predictions using the models
        predicted_price = model.predict(final_features)
        round_price = round(int(predicted_price[0]), -5)

        price = "{:,}".format(round_price)
        
        
        # Format the prediction results
        results = {'Price': price}
        # Return results as an HTML table
        table = '''<table border="1" style="width: 100%; font-size: 18px; text-align: center; border-collapse: collapse; border: 2px solid red;">
            <tr><th style="color: blue;"><b>Price</b></th></tr>
            <tr><td style="font-weight: bold;">{}</td></tr>
        </table>'''.format(results['Price'])

        # Return the HTML table as the response
        return render_template('model_index.html', message=table)

if __name__ == '__main__':
    model = generate_model()
    app.run(port=5002, debug=True, use_reloader=False)
