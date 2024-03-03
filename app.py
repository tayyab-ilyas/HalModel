from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from typing import List
import os

app = Flask(__name__)

soil_index_dict = {
  "1": "Sand",
  "2": "Loamy Sand",
  "3": "Sandy Loam",
  "4": "Silt Loam",
  "5": "Silt",
  "6": "Loam",
  "7": "Sandy Clay Loam",
  "8": "Clay Loam",
  "9": "Silty Clay Loam",
  "10": "Sandy Clay",
  "11": "Silty Clay",
  "12": "Clay"
}

suitableCrops = {
    "clay": ["Broccoli", "Brussels sprouts", "Cabbage", "Cauliflower", "Kale", "Beans", "Peas", "Potato", "Daikon radish"],
    "sandy clay": ["sweet", "corn", "okra", "radishes", "eggplant", "carrots", "pole beans", "greens", "spinach"],
    "silty clay": ["fruits, veggies"],
    "sandy clay loam": ["sweet corn", "okra", "radishes", "eggplant", "carrots", "pole beans", "greens", "spinach"],
    "clay loam": ["wheat", "sugarcane", "cotton", "pulses", "oilseeds"],
    "silty clay loam": ["faba bean", "maize", "pea", "rapeseed", "sorghum", "soybean", "sunflower", "wheat"],
    "sandy loam": ["Strawberries", "Blackberries", "Blueberries", "sweet corn", "okra", "radishes", "eggplant", "carrots", "pole beans", "greens", "spinach"],
    "sand": ["Carrots", "Radishes", "Potatoes", "Lettuce", "Collard greens", "Tomatoes", "Zucchini", "Corn", "Asparagus", "Watermelon", "Beans", "Cucumber"],
    "loamy sand": ["tomatoes", "peppers", "green beans", "cucumbers", "onions", "lettuce", "sweet corn", "okra", "radishes", "eggplant", "carrots", "pole beans", "greens", "spinach"],
    "loam": ["wheat", "sugarcane", "cotton", "pulses", "oilseeds", "veggies"],
    "silt": ["tomatoes", "sage", "peonies", "hellebore", "roses", "butterfly bush", "ferns", "daffodils"],
    "clay loam": ["tomatoes", "sage", "peonies", "hellebore", "roses", "butterfly bush", "ferns", "daffodils"],
    "silt loam": ["wheat", "potatoes", "sugar beet", "vining peas", "bulbs", "field vegetables"]
}

def soilType(sizes: List[float]):
    clay = 0
    sand = 0
    silt = 0

    for size in sizes:
        if size <= 0.002:
            clay += 10
        elif size <= 0.05:
            silt += 10
        elif size <= 2.0:
            sand += 10

    path = os.getcwd()
    df = pd.read_csv(filepath_or_buffer='soil_db.csv')

    X_train = df[['Clay %', 'Sand %', 'Silt %']]
    y_train = df['Classification']

    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train, y_train)

    result = knn.predict([[clay, sand, silt]])
    result = str(result[0])

    return_data = {}
    return_data["soil"] = soil_index_dict[result]

    soil_type = soil_index_dict[result].lower()
    return_data["suitableCrops"] = suitableCrops.get(soil_type, [])

    return return_data

@app.route('/predict_soil_type', methods=['POST'])
def predict_soil_type():
    try:
        data = request.get_json(force=True)
        example_list = data.get('example_list', [])
        soil_type_result = soilType(example_list)
        return jsonify(soil_type_result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(port=5000)