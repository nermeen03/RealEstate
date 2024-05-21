from flask import Flask, render_template, request, url_for
import threading
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

df = pd.read_csv('data.csv')

@app.route('/static')

def floor_visualization():
    avg_price_by_floor = df[['floor', 'price']].groupby('floor')['price'].mean()

    # Plot line chart for all cities combined
    plt.figure(figsize=(10, 6))  # Adjust figure size if needed
    plt.plot(avg_price_by_floor.index, avg_price_by_floor.values, marker='o')

    # Set title and labels
    plt.xlabel('Floor Level')
    plt.ylabel('Average Price')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)  # Add grid lines for better visualization

    # Save the plot
    plt.tight_layout()
    plt.savefig(f'static/floor_price.png')

    # Close the plot object
    plt.close()

    # Return the plot object (optional, but recommended for cleaner code)
    return plt

def room_visualization():
    # Group by number of bathrooms and calculate the average price
    room_avg_price = df.groupby('room')['price'].mean()

    # Plot line chart
    plt.figure(figsize=(10, 6))  # Adjust figure size if needed
    plt.plot(room_avg_price.index, room_avg_price.values, marker='o', linestyle='-')

    # Set title and labels
    plt.xlabel('Number of Rooms')
    plt.ylabel('Average Price')
    plt.grid(True)  # Add grid lines for better visualization

    # Show plot
    plt.tight_layout()  # Adjust layout to prevent overlapping labels
    plt.savefig(f'static/room_price.png')

def bath_visualization():
    # Group by number of bathrooms and calculate the average price
    bath_avg_price = df.groupby('bath')['price'].mean()

    # Plot line chart
    plt.figure(figsize=(10, 6))  # Adjust figure size if needed
    plt.plot(bath_avg_price.index, bath_avg_price.values, marker='o', linestyle='-')

    # Set title and labels
    plt.xlabel('Number of Bathrooms')
    plt.ylabel('Average Price')
    plt.grid(True)  # Add grid lines for better visualization

    # Show plot
    plt.tight_layout()  # Adjust layout to prevent overlapping labels
    plt.savefig(f'static/bath_price.png')

def area_visualization():
    # Group by 'area' and calculate the average price for each area count
    area_price = df.groupby('area')['price'].mean()

    # Sort the index (area) for better visualization
    area_price = area_price.sort_index()

    # Plot line chart
    plt.figure(figsize=(10, 6))
    plt.plot(area_price.index, area_price.values, marker='o', linestyle='-')
    plt.xlabel('House Size (Area)')
    plt.ylabel('Average Price')
    plt.grid(True)
    plt.savefig(f'static/area_price.png')

def run_visualizations():
    area_visualization()
    room_visualization()
    bath_visualization()
    floor_visualization()


@app.route('/')
def index():
    return render_template('analysis_index.html', images_generated=False)

@app.route('/generate_visualizations', methods=['POST'])
def generate_visualizations():
    # Start a background thread to run all visualizations
    thread = threading.Thread(target=run_visualizations)
    thread.start()

    # Wait for the visualizations to be generated
    thread.join()

    # Render the template with images displayed
    return render_template('analysis_index.html', images_generated=True)


if __name__ == '__main__':
    app.run(port=5003, debug=True)