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

#Import car maintenacne costs
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

#Import car star ratings
starFeatures = ["make","model","stars"]
starsDf = pd.read_csv("CarsData/Car Reviews.csv", names=starFeatures, index_col=False)

#Uncapitalise make
starsDf['make'] = starsDf['make'].str.lower()
starsDf.sample(n=5)

# Apply the function to the column
starsDf['model'] = starsDf['model'].apply(lowercase_words)

merged_df = pd.merge(merged_df, starsDf, on=['make', 'model'], how='left')

# Define the color options
colors = ['red', 'green', 'blue', 'silver', 'black', 'yellow', 'white']

# Generate the "colour" column
merged_df['colour'] = np.random.choice(colors, size=len(merged_df))

# Generate the "co2" column with controlled precision
co2 = np.around(np.random.choice(np.arange(3, 5, 0.1), size=len(merged_df)), decimals=1)

# Add the "co2" column to the merged DataFrame
merged_df['co2(metric tons per year)'] = co2

# Replace 'hyundi' with 'hyundai'
merged_df['make'] = merged_df['make'].replace('hyundi', 'hyundai')






#Data exploration of each field
#Makes are fine (hyndai was spelled incorrectly)
makes = merged_df['make'].unique()
print(makes)

#Models is fine
models = merged_df['model'].unique()
print(models)

#Years seems to have cars from the future and cars that are far too old for most first time buyers
years = merged_df['year'].unique()
print(sorted(years))

#Look at distibution of years
yearcounts = merged_df['year'].value_counts()
print(yearcounts)

# Convert 'year' column to integers
merged_df['year'] = merged_df['year'].astype(int)

# Filtering out rows with years from 1970 to 2007 and the outlier from 2060
merged_df = merged_df[~merged_df['year'].between(1970, 2007)]
merged_df = merged_df[merged_df['year'] != 2060]

# Convert 'year' column back to strings
merged_df['year'] = merged_df['year'].astype(str)

#Test update
yearcounts = merged_df['year'].value_counts()
print(yearcounts)

#Prices seems fine
prices = merged_df['price'].unique()
print(sorted(prices))

#Transmission seems fine
transmissions = merged_df['transmission'].unique()
print(transmissions)

#Mileages seem fine
mileages = merged_df['mileage'].unique()
print(sorted(mileages))

#Fuel types seem fine
fuelTypes = merged_df['fuelType'].unique()
print(fuelTypes)

#Taxes seem fine
taxes = merged_df['tax'].unique()
print(sorted(taxes))

#Some very strangely low mpgs
merged_df['mpg'] = merged_df['mpg'].astype(float)
mpgs = merged_df['mpg'].unique()
print (sorted(mpgs))

#Isolate odd mpgs
weirdMpgs = [0.3, 1.1, 2.8, 5.5, 6.0, 8.8, 11.0]
df_mpg = merged_df['mpg'].isin (weirdMpgs)
df_mpg2 = merged_df[df_mpg]
print(df_mpg2)

#Remove petrol and diesel cars under 11.0 mpg
merged_df = merged_df[~((merged_df['fuelType'] == 'Petrol') | (merged_df['fuelType'] == 'Diesel')) | (merged_df['mpg'] >= 11.0)]

#Test
weirdMpgs = [0.3, 1.1, 2.8, 5.5, 6.0, 8.8, 11.0]
df_mpg = merged_df['mpg'].isin (weirdMpgs)
df_mpg2 = merged_df[df_mpg]
print(df_mpg2)

# Convert 'mpg' column back to strings
merged_df['mpg'] = merged_df['mpg'].astype(str)

#0.0 engine size?
engineSizes = merged_df['engineSize'].unique()
print(sorted(engineSizes))

#Look at distibution of engineSize
enginecounts = merged_df['engineSize'].value_counts()
print(enginecounts)

# Convert 'engineSize' column to floats
merged_df['engineSize'] = merged_df['engineSize'].astype(np.float16)

# Filtering out rows with engine size of 0.0
merged_df = merged_df[merged_df['engineSize'] != 0.0]

# Convert 'engine_size' column back to strings
merged_df['engineSize'] = merged_df['engineSize'].astype(str)

# Test
enginecounts = merged_df['engineSize'].value_counts()
print(enginecounts)

#Maintenance cost looks fine
maintenances = merged_df['maintenanceCostYearly'].unique()
print(sorted(maintenances))

#Stars is fine
stars = merged_df['stars'].unique()
print(sorted(stars))

#Colours is fine
colours = merged_df['colour'].unique()
print(sorted(colours))

co2s = merged_df['co2(metric tons per year)'].unique()
print(sorted(co2s))

# Define the folder path for exporting the CSV file
folder_path = "CarsData"

# Define the file path for the CSV export
combined_csv_path = os.path.join(folder_path, "merged_data.csv")

# Export the combined DataFrame to a CSV file in the specified folder
merged_df.to_csv(combined_csv_path, index=False)

#import csv

def read_csv_to_string(file_path):
    # Read CSV file and convert it to a string
    with open(file_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        csv_data = '\n'.join(','.join(row) for row in csv_reader)
    return csv_data

def write_string_to_file(data_string, output_file):
    # Write string data to a text file
    with open(output_file, 'w') as file:
        file.write(data_string)