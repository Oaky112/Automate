#Kyle Jones 
#Data Preprocessing
#Imports
import pandas as pd
import os
import numpy as np

#Import datasets
features = ["model","year","price","transmission","mileage","fuelType","tax","mpg","engineSize"]
audis = pd.read_csv("CarsData/audi.csv", names=features, index_col=False) 
bmws = pd.read_csv("CarsData/bmw.csv", names=features, index_col=False) 
fords = pd.read_csv("CarsData/ford.csv", names=features, index_col=False) 
hyundais = pd.read_csv("CarsData/hyundai.csv", names=features, index_col=False) 
mercs = pd.read_csv("CarsData/merc.csv", names=features, index_col=False) 
skodas = pd.read_csv("CarsData/skoda.csv", names=features, index_col=False) 
toyotas = pd.read_csv("CarsData/toyota.csv", names=features, index_col=False) 
vauxhalls = pd.read_csv("CarsData/vauxhall.csv", names=features, index_col=False) 
vws = pd.read_csv("CarsData/vw.csv", names=features, index_col=False) 

#Remove first row from cars
audis = audis.iloc[1:]
bmws = bmws.iloc[1:]
fords = fords.iloc[1:]
hyundais = hyundais.iloc[1:]
mercs = mercs.iloc[1:]
skodas = skodas.iloc[1:]
toyotas = toyotas.iloc[1:]
vauxhalls = vauxhalls.iloc[1:]
vws = vws.iloc[1:]

#Reset the index after removing the top row
audis.reset_index(drop=True, inplace=True)
bmws.reset_index(drop=True, inplace=True)
fords.reset_index(drop=True, inplace=True)
hyundais.reset_index(drop=True, inplace=True)
mercs.reset_index(drop=True, inplace=True)
skodas.reset_index(drop=True, inplace=True)
toyotas.reset_index(drop=True, inplace=True)
vauxhalls.reset_index(drop=True, inplace=True)
vws.reset_index(drop=True, inplace=True)

#Add the make of car
audis.insert(0, 'make', 'audi')
bmws.insert(0, 'make', 'bmw')
fords.insert(0, 'make', 'ford')
hyundais.insert(0, 'make', 'hyundi')
mercs.insert(0, 'make', 'mercedes')
skodas.insert(0, 'make', 'skoda')
toyotas.insert(0, 'make', 'toyota')
vauxhalls.insert(0, 'make', 'vauxhall')
vws.insert(0, 'make', 'volkswagen')

#Combine all datasets
combined_df = pd.concat([audis,bmws,fords,hyundais,mercs,skodas,toyotas,vauxhalls,vws], ignore_index=True)

maiFeatures = ["make","model","year","maintenanceCostYearly"]
maiCost = pd.read_csv("CarsData/Car Maintenance Costs.csv", names=maiFeatures, index_col=False) 

#Remove top row
maiCost = maiCost.iloc[1:]

#Reset the index after removing the top row
maiCost.reset_index(drop=True, inplace=True)

#Uncapitalise make
maiCost['make'] = maiCost['make'].str.lower()
maiCost.sample(n=5)

# Define a function to lowercase each individual word in a string
def lowercase_words(string):
    # Split the string into words
    words = string.split()
    # Lowercase each word individually
    lowercase_words = [word.lower() for word in words]
    # Join the words back together
    return ' '.join(lowercase_words)

# Apply the function to the column
maiCost['model'] = maiCost['model'].apply(lowercase_words)
combined_df['model'] = combined_df['model'].apply(lowercase_words)

merged_df = pd.merge(combined_df, maiCost, on=['make', 'model', 'year'], how='left')

# Generate the "stars" column
stars = np.random.choice(np.arange(2, 5.1, 0.1), size=len(merged_df))

# Prioritize numbers between 3.5 and 4
stars[(stars < 3.5) | (stars > 4)] = np.random.choice([3.5, 3.6, 3.7, 3.8, 3.9, 4.0], size=np.sum((stars < 3.5) | (stars > 4)))

# Add the "stars" column to the merged DataFrame
merged_df['stars'] = stars

# Define the color options
colors = ['red', 'green', 'blue', 'silver', 'black', 'yellow', 'white']

# Generate the "colour" column
merged_df['colour'] = np.random.choice(colors, size=len(merged_df))

# Define the folder path for exporting the CSV file
folder_path = "CarsData"

# Define the file path for the CSV export
combined_csv_path = os.path.join(folder_path, "merged_data.csv")

# Export the combined DataFrame to a CSV file in the specified folder
merged_df.to_csv(combined_csv_path, index=False)