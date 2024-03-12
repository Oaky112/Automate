# Automate
## sfdfafafa
# Autotrader Car Scraper
## Overview
### This Python script automates the process of scraping car listings from the Autotrader website based on user-defined criteria. It utilizes web scraping techniques with Selenium WebDriver and BeautifulSoup to extract relevant car details such as price, year, mileage, etc., and saves the data into a CSV file.

## Features
User Input: Allows users to input their postcode and criteria such as the age of the car they are looking for.
Web Scraping: Utilizes Selenium WebDriver to automate browsing and scraping of Autotrader website.
Data Processing: Cleans and preprocesses the scraped data, calculates additional metrics like miles per year, filters data based on user-defined criteria, and sorts the data by distance.
CSV Output: Saves the scraped data into a CSV file for further analysis or reference.

## Requirements
- Python 3.x
- Selenium
- BeautifulSoup
- pandas

## Installation
1. Clone the repository: <br>
```
git clone https://github.com/your_username/autotrader-car-scraper.git
```
3. Install the required dependencies: <br>
```
pip install selenium beautifulsoup4 pandas
```
4. Download the appropriate WebDriver for your browser (e.g., Chrome WebDriver) and place it in the project directory.

## Usage
1. Run the script: <br>
```
python autotrader_car_scraper.py
```

3. Follow the prompts to input your postcode and criteria.
4. The script will scrape Autotrader for car listings based on the provided criteria and save the data into a CSV file.

## Contributing
Rusty

License
This project is licensed under the MIT License.

